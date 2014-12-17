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
from django.db.models import Q
import json
import json as simplejson


# Create your views here.
@login_required
def homepage(request):
	sales = Sale.objects.all()
	categories = []
	for item in CATEGORY_CHOICES:
		categories.append(item[0])
	auctions = Auction.objects.filter(is_ended = False)
	return render(request, 'cbayweb/homepage.html',{'sales': sales,'categories':categories,'auctions': auctions})

@login_required
def viewSale(request, sale_id):
	sale = get_object_or_404(Sale, id=sale_id)
	context = {}
	context['sale'] = sale 
	comments = Comment.objects.filter(sale = sale)
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
	comments = Comment.objects.filter(auction = auction)
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
def editProfile(request):
	if request.method == 'POST':
		form = ProfileModelForm(request.POST, request.FILES)
		if form.is_valid():
			user_profile = Profile.objects.get(user = request.user)
			user_profile.id_picture = form.cleaned_data['id_picture']
			user_profile.address = form.cleaned_data['address']
			user_profile.phone = form.cleaned_data['phone']
			user_profile.self_description = form.cleaned_data['self_description']
			user_profile.save()
			return redirect('accountManage')
		else:
			return render(request, 'cbayweb/editProfile.html', {'form': form})
	else:
		form = ProfileModelForm()
		return render(request, 'cbayweb/editProfile.html', {'form': form})

@login_required
def reviewOrder(request):
	return render(request, 'cbayweb/reviewOrder.html',{})


@login_required
def placeOrder(request):
	if request.method == 'POST':
		context = {}
		my_sale=get_object_or_404(Sale, id=request.POST['sale_id'])
		new_order = Order(buyer = request.user, sale=my_sale, quantity = request.POST['sale_quantity'])
		buyer_profile = get_object_or_404(Profile, user = request.user)
		new_order.shipping_address = buyer_profile.address
		new_order.price = (float)(new_order.sale.price) * (float)(new_order.quantity)
		new_order.save()
		context['order'] = new_order
		context['buyer_profile'] = buyer_profile
		return render(request, 'cbayweb/reviewOrder.html',context)
	else:
		return redirect('/')

@login_required
def addComment(request):
	if request.method == 'POST':
		if 'sale_id' in request.POST:
			sale = get_object_or_404(Sale, id= request.POST['sale_id'])
			comment = Comment(buyer = get_object_or_404(User, id = request.user.id), seller = sale.seller, sale = sale)
			form = CommentModelForm(request.POST, instance=comment)
			if form.is_valid():
				new_comment = form.save()
				print('New Comment Saved')
				return redirect('viewSale', request.POST['sale_id'])
		elif 'auction_id' in request.POST:
			print(request.POST['auction_id'])
			auction = get_object_or_404(Auction, id = request.POST['auction_id'])
			comment = Comment(buyer = get_object_or_404(User, id = request.user.id), seller = auction.seller, auction = auction)
			form = CommentModelForm(request.POST, instance=comment)
			if form.is_valid():
				new_comment = form.save()
				return redirect('viewAuction', request.POST['auction_id'])
		else:
			return redirect('/')


	else:
		sale_id = request.GET.get('sale_id', False)
		auction_id = request.GET.get('auction_id', False)
		print(auction_id)
		form = CommentModelForm()
		if sale_id:
			sale = get_object_or_404(Sale, id = sale_id)
			return render(request, 'cbayweb/addComment.html', {'sale': sale, 'form':form})
		elif auction_id:
			print(auction_id)
			auction = get_object_or_404(Auction, id= auction_id)
			return render(request, 'cbayweb/addComment.html', {'auction': auction, 'form':form})
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
			new_transaction.is_finshied = False
			sale.quantity = sale.quantity - order.quantity
			sale.sold_num = sale.sold_num + order.quantity
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
			new_transaction.is_finshied = False
			auction.is_paid = True
			auction.save()
			new_transaction.save()		
			order.delete()
		return redirect('/')
	else:
		return redirect('/')

