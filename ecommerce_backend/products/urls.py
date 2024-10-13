from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, UserViewSet, OrderViewSet,login_view,signup_view 
from django.conf import settings
from django.conf.urls.static import static

# Create a router for your ViewSets
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'user', UserViewSet)
router.register(r'order', OrderViewSet)

urlpatterns = [
    # Include the router URLs for Product and User ViewSets
    path('api/', include(router.urls)),
    
    # Add a path for your custom login view
    path('api/signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
