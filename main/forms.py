from django import forms
from .models import Profile,Review

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture','phone_number','address']
        widgets = {
            "profile_picture":forms.FileInput(attrs={'class':"form-control",}),
            'phone_number':forms.TextInput(attrs={'class':"form-control",'placeholder':"enter your phonenumber:"}),
            'address':forms.TextInput(attrs={'class':"form-control",'placeholder':"enter your address:"}),
            
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','comment']
        widgets = {
            'rating': forms.Select(choices=[(i,i) for i in range(1,6)],attrs={'class':"form-control"}),
            'comment': forms.Textarea(attrs={'class':"form-control",'rows':4}),
        }

