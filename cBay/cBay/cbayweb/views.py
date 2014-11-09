from django.shortcuts import render
from forms import *

# Create your views here.
def homepage(request):
    return render(request, 'cbayweb/homepage.html',{})

def viewItem(request):
	return render(request, 'cbayweb/viewItem.html',{})

def register(request):
	if request.method == 'POST':
		pass
	else:
		form = RegisterForm()
	return render(request, 'cbayweb/register.html',{'form':form})

def login(request):
	if request.method == 'POST':
		pass
	else:
		form = LoginForm()
	return render(request, 'cbayweb/login.html',{'form':form})