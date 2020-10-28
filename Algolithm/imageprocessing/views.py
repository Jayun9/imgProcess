from django.shortcuts import render
from .forms import UploadImageForm
from django.core.files.storage import FileSystemStorage
from .forms import ImageUploadForm
from django.conf import settings
from .image_seg import segment
import os
from django.http import HttpResponse
import simplejson as js
from django.views.generic import View

def image_process(request):
    return render(request, 'image_process/base.html',{})

def uimage(request):
    if request.method =='POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            return render(request, 'image_process/uimage.html', {'form' : form , 'uploaded_file_url' : uploaded_file_url})
    else:
        form = UploadImageForm()
        return render(request, 'image_process/uimage.html', {'form' : form})

class dface(View):
    def __init__(self):
        self.post_path = []
    def post(self,request, *args, **kwargs):
        if request.POST.get('RUN', None) is None:
            print(self.post_path)
            return render(request, 'image_process/algolithm.html') 
        else:
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                
                imageURL = settings.MEDIA_URL + form.instance.image.name 
                json = request.FILES['json_file']
                segment(settings.MEDIA_ROOT_URL + imageURL, json)

                result_image_path = post.image.url
                original_name = result_image_path.split('/')[-1]
                result_image_path = result_image_path.split('/')[:-1]
                result_image_path = '/'.join(result_image_path)
                image_list = os.listdir("{}/{}".format(settings.MEDIA_ROOT_URL,result_image_path))
                image = []
                for image_name in image_list:
                    if image_name != original_name:
                        image_path = "{}/{}".format(result_image_path,image_name)
                        self.post_path.append(image_path)
                        image.append(image_name)
                return render(request, 'image_process/algolithm.html', {'post' : post, 'post_path' : self.post_path, 'image_list' : image})
    def get(self, request, *args, **kwargs):
        return render(request, 'image_process/algolithm.html')

