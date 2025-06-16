from django.urls import path
from .views import solicitud_socio
from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet

urlpatterns = [
    path('api/socios/', solicitud_socio, name='solicitud-socio'),
]

router = DefaultRouter()
router.register(r'job-applications', JobApplicationViewSet)

