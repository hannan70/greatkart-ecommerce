
from django import forms

from accounts.models import Account


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['first_name'].widget.attrs['placeholder'] = "Enter First Name"
    #
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-control'


    # custom validation for mobile
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if len(phone_number) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return phone_number

    # custom validation for password and confirm password
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class" : "form-control", "placeholder": "Enter First Name"}),
        error_messages= {"required": "First Name is required !"},
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Last Name"}),
        error_messages={"required": "Last Name is required !"},
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Your Email"}),
        error_messages={"required": "Email is required !"},
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Your Number"}),
        error_messages={"required": "Phone Number is required !"},
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={ 'class': "form-control", "placeholder": "Enter Password"}),
        error_messages={"required": "Password is required !"},

    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={ 'class': "form-control", "placeholder": "Repeat Password"}),
        error_messages={"required": "Confirm Password is required !"},
    )

