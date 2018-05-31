from django.contrib.auth.views import logout, login
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from .forms import RegisterForm , UserUpdateForm
from django.contrib.auth.models import Group,User
from django.urls import reverse
from Project.models import Book
from Project.forms import BookForm


# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None)
    print(request.POST)
    context = {'register': form }
    if request.method == 'POST':

        if form.is_valid():

            form.save()
            return redirect('/')
      
    return render(request, 'registration/register.html' , context)

def logout_view(request):
    logout()


def member_add(request):
    group = Group.objects.get(name='Librarian')
    form = RegisterForm(request.POST or None)
    if group not in request.user.groups.all():
        return redirect('/')
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            grp = Group.objects.get(name='members')
            instance.groups.add(grp)
            return redirect('member_list')
    context = {'form': form , 'group': group}
    return render(request, 'member_add.html', context)

def member_list(request):
    members = User.objects.filter(groups__name='members')
    context = {'members': members}
    return render(request, 'member_list.html', context)

def member_detail(request, id):
    member = User.objects.get(id=id)
    form = UserUpdateForm(request.POST or None , instance= member)
    if request.method == 'POST':
        if form.is_valid():
            member.username = form.cleaned_data.get('username')
            member.first_name = form.cleaned_data.get('first_name')
            member.last_name = form.cleaned_data.get('last_name')
            member.email = form.cleaned_data.get('email')
            member.save()
            return redirect(reverse('member_detail', kwargs={'id':id}))
    context = {'member': member, 'form': form}
    return render(request, 'member_detail.html', context)

def member_search(request):
    query = request.GET.get('q')
    members = User.objects.filter(username__icontains=query)
    print(query)
    print(members)
    context = {'members': members}
    return render(request, 'member_search.html', context)

def member_delete(request, id):
    member = User.objects.get(id=id)
    member.delete()
    return redirect(reverse('member_list'))

def librarian_liste(request):
    group= Group.objects.get(name='admin')
    if group not in request.user.groups.all():
        return redirect('/')
    librarian = User.objects.filter(groups__name='Librarian')
    context={'librarian':librarian , 'group':group}
    return render(request, 'Librarian_liste.html', context )

def librarian_delete(request, id):
    librarian = User.objects.get(id=id)
    librarian.delete()
    return redirect(reverse('librarian_liste'))


def librarian_update (request, id):
    librarian = User.objects.get(id=id)
    form = UserUpdateForm(request.POST or None , instance= librarian)
    if request.method == 'POST':
        if form.is_valid():
            librarian.username = form.cleaned_data.get('username')
            librarian.first_name = form.cleaned_data.get('first_name')
            librarian.last_name = form.cleaned_data.get('last_name')
            librarian.email = form.cleaned_data.get('email')
            librarian.save()
            return redirect(reverse('librarian_update', kwargs={'id':id}))
    context = {'librarian': librarian, 'form': form}
    return render(request, 'librarian_update.html', context)