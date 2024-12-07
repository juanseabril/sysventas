from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ProductoViewSet, VentaViewSet, DetalleVentaViewSet, register_user, LoginView
from django.urls import path

router = DefaultRouter()
router.register('clientes', ClienteViewSet)
router.register('productos', ProductoViewSet)
router.register('ventas', VentaViewSet)
router.register('detalles-venta', DetalleVentaViewSet)

urlpatterns = router.urls + [
    path('register/', register_user, name='register_user'),
    path('login/', LoginView.as_view(), name='login'),
]
