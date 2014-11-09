from django import forms

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