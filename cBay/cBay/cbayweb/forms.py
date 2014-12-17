from django import forms
from models import *

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'User Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'Password'}))
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'Confirm Password'}))
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if not password == confirm_password:
            self.add_error(None, 'password are not the same')

class LoginForm(forms.Form):
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'User Name'}))
	password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'Password'}))


class SaleModelForm(forms.ModelForm):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Item Name'}))
	description = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={'class':'form-control'}))
	shipping_info = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={'class':'form-control'}))
	class Meta:
		model = Sale
		fields = ('name','description','quantity','start_time','end_time','price','item_pic','category','shipping_info')
	def clean(self):
		cleaned_data = super(SaleModelForm, self).clean()
		name = cleaned_data.get("name")
		if name == '':
			self.add_error(None, 'Item Name Must Not Be Empty')


class AuctionModelForm(forms.ModelForm):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Item Name'}))
	description = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={'class':'form-control'}))
	shipping_info = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={'class':'form-control'}))
	class Meta:
		model = Auction
		fields = ('name','description','start_time','end_time','start_price','item_pic','shipping_info','category')
	def clean(self):
		cleaned_data = super(AuctionModelForm, self).clean()
		name = cleaned_data.get("name")
		if name == '':
			self.add_error(None, 'Item Name Must Not Be Empty')

class ProfileModelForm(forms.ModelForm):
	address = forms.CharField(max_length=256, widget=forms.Textarea(attrs={'class':'form-control'}))
	self_description = forms.CharField(max_length=256, widget=forms.Textarea(attrs={'class':'form-control'}))
	class Meta:
		model = Profile
		fields = ('id_picture', 'address', 'phone', 'self_description')

class CommentModelForm(forms.ModelForm):
	content = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={'class':'form-control'}))
	class Meta:
		model = Comment
		fields = ('title', 'content','rating')
	def clean(self):
		cleaned_data = super(CommentModelForm, self).clean()
		title = cleaned_data.get("title")
		if title == '':
			self.add_error(title, 'Comment Title Must Not Be Empty')


class MessageModelForm(forms.ModelForm):
	subject = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
	content = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={'class':'form-control'}))
	class Meta:
		model = Message
		fields = ('subject','content')
	def clean(self):
		cleaned_data = super(MessageModelForm, self).clean()
		subject = cleaned_data.get("subject")
		if subject == '':
			self.add_error(subject, 'Subject Must Not Be Empty')

