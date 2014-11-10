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
def viewSale(request, sale_id):
	sale = get_object_or_404(Sale, id=sale_id)
	context = {}
	context['sale'] = sale 
	comments = []
	context['comments'] = comments
	return render(request, 'cbayweb/viewSale.html',context)

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password'],
				email=form.cleaned_data['email']
			)
			new_profile = Profile(user = user)
			new_profile.save()
			user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
			login(request, user)
			return redirect('/')
		else:
			print(form.errors)
			return render(request, 'cbayweb/register.html',{'form':form})
	else:
		form = RegisterForm()
	return render(request, 'cbayweb/register.html',{'form':form})

@login_required
def reviewOrder(request):
	return render(request, 'cbayweb/reviewOrder.html',{})


@login_required
def placeOrder(request):
	if request.method == 'POST':
		context = {}
		my_sale=get_object_or_404(Sale, id=request.POST['sale_id'])
		print(my_sale.name)
		new_order = Order(buyer = request.user, sale=my_sale, quantity = request.POST['sale_quantity'])
		new_order.price = (float)(new_order.sale.price) * (float)(new_order.quantity)
		new_order.save()
		print('new order is saved')
		context['order'] = new_order
		return render(request, 'cbayweb/reviewOrder.html',context)
	else:
		return redirect('/')

@login_required
def payOrder(request):
	if request.method == 'POST':
		order = get_object_or_404(Order, id = request.POST['order_id'])
		print(order.id)
		buyer_profile = get_object_or_404(Profile, user = order.buyer)
		print(buyer_profile.id)
		seller_profile = get_object_or_404(Profile, user = order.sale.seller)
		print(seller_profile.id)
		sale = order.sale
		new_item = Item(sale=sale, sold_price=sale.price, name=sale.name, description=sale.description, buyer=request.user, seller= sale.seller, list_time = sale.start_time)
		new_transaction = Transaction(item = new_item, quantity=order.quantity, price = order.price, seller = sale.seller, buyer=request.user)
		buyer_profile.account_balance = buyer_profile.account_balance - order.price
		seller_profile.account_balance = seller_profile.account_balance + order.price
		sale.quantity = sale.quantity - order.quantity
		sale.save()
		new_item.save()
		new_transaction.save()
		buyer_profile.save()
		seller_profile.save()
		order.delete()
		print('payment success')
		return redirect('/')
	else:
		return redirect('/')

@login_required
def postSale(request):
	if request.method == 'POST':
		sale = Sale(seller= get_object_or_404(User, id = request.user.id))
		form = SaleModelForm(request.POST,instance=sale)
		if form.is_valid():
			new_sale = form.save()
			print('New Item Saved')
			return redirect('/')
		else:
			print(form.errors)
			return render(request,'cbayweb/postItem.html',{'form':form})
	else:
		form = SaleModelForm()
	return render(request, 'cbayweb/postItem.html',{'form':form})

@login_required
def accountManage(request):
	return render(request, 'cbayweb/accountManage.html',{})