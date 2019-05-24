from django import forms

class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Speak', 'name': 'userInput', 'id': 'transcribed', 'class':'form-input'}))