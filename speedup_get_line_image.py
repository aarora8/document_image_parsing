import argparse
import os
import xml.dom.minidom as minidom
from PIL import Image
import numpy as np
from scipy.misc import toimage

from scipy.spatial import ConvexHull
from math import sqrt
from math import atan2, cos, sin, pi, degrees
from collections import namedtuple

bounding_box_tuple = namedtuple('bounding_box_tuple', 'area '
                                        'length_parallel '
                                        'length_orthogonal '
                                        'rectangle_center '
                                        'unit_vector '
                                        'unit_vector_angle '
                                        'corner_points'
                         )


def unit_vector(pt0, pt1):
    dis_0_to_1 = sqrt((pt0[0] - pt1[0])**2 + (pt0[1] - pt1[1])**2)
    return (pt1[0] - pt0[0]) / dis_0_to_1, \
           (pt1[1] - pt0[1]) / dis_0_to_1


def orthogonal_vector(vector):
    return -1 * vector[1], vector[0]


def bounding_area(index, hull):
    unit_vector_p = unit_vector(hull[index], hull[index+1])
    unit_vector_o = orthogonal_vector(unit_vector_p)

    dis_p = tuple(np.dot(unit_vector_p, pt) for pt in hull)
    dis_o = tuple(np.dot(unit_vector_o, pt) for pt in hull)

    min_p = min(dis_p)
    min_o = min(dis_o)
    len_p = max(dis_p) - min_p
    len_o = max(dis_o) - min_o

    return {'area': len_p * len_o,
            'length_parallel': len_p,
            'length_orthogonal': len_o,
            'rectangle_center': (min_p + len_p / 2, min_o + len_o / 2),
            'unit_vector': unit_vector_p,
            }


def to_xy_coordinates(unit_vector_angle, point):
    angle_orthogonal = unit_vector_angle + pi / 2
    return point[0] * cos(unit_vector_angle) + point[1] * cos(angle_orthogonal), \
           point[0] * sin(unit_vector_angle) + point[1] * sin(angle_orthogonal)


def rotate_points(center_of_rotation, angle, points):
    rot_points = []
    ang = []
    for pt in points:
        diff = tuple([pt[d] - center_of_rotation[d] for d in range(2)])
        diff_angle = atan2(diff[1], diff[0]) + angle
        ang.append(diff_angle)
        diff_length = sqrt(sum([d**2 for d in diff]))
        rot_points.append((center_of_rotation[0] + diff_length * cos(diff_angle),
                           center_of_rotation[1] + diff_length * sin(diff_angle)))

    return rot_points


def rectangle_corners(rectangle):
    corner_points = []
    for i1 in (.5, -.5):
        for i2 in (i1, -1 * i1):
            corner_points.append((rectangle['rectangle_center'][0] + i1 * rectangle['length_parallel'],
                            rectangle['rectangle_center'][1] + i2 * rectangle['length_orthogonal']))

    return rotate_points(rectangle['rectangle_center'], rectangle['unit_vector_angle'], corner_points)


def minimum_bounding_box(points):
    if len(points) <= 2: raise ValueError('More than two points required.')

    hull_ordered = [points[index] for index in ConvexHull(points).vertices]
    hull_ordered.append(hull_ordered[0])
    hull_ordered = tuple(hull_ordered)

    min_rectangle = bounding_area(0, hull_ordered)
    for i in range(1, len(hull_ordered)-1):
        rectangle = bounding_area(i, hull_ordered)
        if rectangle['area'] < min_rectangle['area']:
            min_rectangle = rectangle

    min_rectangle['unit_vector_angle'] = atan2(min_rectangle['unit_vector'][1], min_rectangle['unit_vector'][0])
    min_rectangle['rectangle_center'] = to_xy_coordinates(min_rectangle['unit_vector_angle'], min_rectangle['rectangle_center'])

    return bounding_box_tuple(
        area=min_rectangle['area'],
        length_parallel=min_rectangle['length_parallel'],
        length_orthogonal=min_rectangle['length_orthogonal'],
        rectangle_center=min_rectangle['rectangle_center'],
        unit_vector=min_rectangle['unit_vector'],
        unit_vector_angle=min_rectangle['unit_vector_angle'],
        corner_points=set(rectangle_corners(min_rectangle))
    )


def get_center(im):
    center_x = im.size[0]/2
    center_y = im.size[1]/2
    return int(center_x), int(center_y)


def get_horizontal_angle(unit_vector_angle):
    if unit_vector_angle > pi / 2 and unit_vector_angle <= pi:
        unit_vector_angle = unit_vector_angle - pi
    elif unit_vector_angle > -pi and unit_vector_angle < -pi / 2:
        unit_vector_angle = unit_vector_angle + pi

    return unit_vector_angle


def get_smaller_angle(bounding_box):

    unit_vector = bounding_box.unit_vector
    unit_vector_angle = bounding_box.unit_vector_angle
    ortho_vector = orthogonal_vector(unit_vector)
    ortho_vector_angle = atan2(ortho_vector[1], ortho_vector[0])

    unit_vector_angle_updated = get_horizontal_angle(unit_vector_angle)
    ortho_vector_angle_updated = get_horizontal_angle(ortho_vector_angle)

    if abs(unit_vector_angle_updated) < abs(ortho_vector_angle_updated):
        return unit_vector_angle_updated
    else:
        return ortho_vector_angle_updated


