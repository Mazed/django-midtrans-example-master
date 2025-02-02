from django.contrib import admin
from django.urls import re_path, path
from midtrans.views import index, checkout, payment_success
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^checkout/(?P<order_id>[^/]+)/$', checkout, name='checkout'),
    re_path(r'^payment_success/$', payment_success, name='payment_success'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
