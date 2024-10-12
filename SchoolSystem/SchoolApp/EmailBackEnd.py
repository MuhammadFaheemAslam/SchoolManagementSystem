from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
import logging  # For optional logging

# logger = logging.getLogger(__name__)  # Configure logging

class EmailBackEnd(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # Optional logging for failed login attempts
            # logger.warning(f"Login failed: No user found with email {username}")
            return None
        else:
            if user.check_password(password):
                return user
        return None
        
