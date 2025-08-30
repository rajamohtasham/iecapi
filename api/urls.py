
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    MeetingViewSet,
    VideoRoomViewSet,
    DocumentViewSet,
    DocumentSignatureView,
    WalletView,
    TransactionViewSet,
)

router = DefaultRouter()
router.register(r"meetings", MeetingViewSet, basename="meeting")
router.register(r"video-rooms", VideoRoomViewSet, basename="video-room")
router.register(r"documents", DocumentViewSet, basename="document")
router.register(r"transactions", TransactionViewSet, basename="transaction")

urlpatterns = [
    # Auth & Profile
    path("auth/register/", RegisterView.as_view(), name="auth_register"),
    path("auth/login/",    LoginView.as_view(),    name="auth_login"),
    path("auth/refresh/",  TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/profile/",  ProfileView.as_view(),  name="auth_profile"),

    # Wallet
    path("wallet/", WalletView.as_view(), name="wallet"),

    # Document signing
    path("documents/<int:doc_id>/sign/", DocumentSignatureView.as_view(), name="document_sign"),

    # ViewSets (meetings, video-rooms, documents, transactions)
    path("", include(router.urls)),
]
