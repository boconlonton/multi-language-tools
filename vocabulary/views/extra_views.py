import json

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from utils import get_or_none, create_screen_from_code_only

from vocabulary.models import Vocabulary
from screen.models import Screen


@login_required(login_url="/accounts/login")
def vocab_export_home(request):
    search_key = request.GET.get('scrCodeSearch')
    page_obj = None
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
            screens = Screen.objects.filter(screen_code__icontains=search_key.strip())
            return render(
                request,
                'vocabulary/export.html',
                {
                    'screens': screens,
                    'search_key': search_key
                 }
            )
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
def vocab_export_home_with_code(request, screen_code):
    search_key = screen_code
    page_obj = None
    languages = {
        'en': 'English',
        'vi': 'Vietnam',
        'kr': 'Korean'
    }
    if request.method == 'POST' or search_key:
        search_key = request.POST.get('scrCodeSearch') or search_key
        try:
            screen = Screen.objects.get(screen_code=search_key.strip())
        except Screen.DoesNotExist:
            screens = Screen.objects.filter(screen_code__icontains=search_key.strip())
            return render(
                request,
                'vocabulary/export.html',
                {
                    'screens': screens,
                    'search_key': search_key
                 }
            )
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


@login_required(login_url='/accounts/login')
def vocab_import(request):
    if request.method == 'POST':
        structure = {
            "screen_name": {
                "key": {
                    "en": "",
                    "vi": ""
                }
            }
        }
        data = request.FILES.get('json').read()
        data_parse = json.loads(data)
        list_screens = data_parse.keys()
        for screen_code in list_screens:
            screen = get_or_none(Screen, screen_code=screen_code)
            if not screen:
                screen = create_screen_from_code_only(
                    screen_code=screen_code,
                    user=request.user
                )
            list_words = list_screens[screen_code].keys()
            # for word in list_words:
    return render(
        request,
        'vocabulary/import.html',
    )
