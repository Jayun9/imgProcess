from django.db import models
import uuid



def image_directory(instance,filename):
    return '{}/{}/{}'.format(instance.id,"image", filename)


class ImageUploadModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=image_directory)

    class Meta:
        db_table = 'image_table'
        verbose_name = "이미지 처리"
        verbose_name_plural = '이미지 처리'

    