#!/usr/bin/env python3

import argparse
import os
import xml.dom.minidom as minidom
import unicodedata

parser = argparse.ArgumentParser(description="""Creates line images from page image.""")
parser.add_argument('database_path', type=str,
                    help='Path to the downloaded (and extracted) mdacat data')
args = parser.parse_args()

def get_word_line_mapping(madcat_file_path):
    doc = minidom.parse(madcat_file_path)
    zone = doc.getElementsByTagName('zone')
    for node in zone:
        line_id = node.getAttribute('id')
        line_word_dict[line_id] = list()
        word_image = node.getElementsByTagName('token-image')
        for tnode in word_image:
            word_id = tnode.getAttribute('id')
            line_word_dict[line_id].append(word_id)
            word_line_dict[word_id] = line_id


def remove_corrupt_xml_files():
    return True


def read_text(madcat_file_path):
    text_line_word_dict = dict()
    print(madcat_file_path)
    doc = minidom.parse(madcat_file_path)
    segment = doc.getElementsByTagName('segment')
    for node in segment:
        token = node.getElementsByTagName('token')
        for tnode in token:
            segment_id = tnode.getAttribute('id')
            ref_word_id = tnode.getAttribute('ref_id')
            word = tnode.getElementsByTagName('source')[0].firstChild.nodeValue
            ref_line_id = word_line_dict[ref_word_id]
            if ref_line_id not in text_line_word_dict:
                text_line_word_dict[ref_line_id] = list()
            text_line_word_dict[ref_line_id].append(word)

    for key in text_line_word_dict:
        text_line = key
        for ele in text_line_word_dict[key]:
            text_line += ele
        print(text_line)

### main ###
data_path = args.database_path
line_word_dict = dict()
word_line_dict = dict()
for file in os.listdir(os.path.join(data_path, 'images')):
    if file.endswith(".tif"):
        madcat_file_path = os.path.join(data_path, 'gedi', file)
        madcat_file_path = madcat_file_path.replace(".tif", ".madcat.xml")

        if remove_corrupt_xml_files():
            line_word_dict = dict()
            word_line_dict = dict()
            get_word_line_mapping(madcat_file_path)
            read_text(madcat_file_path)
            break


