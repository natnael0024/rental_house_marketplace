from .models import Message
from django import forms

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

        widgets = {
            'content': forms.TextInput(attrs={
            'placeholder': 'Type your message...',
            'class': 'w-full px-4 py-2 rounded border border-gray-300 focus:outline-none focus:border-cyan-500',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['autofocus'] = True