#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Hantzley Tauckoor
Date: 14 June 2017
Version: 1
Description: Sample script to download image file from web or Spark, and use
             Google Vision API to extract a MAC address if it exists in the
             image.
'''

import requests
import io
import os
import re
from google.cloud import vision
from google.cloud.vision import types


image_is_in_Spark = False
filename = None

# Set Spark Token on the next line, or use an env variable if you have one.
#SPARK_TOKEN = ""

# I am using an env variable for the Spark Token. Comment the line below if you
# are manually setting this variable above.
SPARK_TOKEN = os.environ['SPARK_TOKEN']


#image_url = "https://api.ciscospark.com/v1/contents/XXXXXXXXXXXXXXXXXXXXXXXXXX"
#image_url = "https://upload.wikimedia.org/wikipedia/commons/c/c0/Opera_House_and_ferry._Sydney.jpg"
#image_url = "http://justfunfacts.com/wp-content/uploads/2015/11/sydney-opera-house-2.jpg"
image_url = "https://theautomationblog.com/wp-content/uploads/Micro820.jpg"


def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))


def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))


def detect_mac_address(path):
    """Detects MAC address in the file."""
    client = vision.ImageAnnotatorClient()
    MAC = "MAC address not found"

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        match_regex = re.compile('^' + '[\:\-]'.join(['([0-9A-F]{1,2})']*6) + '$', re.IGNORECASE)
        mac_addresses = match_regex.findall(text.description)
        if len(mac_addresses) > 0:
            MAC = ':'.join(mac_addresses[0])

    return MAC

if __name__ == '__main__':

    # Check if image is in Spark, and setting the headers with Spark Token
    if "https://api.ciscospark.com/v1/contents/" in image_url:
        image_is_in_Spark = True
        headers = {
            'authorization': "Bearer " + SPARK_TOKEN,
            'cache-control': "no-cache",
        }
        response = requests.request("GET", image_url, headers=headers)
    else:
        response = requests.request("GET", image_url)

    #print ("Status code: ", response.status_code)

    if response.status_code == 200:
        if image_is_in_Spark:
            # Image is in Spark, filename is retrieved from headers
            imgHeaders = response.headers
            #print (imgHeaders)

            if 'image' in imgHeaders['Content-Type']:
                filename = imgHeaders[
                    'Content-Disposition'].replace("attachment; ", "").replace('filename', '').replace('=', '').replace('"', '')
            else:
                print(str(filename) + " is not an image")
                exit()
        else:
            filename = image_url.split("/")[-1]

        # Download the image
        with open(filename, 'wb') as f:
            f.write(response.content)

        # Instantiates a client
        vision_client = vision.Client()

        # The name of the image file to annotate
        file_name = os.path.join(
            os.path.dirname(__file__), filename)

        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
            image = vision_client.image(
                content=content)


        #print ("Detecting text from URI")
        #etect_text_uri(image_url)

        #print ("\n\nDetecting text from downloaded image")
        #detect_text(filename)

        print ("\n\nDetecting MAC address from downloaded image:")
        print (detect_mac_address(filename))
