from .models import UserProfile
from django import forms
from .models import Review, CommunityMember
from .models import Club

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', initial='')
    username = forms.CharField(max_length=30, initial='')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    IDENTITY_CHOICES = [
        ('player', 'Player'),
        ('game_dev', 'Game Developer'),
        ('club_mgr', 'Club Manager'),
        ('admin', 'Administrator'),
    ]
    identity = forms.ChoiceField(choices=IDENTITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}), required=False)

    GENRE_CHOICES = [
        ('strategy', 'Strategy'),
        ('party', 'Party'),
        ('cooperative', 'Cooperative'),
        ('deck_building', 'Deck Building'),
        ('worker_placement', 'Worker Placement'),
        ('thematic', 'Thematic'),
    ]
    favorite_genre = forms.ChoiceField(choices=GENRE_CHOICES, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}), required=False, initial='')
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2', 'identity', 'favorite_genre')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class JoinClubForm(forms.Form):
    club = forms.ModelChoiceField(queryset=Club.objects.all())

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class JoinCommunityForm(forms.ModelForm):
    class Meta:
        model = CommunityMember
        fields = []

