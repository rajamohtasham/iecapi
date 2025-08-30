from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Meeting, VideoRoom, Document, Transaction, Wallet, DocumentSignature
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    MeetingSerializer,
    VideoRoomSerializer,
    DocumentSerializer,
    TransactionSerializer,
    WalletSerializer,
)

User = get_user_model()

# ---------------- AUTH ----------------

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ---------------- WALLET ----------------

class WalletView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


# ---------------- DOCUMENT SIGNING  ✅ FIXED ----------------

class DocumentSignatureView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, doc_id):
        try:
            document = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=404)

        # Prevent duplicate sign by the same user
        if DocumentSignature.objects.filter(document=document, signed_by=request.user).exists():
            return Response({"error": "You already signed this document."}, status=400)

        DocumentSignature.objects.create(document=document, signed_by=request.user)

        # Optionally mark document as signed
        if document.status != "signed":
            document.status = "signed"
            document.save(update_fields=["status"])

        return Response({"status": f"Document '{document.title}' signed"})


# ---------------- PERMISSION CLASSES ----------------

class ReadOnlyOrAuthenticated(permissions.BasePermission):
    """
    - GET, HEAD, OPTIONS: AllowAny (public)
    - POST, PUT, PATCH, DELETE: IsAuthenticated
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


# ---------------- VIEWSETS ----------------

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [ReadOnlyOrAuthenticated]


class VideoRoomViewSet(viewsets.ModelViewSet):
    queryset = VideoRoom.objects.all()
    serializer_class = VideoRoomSerializer
    permission_classes = [ReadOnlyOrAuthenticated]


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [ReadOnlyOrAuthenticated]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [ReadOnlyOrAuthenticated]
