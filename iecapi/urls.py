from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API routes (coming from your app)
    path('api/', include('api.urls')),

    # 🔹 DRF Browsable API login/logout
    path('api-auth/', include('rest_framework.urls')),
]