@login_required
def confirmDelivery(request):
	if request.method == 'POST':
		if 'transaction_id' in request.POST:
			unfinished_transaction = get_object_or_404(Transaction, id = request.POST['transaction_id'], buyer = request.user)
			seller_profile = get_object_or_404(Profile, user = unfinished_transaction.seller)
			seller_profile.account_balance = seller_profile.account_balance + unfinished_transaction.price
			seller_profile.save()
			unfinished_transaction.is_finished = True
			unfinished_transaction.save()
			return redirect('accountManage')
		else:
			return redirect('accountManage')
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
	auctions = Auction.objects.filter(seller = request.user)
	sales = Sale.objects.filter(seller = request.user)
	won_auctions = Auction.objects.filter(winner = request.user)
	messages = Message.objects.filter(recipient = request.user)
	context['user'] = current_user
	context['profile'] = user_profile
	context['transactions'] = transactions 
	context['sales'] = sales
	context['auctions'] = auctions
	context['won_auctions'] = won_auctions
	context['messages'] = messages
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
def id_picture(request, id):
	profile = get_object_or_404(Profile, id=id)
	if not profile.id_picture:
		raise Http404
	content_type = guess_type(profile.id_picture.name)
	return HttpResponse(profile.id_picture, content_type=content_type)

@login_required
def check_auction(request, auction_id):
	auction = get_object_or_404(Auction, id = auction_id)
	auction_json = {}
	auction_json['is_ended'] = auction.is_ended
	auction_json['current_max_bid'] = auction.current_max_bid
	if auction.is_ended:
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
			buyer_profile = get_object_or_404(Profile, user = request.user)
			new_order.shipping_address = buyer_profile.address
			new_order.price = auction.current_max_bid;
			new_order.save()
			context['order'] = new_order
			context['buyer_profile'] = buyer_profile
			return render(request, 'cbayweb/reviewOrder.html',context)
		else:
			return redirect('/')
	else:
		return redirect('/')

@login_required
def get_items_by_category(request, category):
	sales_data = serializers.serialize('json', Sale.objects.filter(category = category), fields=('name','id','seller','price','start_time','end_time'))
	auctions_data = serializers.serialize('json', Auction.objects.filter(category = category), fields=('name','id','seller','current_max_bid','start_time', 'end_time'))
	data = {'sales_data':  sales_data, 'auctions_data': auctions_data}
	return HttpResponse(json.dumps(data), content_type = "application/json")

@login_required
def searchItem(request):

	keyword = request.GET.get('keyword', False)
	category = request.GET.get('category', False)
	print(keyword)
	print(category)
	categories = []
	for item in CATEGORY_CHOICES:
		categories.append(item[0])

	if keyword =='':
		sales = Sale.objects.all()
		auctions = Auction.objects.all()
		return render(request, 'cbayweb/searchResult.html',{'sales': sales,'categories':categories,'auctions': auctions, 'keyword':keyword })
	elif category == '':
		print('category is none')
		sales = Sale.objects.filter( Q(name__icontains= keyword) | Q(description__icontains=keyword) | Q(seller__username__icontains = keyword))
		auctions = Auction.objects.filter(Q(name__icontains= keyword) | Q(description__icontains=keyword) | Q(seller__username__icontains = keyword))
		return render(request, 'cbayweb/searchResult.html',{'sales': sales,'categories':categories,'auctions': auctions, 'keyword':keyword })
	else:
		sales = Sale.objects.filter( Q(name__icontains= keyword) | Q(description__icontains=keyword) | Q(seller__username__icontains = keyword) , category = category)
		auctions = Auction.objects.filter(Q(name__icontains= keyword) | Q(description__icontains=keyword) | Q(seller__username__icontains = keyword) , category = category)
		return render(request, 'cbayweb/searchResult.html',{'sales': sales,'categories':categories,'auctions': auctions, 'keyword': keyword})


@login_required
def sendMessage(request):
	if request.method == 'POST':
		if 'recipient_id' in request.POST:
			recipient = get_object_or_404(User, id= request.POST['recipient_id'])
		elif 'recipient_name' in request.POST:
			recipient = get_object_or_404(User, username = request.POST['recipient_name'])
		else:
			return redirect('/')
		message = Message(sender = get_object_or_404(User, id = request.user.id), recipient = recipient, subject = request.POST['subject'], content = request.POST['content'])
		form = MessageModelForm(request.POST, instance=message)
		if form.is_valid():
			new_message = form.save()
			print('New Message Saved')
			print new_message.subject
			print new_message.content
			return redirect('/')
	else:
		recipient_id = request.GET.get('recipient_id', False)
		form = MessageModelForm()
		if recipient_id:
			recipient = get_object_or_404(User, id = recipient_id)
			return render(request, 'cbayweb/sendMessage.html', {'recipient': recipient, 'form':form})
		else:
			return render(request, 'cbayweb/sendMessage.html', {'recipient': '', 'form':form})


@login_required
def viewMessage(request):
	message_id = request.GET.get('message_id', False)
	if message_id:
		message = get_object_or_404(Message, id = message_id)
		return render(request, 'cbayweb/viewMessage.html', {'message': message})
	else:
		raise 404



