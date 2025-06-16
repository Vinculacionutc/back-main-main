from django.shortcuts import render
from .models import *
from .serializers import *
# Create your views here.
# views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import permissions

class IsCompanyUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Verificar si el usuario está autenticado y tiene acceso a la empresa
        if not request.user.is_authenticated:
            return False
            
        try:
            empresa_usuario = EmpresaUsuario.objects.get(usuario=request.user)
            return obj.empresa == empresa_usuario.empresa
        except EmpresaUsuario.DoesNotExist:
            return False

class EmpresaUsuarioViewSet(viewsets.ModelViewSet):
    queryset = EmpresaUsuario.objects.all()
    serializer_class = EmpresaUsuarioSerializer
    permission_classes = [permissions.IsAdminUser]  # Solo los administradores pueden crear usuarios de empresa

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']

class SocioViewSet(viewsets.ModelViewSet):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer

class RedSocialViewSet(viewsets.ModelViewSet):
    queryset = RedSocial.objects.all()
    serializer_class = RedSocialSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(activo=True)
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categoria', 'empresa']
    search_fields = ['nombre', 'descripcion']
    permission_classes = [IsCompanyUserOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            try:
                empresa_usuario = EmpresaUsuario.objects.get(usuario=self.request.user)
                return queryset.filter(empresa=empresa_usuario.empresa)
            except EmpresaUsuario.DoesNotExist:
                return Producto.objects.none()
        return queryset

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.filter(activa=True)
    serializer_class = EmpresaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categoria']
    search_fields = ['nombre', 'descripcion']

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.filter(activo=True)
    serializer_class = ServicioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categoria']
    search_fields = ['titulo', 'descripcion']

class TestimonioViewSet(viewsets.ModelViewSet):
    queryset = Testimonio.objects.filter(aprobado=True)
    serializer_class = TestimonioSerializer


# views.py
from rest_framework import viewsets
from .models import Equipo, Noticia
from .serializers import EquipoSerializer, NoticiaSerializer

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer


class MensajeContactoViewSet(viewsets.ModelViewSet):
    queryset = MensajeContacto.objects.all()
    serializer_class = MensajeContactoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'email', 'mensaje']

@api_view(['POST'])
def solicitud_socio(request):
    serializer = SocioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Solicitud enviada exitosamente',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    
    
    

    def perform_create(self, serializer):
        serializer.save()
        # Aquí podrías agregar lógica para enviar emails de confirmación