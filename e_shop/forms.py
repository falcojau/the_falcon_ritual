from django import forms
from django.contrib.auth.models import User

# Form to register Users
class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password"
        ]
    
    # function to save users data
    def save(self):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data["password"])
        user.save()
        # A profile will be created
        from e_shop.models import Order
        Order.objects.create(user=user)
        return user


# function for login
class LoginUserForm(forms.Form):
    username = forms.CharField(label='User')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


# Form for Contact
class ContactForm(forms.Form):
    first_name = forms.CharField(label="Name", max_length=100)
    last_name = forms.CharField(label="Last Name", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Your message", widget=forms.Textarea)