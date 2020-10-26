from .segment.segmentation_v2 import Segmentation as seg
from django.conf import settings
from cv2 import cv2 as cv
import numpy as np
import json as js
import os


def segment(imagepath, json):
    img = cv.imread(imagepath,1)
    se = seg()
    json_dict = js.load(json)
    se.run(img, json_dict)
    path_list = imagepath.split('/')
    path_list = path_list[:-1]
    save_path = "/".join(path_list)
    ##### image_path = save_path
    path_list = path_list[:-1]
    json_save_path = "/".join(path_list)
    json_path = "{}/{}".format(json_save_path, "json")
    os.mkdir(json_path)
    #### json path == json_path
    for image_name, image in se.image_dict.items():            
        result_name = "{}/{}".format(save_path,image_name)
        cv.imwrite(result_name,image)
    for json_name, json_dict in se.json_dict.items():
        result_json = "{}/{}".format(json_path,json_name)
        with open(result_json,'w') as f:
            js.dump(json_dict, f)