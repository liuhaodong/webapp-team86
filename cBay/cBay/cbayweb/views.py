from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core import serializers
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from forms import *

# Create your views here.
@login_required
def homepage(request):
	return render(request, 'cbayweb/homepage.html',{})

@login_required
def viewItem(request):
	return render(request, 'cbayweb/viewItem.html',{})

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password'],
				email=form.cleaned_data['email']
			)
			user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
			login(request, user)
			return redirect('/')
		else:
			print('form error')
			return render(request, 'cbayweb/register.html',{'form':form})
	else:
		form = RegisterForm()
	return render(request, 'cbayweb/register.html',{'form':form})


def reviewOrder(request):
	return render(request, 'cbayweb/reviewOrder.html',{})

def postItem(request):
	return render(request, 'cbayweb/postItem.html',{})

def accountManage(request):
	return render(request, 'cbayweb/accountManage.html',{})