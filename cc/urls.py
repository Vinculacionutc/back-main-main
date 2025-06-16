from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, ProductoViewSet, EmpresaViewSet,
    ServicioViewSet, TestimonioViewSet, EquipoViewSet,
    NoticiaViewSet, ContactoViewSet, SocioViewSet,
    JobApplicationViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'empresas', EmpresaViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'testimonios', TestimonioViewSet)
router.register(r'equipo', EquipoViewSet)
router.register(r'noticias', NoticiaViewSet)
router.register(r'contacto', ContactoViewSet)
router.register(r'socios', SocioViewSet)
router.register(r'job-applications', JobApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

