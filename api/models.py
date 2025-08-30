from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# -------------------------
# 1. Custom User Model
# -------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ("investor", "Investor"),
        ("entrepreneur", "Entrepreneur"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    portfolio = models.TextField(blank=True, null=True)
    preferences = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# -------------------------
# 2. Meetings
# -------------------------
class Meeting(models.Model):
    STATUS_CHOICES = (
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    organizer = models.ForeignKey(User, related_name="organized_meetings", on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name="meetings")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")

    def __str__(self):
        return f"{self.title} ({self.status})"


# -------------------------
# 3. Video Call Rooms
# -------------------------
class VideoRoom(models.Model):
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE, related_name="video_room")
    room_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Room {self.room_id} for {self.meeting.title}"


# -------------------------
# 4. Documents & Signatures
# -------------------------
class Document(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("reviewed", "Reviewed"),
        ("signed", "Signed"),
    )
    owner = models.ForeignKey(User, related_name="documents", on_delete=models.CASCADE)
    file = models.FileField(upload_to="documents/")
    title = models.CharField(max_length=255)
    version = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} v{self.version} ({self.status})"


class DocumentSignature(models.Model):
    document = models.ForeignKey(Document, related_name="signatures", on_delete=models.CASCADE)
    signed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    signed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.signed_by.username} signed {self.document.title}"


# -------------------------
# 5. Payments & Transactions
# -------------------------
class Wallet(models.Model):
    user = models.OneToOneField(User, related_name="wallet", on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} Wallet - Balance: {self.balance}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("deposit", "Deposit"),
        ("withdraw", "Withdraw"),
        ("transfer", "Transfer"),
    )
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )
    sender = models.ForeignKey(User, related_name="sent_transactions", on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.ForeignKey(User, related_name="received_transactions", on_delete=models.SET_NULL, null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} ({self.status})"
