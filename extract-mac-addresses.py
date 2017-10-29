#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Hantzley Tauckoor
Date: October 2017
Version: 1
Description: Command line utility to find MAC addresses in an image using
             Google Vision API.

             Usage: python extract-mac-addresses.py image.jpg
'''

import requests
import io
import os
import re
import sys
from google.cloud import vision
from google.cloud.vision import types

filename = None


def detect_mac_addresses(path):
    """Detects MAC addresses in the file."""
    client = vision.ImageAnnotatorClient()
    mac_addresses = []

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        #Match MAC addresses in format aa:bb:cc:dd:ee:ff or aa-bb-cc-dd-ee-ff
        tmp_text = text.description

        match_regex = re.compile('^' + '[\:\-]'.join(['([0-9A-F]{1,2})']*6) + '$', re.IGNORECASE)
        matched_mac_addresses = match_regex.findall(tmp_text)
        if len(matched_mac_addresses) == 0:
            #Match MAC addresses in format aabbccddeeff
            match_regex = re.compile('^' + '([0-9A-F]{2})'*6 + '$', re.IGNORECASE)
            matched_mac_addresses = match_regex.findall(tmp_text)

        if len(matched_mac_addresses) > 0:
            print (str(len(matched_mac_addresses)) + " matches found in text : " + tmp_text )
            for mac in matched_mac_addresses:
                mac_addresses.append(':'.join(mac))

    return mac_addresses



if __name__ == '__main__':
    if len(sys.argv) > 1:
        print (detect_mac_addresses(sys.argv[1]))
