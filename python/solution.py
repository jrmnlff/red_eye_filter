#!/usr/bin/env python3

from ast import While
from pickle import FALSE
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from typing import (
    List,
    Tuple,
    Union
)
from utils.eye import Eye
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
reduce_value = 150

def compute_solution(images: List[Union[PackedImage, StrideImage]], out_images: List[Union[PackedImage, StrideImage]]):
    ft = FunctionTracer("compute_solution", "seconds")

    for i in images:
        process_image(i.pixels_red, i.resolution.width,i.resolution.height)
        
    del ft

def process_image(image: List[int], width, height):
    #Find all base patterns candidates
    candidates = find_rectangle_candidates(image, width, height)
    #For each candidate - try to match pattens
    eyes = filter_inner_types(image, candidates, width, height)
    #correct eyes
    correct_eyes(image, eyes, width, height)
    return

def correct_eyes(image: List[int], eyes: List[Eye], width:int, height:int):
    #plt.imshow(np.array(image).reshape(height,width))
    for eye in eyes:
        #correct each eye
        correct_rectangle(image, eye.point, width)
        correct_inner_pattern(image, eye, width)
        #plt.imshow(np.array(image).reshape(height,width))
        
    return

def filter_inner_types(image: List[int], candidates: List[int], width, height):
    eyes=[]
    for candidate in candidates:
        #Match all inner patterns
        is_horizontal = check_horizontal_inner_pattern(image, candidate, width)
        is_vertical = check_vertical_inner_pattern(image, candidate, width)
        is_diagonal = check_diagonal_inner_pattern(image, candidate, width)
        
        if not is_horizontal and not is_vertical and not is_diagonal:
            #No inner pattern is matched
            continue

        #For each pattern matched - create eye to correct later
        eyes.append(Eye(candidate, get_inner_type(is_horizontal, is_vertical, is_diagonal)))

    return eyes

def get_inner_type(is_horizontal, is_vertical, is_diagonal):
    if is_horizontal and is_vertical:
        return InnerEyeType.Plus
    elif is_horizontal:
        return InnerEyeType.Horizontal
    elif is_vertical:
        return InnerEyeType.Vertical
    else:
        return InnerEyeType.Diagonal

def is_pixel_under_treshold(image: List[int], index):
    #TODO: Fix this check
    if index>=len(image):
        return True

    if image[index] < red_color_treshold:
            return True
    return False

def correct_pixel(image: List[int], index):
    #In case of overlapping eyes
    if is_pixel_under_treshold(image, index):
        return
    #Correct the pixel value
    image[index] = image[index] - reduce_value

def correct_rectangle(image: List[int], index:int, width:int):
    for i in range(index, index+eye_pattern_size):
        #first row
        correct_pixel(image, i)

        #last row
        correct_pixel(image, i + ((eye_pattern_size-1)*width))
    
    i = index+width
    while(i < index + ((eye_pattern_size)*width)):
        #left column
        correct_pixel(image, i)
        
        #right column
        correct_pixel(image, i + eye_pattern_size - 1)
        i+=width

def correct_inner_pattern(image: List[int], eye:Eye, width:int):
    if eye.type is InnerEyeType.Plus:
        fix_horizontal_inner_pattern(image, eye.point, width)
        fix_vertical_inner_pattern(image, eye.point, width)
    elif eye.type is InnerEyeType.Horizontal:
        fix_horizontal_inner_pattern(image, eye.point, width)
    elif eye.type is InnerEyeType.Vertical:
        fix_vertical_inner_pattern(image, eye.point, width)
    elif eye.type is InnerEyeType.Diagonal:
        fix_diagonal_inner_pattern(image, eye.point, width)
    
    

def check_horizontal_inner_pattern(image: List[int], starting_index, width):
    start = starting_index + 2*width + 1
    for index in range(start,start + eye_inner_size):
        if is_pixel_under_treshold(image, index):
            return False
    return True

def fix_horizontal_inner_pattern(image: List[int], starting_index, width):
    start = starting_index + 2*width + 1
    for index in range(start,start + eye_inner_size):
        correct_pixel(image, index)

def check_vertical_inner_pattern(image: List[int], starting_index:int, width:int):
    start = starting_index + int(eye_pattern_size/2) + width
    index=start
    while(index < start + eye_inner_size*width):
        if is_pixel_under_treshold(image, index):
            return False
        index+=width
    return True

def fix_vertical_inner_pattern(image: List[int], starting_index:int, width:int):
    start = starting_index + int(eye_pattern_size/2) + width
    index=start
    while(index < start + eye_inner_size*width):
        correct_pixel(image, index)
        index+=width

def check_diagonal_inner_pattern(image: List[int], starting_index:int, width:int):
    if check_first_diagonal(image,starting_index, width) and check_second_diagonal(image,starting_index, width):
        return True
    return False

def check_first_diagonal(image: List[int], starting_index:int, width:int):
    start = starting_index + width + 1
    index=start
    while(index < start + eye_inner_size*width + eye_inner_size-1):
        if is_pixel_under_treshold(image, index):
            return False
        index+=width+1
    return True

def check_second_diagonal(image: List[int], starting_index:int, width:int):
    start = starting_index + width + eye_inner_size
    index=start
    while(index < start + eye_inner_size*width + 1):
        if is_pixel_under_treshold(image, index):
            return False
        index+=width-1
    return True

def fix_diagonal_inner_pattern(image: List[int], starting_index:int, width:int):
    #first diagonal
    start = starting_index + width + 1
    index=start
    while(index < start + eye_inner_size*width + eye_inner_size-1):
        correct_pixel(image, index)
        index+=width+1

    #second diagonal
    start = starting_index + width + eye_inner_size
    index=start
    while(index < start + eye_inner_size*width + 1):
        correct_pixel(image, index)
        index+=width-1

def find_rectangle_candidates(image: List[int], width:int, height:int):
    rectangle_points = []
    for row in range(0, height - eye_pattern_size+1):
        for col in range(0, width - eye_pattern_size+1):
            if find_rectangle(image, row,col,width,height):
                rectangle_points.append((row*width)+col)
    return rectangle_points

def find_rectangle(image: List[int], row:int, col:int, width:int, height:int):
    for roi_col in range(col, col+eye_pattern_size):
        #first row
        if is_pixel_under_treshold(image, roi_col+row*width):
                return False
        #last row
        if is_pixel_under_treshold(image, roi_col+(row+eye_pattern_size-1)*width):
                return False
    
    for roi_row in range(row+1, row+1+eye_inner_size):
        #left column
        if is_pixel_under_treshold(image,col+roi_row*width):
            return False
        #right column
        if is_pixel_under_treshold(image,col+eye_inner_size+1+roi_row*width):
            return False
    
    return True

