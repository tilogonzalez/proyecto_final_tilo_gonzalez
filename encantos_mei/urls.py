from django.contrib import admin
from django.urls import include, path
from shop.views import IndexView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("shop/", include("shop.urls")),
    path("admin/", admin.site.urls),
    path('messages/', include('shop_messages.urls')),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
