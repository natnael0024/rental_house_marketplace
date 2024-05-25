from django import forms
from .models import Listing, ListingMedia


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title','desc','price','rooms','bedrooms','bathrooms','square_metre','city','sub_city','area','phone_number1','phone_number2']
        
        widgets = {
            'title': forms.TextInput(attrs={
            'placeholder': 'Luxury Apartment',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-[25rem] p-2.5 ',
            }),
            'desc': forms.Textarea(attrs={
            'placeholder': 'bla bla',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-[25rem] p-2.5 ',
            }),
            'price': forms.TextInput(attrs={
            'placeholder': '20000',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-[25rem] p-2.5 ',
            }),
            'rooms': forms.TextInput(attrs={
            'placeholder': '4',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-[25rem] p-2.5 ',
            }),
            'bedrooms': forms.TextInput(attrs={
            'placeholder': '2',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-[25rem] p-2.5 ',
            }),
            'bathrooms': forms.TextInput(attrs={
            'placeholder': '1',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-[25rem] p-2.5 ',
            }),
            'square_metre': forms.TextInput(attrs={
            'placeholder': '145',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-[25rem] p-2.5 ',
            }),
            'city': forms.TextInput(attrs={
            'placeholder': 'Addis Ababa',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-[25rem] p-2.5 ',
            }),
            'sub_city': forms.TextInput(attrs={
            'placeholder': 'Kirkos',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-[25rem] p-2.5 ',
            }),
            'area': forms.TextInput(attrs={
            'placeholder': 'Kazanchis',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-[25rem] p-2.5 ',
            }),
            'phone_number1': forms.TextInput(attrs={
            'placeholder': '091234___',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-[25rem] p-2.5 ',
            }),
            'phone_number2': forms.TextInput(attrs={
            'placeholder': '094321___',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-cyan-500 focus:border-cyan-500 block w-[25rem] p-2.5 ',
            }),
            
            
            

        }