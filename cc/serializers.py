# serializers.py
from rest_framework import serializers
from .models import Categoria, Icono, RedSocial, CaracteristicaProducto, Producto, Empresa, EmpresaRedSocial, Servicio, Testimonio, Equipo, Noticia, MensajeContacto, Socio, JobApplication
from cloudinary.models import CloudinaryField

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class IconoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icono
        fields = '__all__'

class RedSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedSocial
        fields = '__all__'

class CaracteristicaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaracteristicaProducto
        fields = ['nombre', 'valor']

class ProductoSerializer(serializers.ModelSerializer):
    caracteristicas = CaracteristicaProductoSerializer(many=True, read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = '__all__'

    def get_imagen_url(self, obj):
        if obj.imagen:
            return obj.imagen.url
        return None

class EmpresaRedSocialSerializer(serializers.ModelSerializer):
    red_social_nombre = serializers.CharField(source='red_social.nombre', read_only=True)

    class Meta:
        model = EmpresaRedSocial
        fields = '__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True, read_only=True)
    redes_sociales = EmpresaRedSocialSerializer(many=True, read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Empresa
        fields = '__all__'

    def get_logo_url(self, obj):
        if obj.logo:
            return obj.logo.url
        return None

class ServicioSerializer(serializers.ModelSerializer):
    icono_nombre = serializers.CharField(source='icono.nombre', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Servicio
        fields = '__all__'

class TestimonioSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)

    class Meta:
        model = Testimonio
        fields = '__all__'

class EquipoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Equipo
        fields = '__all__'

    def get_imagen_url(self, obj):
        if obj.imagen:
            return obj.imagen.url
        return None

class NoticiaSerializer(serializers.ModelSerializer):
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Noticia
        fields = '__all__'

    def get_foto_url(self, obj):
        if obj.foto:
            return obj.foto.url
        return None

class MensajeContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']

class SocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socio
        fields = [
            'id', 'nombre', 'apellido', 'email', 'telefono',
            'empresa', 'cargo', 'direccion', 'ciudad',
            'descripcion_empresa', 'motivo', 'fecha_solicitud', 'estado'
        ]
        read_only_fields = ['fecha_solicitud', 'estado']
        
    def validate_email(self, value):
        if Socio.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe una solicitud con este correo electrónico.")
        return value

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            'id',
            'nombre_completo',
            'correo_electronico',
            'telefono',
            'puesto_deseado',
            'experiencia_relevante',
            'mensaje_presentacion',
            'cv',
            'fecha_aplicacion'
        ]
        read_only_fields = ['fecha_aplicacion']

    def validate_cv(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError('El archivo CV no debe exceder 5MB')
        ext = value.name.split('.')[-1].lower()
        if ext not in ['pdf', 'doc', 'docx']:
            raise serializers.ValidationError('Solo se permiten archivos PDF o Word')
        return value
