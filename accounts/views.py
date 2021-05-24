from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            auth.login(request, user)
            return redirect('vocab-home')
        else:
            return render(request, 'accounts/login.html',
                          {'error': 'username or password is incorrect'}
                          )

    else:
        return render(request, "accounts/login.html")


@login_required(login_url="/accounts/login")
def logout(request):
    # TODO: Need to route to hompage
    # and don't forget to logout.
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
    else:
        return render(request, "accounts/logout.html")
