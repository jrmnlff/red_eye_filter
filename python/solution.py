#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from typing import (
    List,
    Tuple,
    Union
)

from utils.image import (
    ImageType,
    PackedImage,
    StrideImage,
)

from utils.function_tracer import FunctionTracer
import utils.eye_pattern as ep
from utils.eye_pattern import InnerEyeType

red_color_treshold = 200
eye_pattern_size = 5
eye_inner_size = 3

def compute_solution(images: List[Union[PackedImage, StrideImage]], out_images: List[Union[PackedImage, StrideImage]]):
    ft = FunctionTracer("compute_solution", "seconds")

    #TODO fill solution
    a=1
    for i in images:
        image = i.pixels_red
        #plt.imsave('out\eye'+str(a)+'.png', np.array(result).reshape(i.resolution.width,i.resolution.height), cmap=cm.gray)
        plt.imshow(np.array(image).reshape(i.resolution.width,i.resolution.height))
        plt.show()
        plt.imshow(np.array(out_images[a-1].pixels_red).reshape(i.resolution.width,i.resolution.height))
        a+=1
        result = process_image(image, i.resolution.width,i.resolution.height)
        plt.imshow(np.array(result).reshape(i.resolution.width,i.resolution.height))

    del ft

def process_image(image: List[int], width, height):
    #Find all base patterns candidates
    candidates = find_rectangle_candidates(image, width, height)
    # For each candidate - try to match pattens
    eyes = filter_inner_types(image, candidates)
    #correct eyes
    correct_eyes(image, eyes)
    return

def filter_inner_types(image: List[int], candidates: List[int]):
    for candidate in candidates:
        


    return

def find_rectangle_candidates(image: List[int], width, height):
    rectangle_points = []
    for row in range(0, width - eye_pattern_size):
        for col in range(0, height - eye_pattern_size):
            if find_rectangle(image, row,col,width,height):
                rectangle_points.append((row*width)+col)
    return rectangle_points

def find_rectangle(image: List[int], row:int,col:int,width:int,height:int):
    
    #first row
    for roi_col in range(col, col+eye_pattern_size):
        if image[roi_col+row*width]<red_color_treshold:
                return False
    
    #last row
    for roi_col in range(col, col+eye_pattern_size):
        if image[roi_col+(row+eye_pattern_size-1)*width]<red_color_treshold:
                return False
    
    # left column
    for roi_row in range(row+1, row+1+eye_inner_size):
        if image[col+roi_row*width]<red_color_treshold:
            return False
    
    # right column
    for roi_row in range(row+1, row+1+eye_inner_size):
        if image[col+eye_inner_size+1+roi_row*width]<red_color_treshold:
            return False
    
    return True

def correct_eyes(rectangles: List[Union[PackedImage, StrideImage]]):
    return