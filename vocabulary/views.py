from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Vocabulary
from screen.models import Screen


@login_required(login_url="/accounts/login")
def vocab_home(request):
    search_key = None
    if request.GET.get('search'):
        search_key = request.GET.get('search').strip()
        vocabs = Vocabulary.objects.filter(vocab_key__contains=search_key)\
            .order_by('-id')
    else:
        vocabs = Vocabulary.objects.all().order_by('-id')
    paginator = Paginator(vocabs, 10)
    if request.GET.get('page'):
        page_number = int(request.GET.get('page')) if int(request.GET.get('page')) > 0 else 1
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    last_page = paginator.num_pages
    if page_number - 2 < 1:
        min_range = 1
    elif page_number == last_page:
        min_range = last_page - 3 if last_page - 3 > 0 else 1
    else:
        min_range = page_number - 2
    if page_number + 1 > last_page:
        max_range = last_page
    elif page_number == last_page:
        max_range = last_page
    else:
        max_range = page_number + 1
    page_range = range(min_range, max_range + 1)
    return render(
        request,
        'vocabulary/home.html',
        {
            'page_obj': page_obj,
            'paginator': paginator,
            'page_range': page_range,
            'search_key': search_key
        }
    )


@login_required(login_url="/accounts/login")
def vocab_create(request):
    screens = Screen.objects.all().order_by('-id')
    search_key = None
    if request.method == 'POST':
        search_key = request.POST.get('scrCodeSearch')
        if search_key:
            screens = Screen.objects.filter(
                screen_code__contains=search_key.strip()
            ).order_by('-id')
        else:
            key = request.POST.get('key')
            eng = request.POST.get('eng')
            vn = request.POST.get('vn')
            korea = request.POST.get('korea')
            vocab = Vocabulary.objects.create(
                vocab_key=key,
                english_definition=eng if eng else "",
                vn_definition=vn if vn else "",
                korean_definition=korea if korea else "",
                created_by=request.user,
                modified_by=request.user
            )
            vocab.screen.add(request.POST.get('scrCode'))
            vocab.save()
            return redirect('vocab-home')
    return render(
        request,
        'vocabulary/create.html',
        {
            'screens': screens,
            'search_key': search_key
        }
    )


@login_required(login_url="/accounts/login")
def vocab_detail(request, vocab_id):
    vocab = get_object_or_404(Vocabulary, pk=vocab_id)
    screens = vocab.screen.all()
    screen_search = screens
    if request.method == 'POST':
        search_key = request.POST.get('scrCodeSearch')
        if search_key:
            screen_search = Screen.objects.filter(
                screen_code__contains=search_key.strip()
            ).order_by('-id')
        elif request.POST.get('scrCode'):
            vocab = Vocabulary.objects.get(pk=vocab_id)
            scrn_code = request.POST.get('scrCode')
            screen = Screen.objects.get(pk=scrn_code)
            if screen not in vocab.screen.all():
                vocab.screen.add(screen)
                vocab.save()
        elif request.POST.get('key'):
            key = request.POST.get('key').strip()
            eng = request.POST.get('eng').strip()
            vn = request.POST.get('vn').strip()
            korea = request.POST.get('korea').strip()
            vocab.key = key
            vocab.english_definition = eng
            vocab.vn_definition = vn
            vocab.korean_definition = korea
            vocab.modified_by = request.user
            vocab.save()
            vocab.refresh_from_db()
    return render(
        request,
        'vocabulary/detail.html',
        {
            'vocab': vocab,
            'screens': screens,
            'screen_search': screen_search
         }
    )


@login_required(login_url="/accounts/login")
def vocab_delete_screen(request, vocab_id, screen_id):
    vocab = Vocabulary.objects.get(pk=vocab_id)
    screen = Screen.objects.get(pk=screen_id)
    if screen in vocab.screen.all():
        vocab.screen.remove(screen)
        vocab.save()
    return redirect('vocab-detail', vocab_id=vocab_id)


@login_required(login_url="/accounts/login")
def vocab_export_home(request):
    page_obj = None
    search_key = None
    languages = {
        'en': 'English',
        'vi': 'Vietnam',
        'kr': 'Korean'
    }
    if request.method == 'POST':
        search_key = request.POST.get('scrCodeSearch')
        try:
            screen = Screen.objects.get(screen_code=search_key.strip())
        except Screen.DoesNotExist:
            return render(request,'404.html')
        vocabs = Vocabulary.objects.filter(
            screen__id=screen.id
        ).order_by('id')
        paginator = Paginator(vocabs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(
        request,
        'vocabulary/export.html',
        {
            'page_obj': page_obj,
            'search_key': search_key,
            'languages': languages.items(),
        }
    )


@login_required(login_url="/accounts/login")
def vocab_export(request, language, screen_code):
    language_dict = {
        'en': lambda x: getattr(x, "english_definition"),
        'vi': lambda x: getattr(x, "vn_definition"),
        'kr': lambda x: getattr(x, "korean_definition")
    }
    screen = Screen.objects.get(screen_code=screen_code)
    vocabs = Vocabulary.objects.filter(
        screen__id=screen.id
    ).order_by('id')
    response = {}
    for vocab in vocabs:
        response[vocab.vocab_key] = language_dict[language](vocab)
    res = JsonResponse(
        response,
        safe=False,
        json_dumps_params={'ensure_ascii': False}
    )
    res['Content-Disposition'] = f'attachment; filename={screen.screen_code}.json'
    return res
