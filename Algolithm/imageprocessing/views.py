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
from django.utils.encoding import smart_str

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
        #     # image path 처리
        # try:
        #     request_dict = request.POST.dict()
        #     print(request_dict)
        #     for _, path in request_dict.items():
        #         file_name = path.split('/')[-1]

        #         file_path = path.split('/')[3:]
        #         file_path = '/'.join(file_path)
        #         path_file = "./{}".format(file_path)

        #         response = HttpResponse(open(path_file, 'rb').read())
        #         response['Content-Type'] = "application/force_download"
        #         response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
        #     return response
        # except:
        #     return render(request, 'image_process/algolithm.html')
        return render(request, 'image_process/algolithm.html')
    
        


def export(request):
    # image path 처리
    request_dict = request.POST.dict()
    download_url = request_dict['0']
    print(download_url)
    response = HttpResponse()
    response['downloadUrl'] = download_url
    # for _, path in request_dict.items():   
    #     file_name = path.split('/')[-1]

    #     file_path = path.split('/')[3:]
    #     file_path = '/'.join(file_path)
    #     path_file = "./{}".format(file_path)

    #     print(file_name)
    #     print(path_file)
    return response
