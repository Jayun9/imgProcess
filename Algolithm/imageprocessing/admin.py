from django.contrib import admin
from .models import ImageUploadModel


class ImageUploadModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'image',)
admin.site.register(ImageUploadModel,ImageUploadModelAdmin)
