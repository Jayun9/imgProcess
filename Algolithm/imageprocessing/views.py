from django.shortcuts import render
from .forms import UploadImageForm
from django.core.files.storage import FileSystemStorage
from .forms import ImageUploadForm
from django.conf import settings
from .image_seg import segment
import os
from django.http import HttpResponse, QueryDict
import simplejson as js
from django.views.generic import View

def image_process(request):
    return render(request, 'image_process/algolithm.html')

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
        return render(request, 'imageprocess/algolithm.html')

def img_seg(request):
    if request.method == 'POST':
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
            post_path = []
            for image_name in image_list:
                if image_name != original_name:
                    image_path = "{}/{}".format(result_image_path,image_name)
                    post_path.append(image_path)
                    image.append(image_name)
            return render(request, 'image_process/algolithm.html', {'post' : post, 'post_path' : post_path, 'image_list' : image})
    else:
        form = ImageUploadForm()
        return render(request, 'image_process/algolithm.html',{'form': form})

def export(request):
    request_dict = request.POST.dict()
    print(request_dict)
    query_dict = QueryDict('', mutable=True)
    query_dict.update(request_dict)
    print(query_dict)
    form = ImageUploadForm()
    return render(request, 'image_process/algolithm.html',{'form': form})
