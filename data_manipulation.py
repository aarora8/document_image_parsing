# Copyright      2018  Johns Hopkins University (author: Daniel Povey)
#                2018  Desh Raj
# Apache 2.0

import numpy as np
from PIL import Image, ImageDraw
""" TODO
"""


def convert_to_mask(x):
    """ This function accepts an object x that should represent an image
        with polygon objects in it, and returns an object representing an image
        with an object mask.
     """

    #validate_image_with_objects(x)

    im = x['img']
    object_id = 255
    y = dict()
    y['img'] = im
    mask_img = Image.new('L', (im.size[0], im.size[1]), 0)
    mask_img_arr = np.array(mask_img)
    for object in x['objects']:
        ordered_polygon_points = object['polygon']
        object_id -= 1
        temp_img = Image.new('L', (im.size[0], im.size[1]), 0)
        ImageDraw.Draw(temp_img).polygon(ordered_polygon_points, fill=object_id)
        temp_img_arr = np.array(temp_img)
        pixels = np.where(temp_img_arr == object_id, temp_img_arr, mask_img_arr)
        array = np.array(pixels, dtype=np.uint8)
        new_image = Image.fromarray(array)
        mask_img_arr = np.array(new_image)
    y['mask'] = mask_img_arr

    # validate_image_with_mask(y)

    return y


def convert_polygon_to_points(polygon):
    """  This function accepts an object representing a polygon as a list of
       points in clockwise or anticlockwise order, and returns the list of
       all the points that are inside that polygon.
    """
    #validate_polygon(polygon)

    ordered_polygon_points = polygon['polygon']
    x_list = [i[0] for i in ordered_polygon_points]
    y_list = [i[1] for i in ordered_polygon_points]
    min_x, max_x = min(x_list), max(x_list)
    min_y, max_y = min(y_list), max(y_list)
    mask_image = Image.new('L', (max_x, max_y), 0)
    ImageDraw.Draw(mask_image).polygon(ordered_polygon_points, fill=1)
    mask_img_arr = np.array(mask_image)
    points_location = np.where(mask_img_arr == 1)
    points_list = []
    for x, y in zip(points_location[0], points_location[1]):
        points_list.append((x, y))

    return points_list
    
