from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'cbayweb/homepage.html',{})

def viewItem(request):
	return render(request, 'cbayweb/viewItem.html',{})
