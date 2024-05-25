from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','password']

        widgets = {
            'first_name': forms.TextInput(attrs={
            'placeholder': 'Abebe',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            }),
            'last_name': forms.TextInput(attrs={
            'placeholder': 'Kebede',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            }),
            'email': forms.TextInput(attrs={
            'placeholder': 'abekebe@example.com',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            }),
            'password': forms.PasswordInput(attrs={
            'placeholder': '********',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            }),
        }

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','password']
        widgets = {
            'email': forms.TextInput(attrs={
            'placeholder': 'abekebe@example.com',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            }),
            'password': forms.PasswordInput(attrs={
            'placeholder': '********',
            'class': 'p-6 rounded bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            }),
        }