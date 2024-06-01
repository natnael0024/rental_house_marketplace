from .models import Message
from django import forms

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

        widgets = {
            'content': forms.TextInput(attrs={
            'placeholder': 'Type your message...',
            'class': 'outline-cyan-100 w-full px-4 py-2 rounded border border-gray-300 outline-none outline-0 focus:border-cyan-50',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['autofocus'] = True