from django.contrib import admin
from django.urls import path
from imageprocessing import views as im_v
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', im_v.image_process),
    path('seg/',im_v.img_seg),
    path('seg/export/',im_v.export) 
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
