from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'User Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'Password'}))
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'Confirm Password'}))

class LoginForm(forms.Form):
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'User Name'}))
	password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'Password'}))