def rotated_points(bounding_box, center):
    p1, p2, p3, p4 = bounding_box.corner_points
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    center_x, center_y = center
    rotation_angle_in_rad = -get_smaller_angle(bounding_box)
    x_dash_1 = (x1 - center_x) * cos(rotation_angle_in_rad) - (y1 - center_y) * sin(rotation_angle_in_rad) + center_x
    x_dash_2 = (x2 - center_x) * cos(rotation_angle_in_rad) - (y2 - center_y) * sin(rotation_angle_in_rad) + center_x
    x_dash_3 = (x3 - center_x) * cos(rotation_angle_in_rad) - (y3 - center_y) * sin(rotation_angle_in_rad) + center_x
    x_dash_4 = (x4 - center_x) * cos(rotation_angle_in_rad) - (y4 - center_y) * sin(rotation_angle_in_rad) + center_x

    y_dash_1 = (y1 - center_y) * cos(rotation_angle_in_rad) + (x1 - center_x) * sin(rotation_angle_in_rad) + center_y
    y_dash_2 = (y2 - center_y) * cos(rotation_angle_in_rad) + (x2 - center_x) * sin(rotation_angle_in_rad) + center_y
    y_dash_3 = (y3 - center_y) * cos(rotation_angle_in_rad) + (x3 - center_x) * sin(rotation_angle_in_rad) + center_y
    y_dash_4 = (y4 - center_y) * cos(rotation_angle_in_rad) + (x4 - center_x) * sin(rotation_angle_in_rad) + center_y
    return x_dash_1, y_dash_1, x_dash_2, y_dash_2, x_dash_3, y_dash_3, x_dash_4, y_dash_4


def set_line_image_data(image, line_id, image_file_name):
    base_name = os.path.splitext(os.path.basename(image_file_name))[0]
    line_image_file_name = base_name + line_id + '.tif'
    imgray = image.convert('L')
    imgray_rev_arr = np.fliplr(imgray)
    imgray_rev = toimage(imgray_rev_arr)
    imgray_rev.save(os.path.join(data_path, 'lines', line_image_file_name))


def get_line_images_from_page_image(image_file_name, madcat_file_path):
    im = Image.open(image_file_name)
    doc = minidom.parse(madcat_file_path)
    zone = doc.getElementsByTagName('zone')
    for node in zone:
        id = node.getAttribute('id')
        if id == 'z14':
            token_image = node.getElementsByTagName('token-image')
            minimum_bounding_box_input = []
            for token_node in token_image:
                word_point = token_node.getElementsByTagName('point')
                col_word, row_word = [], []
                for word_node in word_point:
                    col_word.append(int(word_node.getAttribute('x')))
                    row_word.append(int(word_node.getAttribute('y')))
                    word_coordinate = (int(word_node.getAttribute('x')), int(word_node.getAttribute('y')))
                    minimum_bounding_box_input.append(word_coordinate)

            bounding_box = minimum_bounding_box(minimum_bounding_box_input)

            p1, p2, p3, p4 = bounding_box.corner_points
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = p3
            x4, y4 = p4
            min_x = min(x1, x2, x3, x4)
            min_y = min(y1, y2, y3, y4)
            max_x = max(x1, x2, x3, x4)
            max_y = max(y1, y2, y3, y4)
            box = (min_x, min_y, max_x, max_y)
            region_initial = im.crop(box)
            region_initial.show()

            # #calculate new crop points
            rot_points = []
            p1_new = (x1 - min_x, y1 - min_y)
            p2_new = (x2 - min_x, y2 - min_y)
            p3_new = (x3 - min_x, y3 - min_y)
            p4_new = (x4 - min_x, y4 - min_y)
            rot_points.append(p1_new)
            rot_points.append(p2_new)
            rot_points.append(p3_new)
            rot_points.append(p4_new)

            cropped_bounding_box = bounding_box_tuple(bounding_box.area,
                bounding_box.length_parallel,
                bounding_box.length_orthogonal,
                bounding_box.length_orthogonal,
                bounding_box.unit_vector,
                bounding_box.unit_vector_angle,
                set(rot_points)
            )

            rotation_angle_in_rad = get_smaller_angle(cropped_bounding_box)
            img2 = region_initial.rotate(degrees(rotation_angle_in_rad), resample=Image.BICUBIC)
            img2.show()

            x_dash_1, y_dash_1, x_dash_2, y_dash_2, x_dash_3, y_dash_3, x_dash_4, y_dash_4 = rotated_points(
                cropped_bounding_box, get_center(region_initial))

            min_x = min(x_dash_1, x_dash_2, x_dash_3, x_dash_4)
            min_y = min(y_dash_1, y_dash_2, y_dash_3, y_dash_4)
            max_x = max(x_dash_1, x_dash_2, x_dash_3, x_dash_4)
            max_y = max(y_dash_1, y_dash_2, y_dash_3, y_dash_4)
            box = (min_x, min_y, max_x, max_y)
            region_final = img2.crop(box)
            region_final.show()
            input("Press the <ENTER> key to continue...")
            # set_line_image_data(region_final, id, image_file_name)


### main ###
data_path = '/Users/ashisharora/madcat_ar'
for file in os.listdir(os.path.join(data_path, 'images')):
    if file.endswith(".tif"):
        image_path = os.path.join(data_path, 'images', file)
        gedi_file_path = os.path.join(data_path, 'madcat', file)
        gedi_file_path = gedi_file_path.replace(".tif", ".madcat.xml")
        get_line_images_from_page_image(image_path, gedi_file_path)