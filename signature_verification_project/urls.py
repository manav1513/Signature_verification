from django.contrib import admin
from django.urls import path, include
from verification import views  # Import the views from verification app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_signature, name='home'),  # Set the homepage to the upload_signature view
    path('verification/', include('verification.urls')),  # Keep this for future verification URLs
]
