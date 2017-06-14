#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: Hantzley Tauckoor
Date: 14 June 2017
Version: 1
Description: Sample script to download image file from web or Spark, and use
             Google Vision API to get contextual information on the image.
'''

import requests
import io
import os
from google.cloud import vision

print_labels = True
print_web_pages_with_matching_image = True
print_web_pages_with_full_matching_image = False
print_web_pages_with_partial_matching_image = False
print_web_entities = True
image_is_in_Spark = False
filename = None

# Set Spark Token on the next line, or use an env variable if you have one.
#SPARK_TOKEN = ""

# I am using an env variable for the Spark Token. Comment the line below if you
# are manually setting this variable above.
SPARK_TOKEN = os.environ['SPARK_TOKEN']


#image_url = "https://api.ciscospark.com/v1/contents/XXXXXXXXXXXXXXXXXXXXXXXXXX"
image_url = "https://upload.wikimedia.org/wikipedia/commons/c/c0/Opera_House_and_ferry._Sydney.jpg"


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
        else:
            filename = image_url.split("/")[-1]

        # Download the image
        with open(filename, 'wb') as f:
            f.write(response.content)

        # Imports the Google Cloud client library
        from google.cloud import vision

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

        if print_labels:
            # Performs label detection on the image file
            labels = image.detect_labels()

            print('Image Labels for ', filename, ":")
            for label in labels:
                print("* ", label.description)

        if print_web_pages_with_matching_image or print_web_pages_with_full_matching_image or \
                print_web_pages_with_partial_matching_image or print_web_entities:
            notes = image.detect_web()

        if notes.pages_with_matching_images and print_web_pages_with_matching_image:
            print('\nPages with matching images retrieved')

            for page in notes.pages_with_matching_images:
                print('Url : ', page.url)

        if notes.full_matching_images and print_web_pages_with_full_matching_image:
            print('\nFull Matches found: ', len(notes.full_matching_images))

            for image in notes.full_matching_images:
                print('Url : ', image.url)

        if notes.partial_matching_images and print_web_pages_with_partial_matching_image:
            print('\nPartial Matches found: ', len(notes.partial_matching_images))

            for image in notes.partial_matching_images:
                print('Url : ', image.url)

        if notes.web_entities and print_web_entities:
            print('\nWeb entities found: ', len(notes.web_entities))

            for entity in notes.web_entities:
                print('* Description: ', entity.description)
