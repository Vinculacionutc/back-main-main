from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Categoria, Icono, RedSocial, Empresa, 
    EmpresaRedSocial, Producto, CaracteristicaProducto,
    Servicio, Testimonio, Equipo, Noticia, 
    MensajeContacto, Socio, JobApplication, EmpresaUsuario
)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class EmpresaUsuarioInline(admin.StackedInline):
    model = EmpresaUsuario
    can_delete = True
    verbose_name_plural = 'Empresa asignada'

class CustomUserAdmin(UserAdmin):
    inlines = (EmpresaUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_empresa')
    
    def get_empresa(self, obj):
        try:
            return obj.empresausuario.empresa.nombre
        except:
            return '-'
    get_empresa.short_description = 'Empresa'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(EmpresaUsuario)
class EmpresaUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'empresa', 'fecha_asignacion']
    list_filter = ['empresa', 'fecha_asignacion']
    search_fields = ['usuario__username', 'usuario__email', 'empresa__nombre']
    raw_id_fields = ['usuario', 'empresa']
    date_hierarchy = 'fecha_asignacion'

class CaracteristicaProductoInline(admin.TabularInline):
    model = CaracteristicaProducto
    extra = 1

class EmpresaRedSocialInline(admin.TabularInline):
    model = EmpresaRedSocial
    extra = 1

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'productos_count']
    search_fields = ['nombre']
    list_per_page = 20

    def productos_count(self, obj):
        return obj.producto_set.count()
    productos_count.short_description = 'Número de Productos'

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'telefono', 'correo', 'activa', 'mostrar_logo']
    list_filter = ['categoria', 'activa', 'fecha_registro']
    search_fields = ['nombre', 'descripcion']
    readonly_fields = ['fecha_registro', 'mostrar_logo']
    inlines = [EmpresaRedSocialInline]
    fieldsets = (
        ('Información Principal', {
            'fields': ('nombre', 'categoria', 'descripcion', 'logo', 'mostrar_logo')
        }),
        ('Contacto', {
            'fields': ('telefono', 'correo', 'sitio_web', 'direccion')
        }),
        ('Estado', {
            'fields': ('activa', 'fecha_registro')
        }),
    )

    def mostrar_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.logo.url)
        return "Sin logo"
    mostrar_logo.short_description = 'Vista previa del logo'

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'empresa', 'categoria', 'precio', 'activo', 'mostrar_imagen']
    list_filter = ['categoria', 'activo', 'empresa']
    search_fields = ['nombre', 'descripcion']
    inlines = [CaracteristicaProductoInline]
    readonly_fields = ['mostrar_imagen']
    fieldsets = (
        ('Información Principal', {
            'fields': ('nombre', 'empresa', 'categoria', 'descripcion')
        }),
        ('Imagen y Precio', {
            'fields': ('imagen', 'mostrar_imagen', 'precio')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.imagen.url)
        return "Sin imagen"
    mostrar_imagen.short_description = 'Vista previa de la imagen'

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'icono', 'activo']
    list_filter = ['categoria', 'activo']
    search_fields = ['titulo', 'descripcion']
    list_editable = ['activo']

@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cargo', 'empresa', 'fecha', 'aprobado']
    list_filter = ['aprobado', 'fecha', 'empresa']
    search_fields = ['nombre', 'comentario']
    list_editable = ['aprobado']
    date_hierarchy = 'fecha'

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'asunto', 'fecha_creacion', 'leido']
    list_filter = ['leido', 'fecha_creacion']
    search_fields = ['nombre', 'email', 'asunto', 'mensaje']
    readonly_fields = ['fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    list_editable = ['leido']
    fieldsets = (
        ('Información del Contacto', {
            'fields': ('nombre', 'email')
        }),
        ('Mensaje', {
            'fields': ('asunto', 'mensaje')
        }),
        ('Estado', {
            'fields': ('leido', 'fecha_creacion')
        }),
    )

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_publicacion', 'mostrar_foto']
    list_filter = ['fecha_publicacion']
    search_fields = ['titulo', 'contenido']
    readonly_fields = ['fecha_publicacion', 'mostrar_foto']
    date_hierarchy = 'fecha_publicacion'
    fieldsets = (
        ('Contenido', {
            'fields': ('titulo', 'contenido')
        }),
        ('Multimedia', {
            'fields': ('foto', 'mostrar_foto', 'link')
        }),
        ('Fecha', {
            'fields': ('fecha_publicacion',)
        }),
    )

    def mostrar_foto(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.foto.url)
        return "Sin foto"
    mostrar_foto.short_description = 'Vista previa de la foto'

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'posicion', 'mostrar_imagen']
    search_fields = ['nombre', 'posicion', 'descripcion']
    readonly_fields = ['mostrar_imagen']
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'posicion', 'descripcion')
        }),
        ('Imagen', {
            'fields': ('imagen', 'mostrar_imagen')
        }),
    )

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.imagen.url)
        return "Sin imagen"
    mostrar_imagen.short_description = 'Vista previa de la imagen'

@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'empresa', 'email', 'telefono', 'estado', 'fecha_solicitud']
    list_filter = ['estado', 'fecha_solicitud', 'ciudad']
    search_fields = ['nombre', 'apellido', 'email', 'empresa']
    readonly_fields = ['fecha_solicitud']
    date_hierarchy = 'fecha_solicitud'
    
    fieldsets = (
        ('Información Personal', {
            'fields': (('nombre', 'apellido'), 'email', 'telefono')
        }),
        ('Información Empresarial', {
            'fields': ('empresa', 'cargo', 'descripcion_empresa')
        }),
        ('Ubicación', {
            'fields': ('direccion', 'ciudad')
        }),
        ('Solicitud', {
            'fields': ('motivo', 'estado', 'fecha_solicitud')
        }),
        ('Notas Administrativas', {
            'fields': ('notas_admin',),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('email',)
        return self.readonly_fields

# Registrar los modelos restantes
admin.site.register(Icono)
admin.site.register(RedSocial)

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'puesto_deseado', 'fecha_aplicacion', 'descargar_cv']
    list_filter = ['fecha_aplicacion', 'puesto_deseado']
    search_fields = ['nombre_completo', 'correo_electronico', 'puesto_deseado']
    readonly_fields = ['fecha_aplicacion', 'descargar_cv']
    
    def descargar_cv(self, obj):
        if obj.cv:
            return format_html('<a href="{}" target="_blank">Descargar CV</a>', obj.cv_download_url)
        return "Sin CV"
    descargar_cv.short_description = 'CV'
    
    