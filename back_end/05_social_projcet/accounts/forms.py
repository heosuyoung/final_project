from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields  # 기본 username, password1, password2 포함

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
