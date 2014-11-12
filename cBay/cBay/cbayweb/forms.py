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
		fields = ('name','description','quantity','start_time','end_time','price','item_pic')
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
		fields = ('name','description','start_time','end_time','start_price','item_pic','shipping_info')
	def clean(self):
		cleaned_data = super(AuctionModelForm, self).clean()
		name = cleaned_data.get("name")
		if name == '':
			self.add_error(None, 'Item Name Must Not Be Empty')