from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Model representing a user account."""

    def __str__(self):
        """String representation of user model."""
        return self.get_full_name()
