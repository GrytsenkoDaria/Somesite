from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from app1 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # include включает все сылки с того что в скобочках ('')
    path('', views.ProductListView.as_view(), name='home'),
    path('search/', views.Search.as_view(), name='search'),
    path('detail/<int:pk>', views.HomeDetailView.as_view(), name='detail'),
    path('profile/detail/<int:pk>', views.HomeDetailView.as_view(), name='detail'),
    path('edit-page/', views.ProductCreateView.as_view(), name='edit_page'),
    path('update-page/<int:pk>', views.ProductUpdateView.as_view(), name='update_page'),
    path('delete-page/<int:pk>', views.ProductDeleteView.as_view(), name='delete_page'),
    path('profile/', views.ProfileView.as_view(), name='profile_page'),
    path('profile/products/', views.ProfileProductsView.as_view(), name='profile_products')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
