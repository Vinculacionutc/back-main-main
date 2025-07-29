from django.db import models
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.
# models.py
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Icono(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    codigo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class RedSocial(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    url_base = models.URLField()
    icono = models.ForeignKey(Icono, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

class Empresa(models.Model):
    ruc = models.CharField(max_length=13, blank=True, null=True, default="1234567890001")
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    descripcion = models.TextField()
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True, verbose_name='Red Social')
    direccion = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    logo = CloudinaryField('logo', blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True, default="https://www.facebook.com/")
    twitter = models.CharField(max_length=100, blank=True, null=True, default="https://www.twitter.com/")
    instagram = models.CharField(max_length=100, blank=True, null=True, default="https://www.instagram.com/")
    tiktok = models.CharField(max_length=100, blank=True, null=True, default="https://www.tiktok.com/")
    linkedin = models.CharField(max_length=100, blank=True, null=True, default="https://www.linkedin.com/")

    def __str__(self):
        return self.nombre

class EmpresaRedSocial(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='redes_sociales', on_delete=models.CASCADE)
    red_social = models.ForeignKey(RedSocial, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    url = models.URLField()

    class Meta:
        unique_together = ['empresa', 'red_social']

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    empresa = models.ForeignKey(Empresa, related_name='productos', on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = CloudinaryField('imagen', blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class CaracteristicaProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='caracteristicas', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    valor = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.producto.nombre} - {self.nombre}"

class Servicio(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.ForeignKey(Icono, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Testimonio(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - {self.empresa.nombre}"
    

# models.py
from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    posicion = models.CharField(max_length=100)
    imagen = CloudinaryField('imagen', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)
    foto = CloudinaryField('foto', blank=True, null=True)

    def __str__(self):
        return self.titulo
    

# models.py
from django.db import models
from django.utils import timezone

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    leido = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Mensaje de contacto'
        verbose_name_plural = 'Mensajes de contacto'

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"

class Socio(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado')
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True, verbose_name='Cédula', default="1234567890", blank=True, null=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    empresa = models.CharField(max_length=200)
    cargo = models.CharField(max_length=100)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    descripcion_empresa = models.TextField(help_text='Breve descripción de su empresa y actividades')
    motivo = models.TextField(help_text='¿Por qué desea ser socio?')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    notas_admin = models.TextField(blank=True, null=True, help_text='Notas internas para administradores')
    
    class Meta:
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.empresa}"
#
class JobApplication(models.Model):
    nombre_completo = models.CharField(max_length=200, verbose_name="Nombre Completo")
    correo_electronico = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    puesto_deseado = models.CharField(max_length=100, verbose_name="Puesto Deseado")
    experiencia_relevante = models.TextField(verbose_name="Experiencia Relevante")
    mensaje_presentacion = models.TextField(verbose_name="Mensaje de Presentación")
    cv = CloudinaryField(folder='cvs', resource_type='raw', help_text="PDF o Word (máx. 5MB)")
    fecha_aplicacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Aplicación de Trabajo"
        verbose_name_plural = "Aplicaciones de Trabajo"
        ordering = ['-fecha_aplicacion']

    def __str__(self):
        return f"{self.nombre_completo} - {self.puesto_deseado}"

    def clean(self):
        if self.cv:
            if self.cv.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('El archivo CV no debe exceder 5MB')
            ext = self.cv.name.split('.')[-1].lower()
            if ext not in ['pdf', 'doc', 'docx']:
                raise ValidationError('Solo se permiten archivos PDF o Word')
    
    @property
    def cv_download_url(self):
        if self.cv:
            # Add fl_attachment to force download
            return self.cv.url.replace('/upload/', '/upload/fl_attachment/')
        return None

class EmpresaUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
    fecha_asignacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')

    class Meta:
        verbose_name = 'Usuario de Empresa'
        verbose_name_plural = 'Usuarios de Empresas'
        ordering = ['-fecha_asignacion']

    def __str__(self):
        return f"{self.usuario.username} - {self.empresa.nombre}"

    def clean(self):
        # Validar que no exista otro usuario para la misma empresa
        if EmpresaUsuario.objects.exclude(id=self.id).filter(empresa=self.empresa).exists():
            raise ValidationError('Esta empresa ya tiene un usuario asignado.')
        
        # Validar que el usuario no esté asignado a otra empresa
        if EmpresaUsuario.objects.exclude(id=self.id).filter(usuario=self.usuario).exists():
            raise ValidationError('Este usuario ya está asignado a otra empresa.')