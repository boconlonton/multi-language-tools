from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Screen


@login_required(login_url="/")
def screen_home(request):
    vocabs = Screen.objects.all()
    paginator = Paginator(vocabs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'screen/home.html',
        {'page_obj': page_obj}
    )


@login_required(login_url="/")
def screen_create(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        eng = request.POST.get('eng')
        vn = request.POST.get('vn')
        korea = request.POST.get('korea')
        Screen.objects.create(
            vocab_key=key,
            english_definition=eng if eng else "",
            vn_definition=vn if vn else "",
            korean_definition=korea if korea else "",
            created_by=request.user,
            modified_by=request.user
        )
    return render(
        request,
        'screen/create.html'
    )


@login_required(login_url='/')
def screen_detail(request, screen_id):
    screen = get_object_or_404(Screen, pk=screen_id)
    if request.method == 'POST':
        pass
        # key = request.POST.get('key').strip()
        # eng = request.POST.get('eng').strip()
        # vn = request.POST.get('vn').strip()
        # korea = request.POST.get('korea').strip()
        # vocab.key = key
        # vocab.english_definition = eng
        # vocab.vn_definition = vn
        # vocab.korean_definition = korea
        # vocab.save()
        # vocab.refresh_from_db()
    return render(
        request,
        'screen/detail.html',
        {'screen': screen}
    )
