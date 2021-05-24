from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Screen
from project.models import Project


@login_required(login_url="/accounts/login")
def screen_home(request):
    search_key = None
    if request.GET.get('search'):
        search_key = request.GET.get('search').strip()
        screens = Screen.objects.filter(screen_code__contains=search_key)\
            .order_by('-id')
    else:
        screens = Screen.objects.all().order_by('-id')
    paginator = Paginator(screens, 5)
    if request.GET.get('page'):
        page_number = int(request.GET.get('page')) if int(request.GET.get('page')) > 0 else 1
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    if page_number - 1 < 1:
        min_range = 1
    else:
        min_range = page_number - 1
    if page_number + 5 > paginator.num_pages:
        max_range = paginator.num_pages
    else:
        max_range = page_number + 5

    page_range = range(min_range, max_range+1)
    return render(
        request,
        'screen/home.html',
        {
            'page_obj': page_obj,
            'search_key': search_key,
            'page_range': page_range
        }
    )


@login_required(login_url="/accounts/login")
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


@login_required(login_url="/accounts/login")
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
