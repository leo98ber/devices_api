from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models



class User(AbstractUser):
    """
    Default custom user model for device_api.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    email = EmailField(_("email address"), unique=True)

    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']


    # def get_absolute_url(self) -> str:
    #     """Get URL for user's detail view.
    #
    #     Returns:
    #         str: URL for user detail.
    #
    #     """
    #     return reverse("users:detail", kwargs={"pk": self.id})

    def __str__(self):
        return self.username
