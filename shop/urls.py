from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    IndexView,
    ProductListView,
    ProductDetailView,
    ServiceListView,
    ServiceDetailView,
    ContactView,
    ProductCreateView,
    ServiceCreateView,
    ProductSearchView,
    LoginView,
    LogoutView,
    RegisterView,
    ProfileView,
    EditProfileView,
    ProductDeleteView,
    AboutView,
    PagesListView,
    ProductEditView,
    ServiceDeleteView,
    ServiceEditView,
    ClientListView,
    ClientCreateView,
    ClientEditView,
    ClientDeleteView
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('services/', ServiceListView.as_view(), name='services'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('create_product/', ProductCreateView.as_view(), name='create_product'),
    path('create_service/', ServiceCreateView.as_view(), name='create_service'),
    path('search/', ProductSearchView.as_view(), name='search_products'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('about/', AboutView.as_view(), name='about'),
    path('pages/', PagesListView.as_view(), name='pages'),
    path('edit_product/<int:pk>/', ProductEditView.as_view(), name='edit_product'),
    path('services/edit/<int:pk>/', ServiceEditView.as_view(), name='edit_service'),
    path('services/delete/<int:pk>/', ServiceDeleteView.as_view(), name='delete_service'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/create/', ClientCreateView.as_view(), name='create_client'),
    path('clients/edit/<int:pk>/', ClientEditView.as_view(), name='edit_client'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)