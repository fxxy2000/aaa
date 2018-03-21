from django import forms
 
class UserForm(forms.Form):
    account = forms.CharField(widget=forms.EmailInput(attrs={'size': 25}), label='Account')
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'size': 25}), label='Password')

    class Meta:
        fields = ('account', 'pwd',)

class SearchForm(forms.Form):
	keyword = forms.CharField()

class PinForm(forms.Form):
    pin = forms.CharField(widget=forms.TextInput(attrs={'size': 25}), label='Pin')

    class Meta:
        fields = ('pin')