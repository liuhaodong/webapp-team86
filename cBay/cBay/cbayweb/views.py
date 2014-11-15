from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core import serializers
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core import serializers
from forms import *
from mimetypes import guess_type
from django.utils import timezone
import json
import json as simplejson

# Create your views here.
@login_required
def homepage(request):
	sales = Sale.objects.all()
	print(len(sales))
	return render(request, 'cbayweb/homepage.html',{'sales': sales})

@login_required
def viewSale(request, sale_id):
	sale = get_object_or_404(Sale, id=sale_id)
	context = {}
	context['sale'] = sale 
	comments = []
	context['comments'] = comments
	return render(request, 'cbayweb/viewSale.html',context)

@login_required
def viewAuction(request, auction_id):
	auction = get_object_or_404(Auction, id=auction_id)
	context = {}
	context['auction'] = auction
	bids = Bid.objects.filter(auction = auction).order_by('-bid_price')
	if len(bids) == 0:
		max_bid_price = auction.start_price
	else:
		max_bid_price = bids[0].bid_price
	context['max_bid_price'] = max_bid_price
	context['bids'] = bids
	comments = []
	context['comments'] = comments
	return render(request, 'cbayweb/viewAuction.html',context)

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
		new_order = Order(buyer = request.user, sale=my_sale, quantity = request.POST['sale_quantity'])
		new_order.price = (float)(new_order.sale.price) * (float)(new_order.quantity)
		new_order.save()
		context['order'] = new_order
		return render(request, 'cbayweb/reviewOrder.html',context)
	else:
		return redirect('/')

@login_required
def placeBid(request):
	if request.method == 'POST':
		context = {}
		my_auction=get_object_or_404(Auction, id=request.POST['auction_id'])
		if (float)(request.POST['bid_price']) > my_auction.current_max_bid and timezone.now() < my_auction.end_time:
			my_auction.current_max_bid = (float)(request.POST['bid_price'])
			my_auction.save()
			new_bid = Bid(bidder = request.user, auction=my_auction, bid_price=request.POST['bid_price'])
			new_bid.save()
			return redirect('viewAuction', auction_id=my_auction.id)
		else:
			return redirect('viewAuction', auction_id=my_auction.id)
		print('new bid is saved')
	else:
		return redirect('/')

@login_required
def payOrder(request):
	if request.method == 'POST':
		order = get_object_or_404(Order, id = request.POST['order_id'])
		buyer_profile = get_object_or_404(Profile, user = order.buyer)
		if order.sale:
			seller_profile = get_object_or_404(Profile, user = order.sale.seller)
			sale = order.sale
			new_transaction = Transaction(sale=sale, quantity=order.quantity, price = order.price, seller = sale.seller, buyer=request.user)
			buyer_profile.account_balance = buyer_profile.account_balance - order.price
			buyer_profile.save()
			print(buyer_profile.account_balance)
			seller_profile.account_balance = seller_profile.account_balance + order.price
			seller_profile.save()
			print(seller_profile.account_balance)
			sale.quantity = sale.quantity - order.quantity
			sale.save()
			new_transaction.save()		
			order.delete()
			print('payment success')
		else:
			seller_profile = get_object_or_404(Profile, user = order.auction.seller)
			auction = order.auction
			new_transaction = Transaction(auction=auction, quantity=order.quantity, price = order.price, seller = auction.seller, buyer=request.user)
			buyer_profile.account_balance = buyer_profile.account_balance - order.price
			buyer_profile.save()
			seller_profile.account_balance = seller_profile.account_balance + order.price
			seller_profile.save()
			auction.is_paid = True
			auction.save()
			new_transaction.save()		
			order.delete()
			print('payment success')
		return redirect('/')
	else:
		return redirect('/')

@login_required
def postSale(request):
	if request.method == 'POST':
		sale = Sale(seller= get_object_or_404(User, id = request.user.id))
		form = SaleModelForm(request.POST, request.FILES, instance=sale)
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
def postAuction(request):
	if request.method == 'POST':
		auction = Auction(seller= get_object_or_404(User, id = request.user.id))
		form = AuctionModelForm(request.POST, request.FILES, instance=auction)
		if form.is_valid():
			new_auction = form.save()
			print('New Auction Saved')
			return redirect('/')
		else:
			print(form.errors)
			return render(request,'cbayweb/postAuction.html',{'form':form})
	else:
		form = AuctionModelForm()
	return render(request, 'cbayweb/postAuction.html',{'form':form})

@login_required
def accountManage(request):
	context={}
	current_user = get_object_or_404(User, id=request.user.id)
	user_profile = get_object_or_404(Profile, user=current_user)
	transactions = Transaction.objects.filter(buyer = request.user)
	sales = Sale.objects.filter(seller = request.user)
	context['user'] = current_user
	context['profile'] = user_profile
	context['transactions'] = transactions 
	context['sales'] = sales
	return render(request, 'cbayweb/accountManage.html',context)

@login_required
def get_item_picture(request, sale_id):
	sale = get_object_or_404(Sale, id=sale_id)
	if not sale.item_pic:
		raise Http404
	content_type = guess_type(sale.item_pic.name)
	return HttpResponse(sale.item_pic, content_type=content_type)

@login_required
def get_auction_picture(request, auction_id):
	auction = get_object_or_404(Auction, id=auction_id)
	if not auction.item_pic:
		raise Http404
	content_type = guess_type(auction.item_pic.name)
	return HttpResponse(auction.item_pic, content_type=content_type)	

@login_required
def check_auction(request, auction_id):
	auction = get_object_or_404(Auction, id = auction_id)
	auction_json = {}
	auction_json['is_ended'] = auction.is_ended
	auction_json['current_max_bid'] = auction.current_max_bid
	auction_json['winner_name'] = auction.winner.username
	auction_json['winner_id'] = auction.winner.id
	return HttpResponse(json.dumps(auction_json), content_type = "application/json")

@login_required
def buy_auction(request):
	if request.method == 'POST':
		context = {}
		auction = get_object_or_404(Auction, id = request.POST['auction_id'])
		if request.user == auction.winner:
			new_order = Order(buyer = request.user, auction=auction, quantity = 1)
			new_order.price = auction.current_max_bid;
			new_order.save()
			context['order'] = new_order
			return render(request, 'cbayweb/reviewOrder.html',context)
		else:
			return redirect('/')
	else:
		return redirect('/')
