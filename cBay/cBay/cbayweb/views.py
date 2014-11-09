from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'cbayweb/homepage.html',{})

def viewItem(request):
	return render(request, 'cbayweb/viewItem.html',{})

def reviewOrder(request):
	return render(request, 'cbayweb/reviewOrder.html',{})

def postItem(request):
	return render(request, 'cbayweb/postItem.html',{})

def accountManage(request):
	return render(request, 'cbayweb/accountManage.html',{})