from django.contrib import admin
from django.urls import path
from verification import views  # Import the views from verification app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_signature, name='home'),  # Home page URL pointing to upload_signature view
]
