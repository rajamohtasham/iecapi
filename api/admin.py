from django.contrib import admin
from .models import (
    User,
    Meeting,
    VideoRoom,
    Document,
    DocumentSignature,
    Wallet,
    Transaction,
)

# -------------------------
# Custom User Admin
# -------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role", "is_active", "date_joined")
    list_filter = ("role", "is_active", "date_joined")
    search_fields = ("username", "email")


# -------------------------
# Meeting & VideoRoom
# -------------------------
@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "organizer", "start_time", "end_time", "status")
    list_filter = ("status", "start_time")
    search_fields = ("title", "organizer__username")


@admin.register(VideoRoom)
class VideoRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room_id", "meeting", "created_at")
    search_fields = ("room_id", "meeting__title")


# -------------------------
# Documents & Signatures
# -------------------------
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "version", "status", "uploaded_at")
    list_filter = ("status", "uploaded_at")
    search_fields = ("title", "owner__username")


@admin.register(DocumentSignature)
class DocumentSignatureAdmin(admin.ModelAdmin):
    list_display = ("id", "document", "signed_by", "signed_at")
    list_filter = ("signed_at",)
    search_fields = ("document__title", "signed_by__username")


# -------------------------
# Wallet & Transactions
# -------------------------
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "balance")
    search_fields = ("user__username",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "transaction_type", "amount", "status", "sender", "receiver", "created_at")
    list_filter = ("transaction_type", "status", "created_at")
    search_fields = ("sender__username", "receiver__username")
