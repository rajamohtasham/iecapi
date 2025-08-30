from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Meeting, VideoRoom, Document, DocumentSignature, Wallet, Transaction
from django.contrib.auth import authenticate

User = get_user_model()

# -------------------------
# 1. User & Profile
# -------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "bio", "portfolio", "preferences"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            role=validated_data["role"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


# -------------------------
# 2. Meetings & Video Rooms
# -------------------------
class MeetingSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = ["id", "title", "description", "organizer", "participants", "start_time", "end_time", "status"]


class MeetingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ["id", "title", "description", "start_time", "end_time", "participants"]


class VideoRoomSerializer(serializers.ModelSerializer):
    meeting = MeetingSerializer(read_only=True)

    class Meta:
        model = VideoRoom
        fields = ["id", "room_id", "meeting", "created_at"]


# -------------------------
# 3. Documents & Signatures
# -------------------------
class DocumentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ["id", "owner", "file", "title", "version", "status", "uploaded_at"]


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "file", "title"]


class DocumentSignatureSerializer(serializers.ModelSerializer):
    signed_by = UserSerializer(read_only=True)

    class Meta:
        model = DocumentSignature
        fields = ["id", "document", "signed_by", "signed_at"]


# -------------------------
# 4. Wallet & Transactions
# -------------------------
class WalletSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = ["id", "user", "balance"]


class TransactionSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "sender", "receiver", "transaction_type", "amount", "status", "created_at"]


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "receiver", "amount"]


# -------------------------
# 5. Auth (Login)  ✅ FIXED
# -------------------------
class LoginSerializer(serializers.Serializer):
    # Accept either username or email
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get("username") or data.get("email")
        password = data.get("password")
        if not identifier or not password:
            raise serializers.ValidationError("Username/email and password are required.")

        # Find user by email if email is supplied
        user = None
        if data.get("email"):
            try:
                user_obj = User.objects.get(email=data["email"])
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(username=data["username"], password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        data["user"] = user
        return data
