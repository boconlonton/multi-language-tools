from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Screen
from project.models import Project


@login_required(login_url="/")
def screen_home(request):
    vocabs = Screen.objects.all().order_by('-id')
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
    project = get_object_or_404(Project, project_name='pms')
    if request.method == 'POST':
        data = {
            'screen_code': request.POST.get('scrCode').strip(),
            'screen_name': request.POST.get('scrName').strip(),
            'description': request.POST.get('scrDesc').strip(),
            'url': request.POST.get('scrURL').strip(),
            'project': project,
            'modified_by': request.user,
            'created_by': request.user
        }
        Screen.objects.create(**data)
    return render(
        request,
        'screen/create.html',
        {'project': project}
    )


@login_required(login_url='/')
def screen_detail(request, screen_id):
    screen = get_object_or_404(Screen, pk=screen_id)
    if request.method == 'POST':
        screen.screen_code = request.POST.get('scrCode').strip()
        screen.screen_name = request.POST.get('scrName').strip()
        screen.description = request.POST.get('scrDesc').strip()
        screen.url = request.POST.get('scrURL').strip()
        screen.modified_by = request.user
        screen.project = get_object_or_404(Project, pk=1)
        screen.save()
        screen.refresh_from_db()
    return render(
        request,
        'screen/detail.html',
        {'screen': screen}
    )
