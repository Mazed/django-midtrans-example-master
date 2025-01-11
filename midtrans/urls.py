from django.contrib import admin
from django.urls import path
from midtrans.views import index, checkout, payment_success
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('checkout/<str:order_id>/', checkout, name='checkout'),
    path('payment-success/order_id=<str:order_id>&status_code=200&transaction_status=settlement', payment_success, name='payment_success'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)    
