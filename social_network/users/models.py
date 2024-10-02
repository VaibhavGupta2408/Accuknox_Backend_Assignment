from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from cryptography.fernet import Fernet
from django.db import models
from django.conf import settings
from django.db.models import Q

# Generate and store a key for encryption
key = Fernet.generate_key()
cipher = Fernet(key)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    encrypted_email = models.BinaryField(blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Encrypt the email before saving
        if self.email:
            self.encrypted_email = cipher.encrypt(self.email.encode())
        super().save(*args, **kwargs)

    def get_decrypted_email(self):
        if self.encrypted_email:
            return cipher.decrypt(self.encrypted_email).decode()
        return None

    @property
    def friends(self):
        # Get the accepted friend requests where the current user is either the sender or receiver
        accepted_requests_as_sender = FriendRequest.objects.filter(sender=self, status='accepted')
        accepted_requests_as_receiver = FriendRequest.objects.filter(receiver=self, status='accepted')

        # Extract the friends' user objects
        friends_as_sender = [req.receiver for req in accepted_requests_as_sender]
        friends_as_receiver = [req.sender for req in accepted_requests_as_receiver]

        # Combine the friends lists
        return friends_as_sender + friends_as_receiver



# Friend Request Model
class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.email} -> {self.receiver.email} ({self.status})'


class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=255)  # e.g., 'friend_request_sent', 'friend_request_accepted'
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)  # Additional details about the activity

    def __str__(self):
        return f'{self.user.email} - {self.activity_type}'
