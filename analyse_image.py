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
from google.cloud.vision import types

filename = None

# Set Spark Token on the next line, or use an env variable if you have one.
#SPARK_TOKEN = ""

# I am using an env variable for the Spark Token. Comment the line below if you
# are manually setting this variable above.
SPARK_TOKEN = os.environ['SPARK_TOKEN']


image_url = "https://api.ciscospark.com/v1/contents/Y2lzY29zcGFyazovL3VzL0NPTlRFTlQvZDZlNTJlMTAtYmIyNC0xMWU3LTkzZDEtNmI0NjNkMzMzNzZlLzA"
#image_url = "https://upload.wikimedia.org/wikipedia/commons/c/c0/Opera_House_and_ferry._Sydney.jpg"
#image_url = "http://justfunfacts.com/wp-content/uploads/2015/11/sydney-opera-house-2.jpg"


############################ Google Vision Functions ###########################

# [START def_detect_faces]
def detect_faces(path):
    """Detects faces in an image."""
    client = vision.ImageAnnotatorClient()

    # [START migration_face_detection]
    # [START migration_image_file]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    # [END migration_image_file]

    response = client.face_detection(image=image)
    faces = response.face_annotations

    lines = []

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    lines.append('\n**Faces:**')

    for face in faces:
        lines.append('* anger: {}'.format(likelihood_name[face.anger_likelihood]))
        lines.append('* joy: {}'.format(likelihood_name[face.joy_likelihood]))
        lines.append('* surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        lines.append('* face bounds: {}'.format(','.join(vertices)))

    return lines
    # [END migration_face_detection]
# [END def_detect_faces]


# [START def_detect_faces_uri]
def detect_faces_uri(uri):
    """Detects faces in the file located in Google Cloud Storage or the web."""
    client = vision.ImageAnnotatorClient()
    # [START migration_image_uri]
    image = types.Image()
    image.source.image_uri = uri
    # [END migration_image_uri]

    response = client.face_detection(image=image)
    faces = response.face_annotations

    lines = []

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    lines.append('\n**Faces:**')

    for face in faces:
        lines.append('* anger: {}'.format(likelihood_name[face.anger_likelihood]))
        lines.append('* joy: {}'.format(likelihood_name[face.joy_likelihood]))
        lines.append('* surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        lines.append('* face bounds: {}'.format(','.join(vertices)))

    return lines
# [END def_detect_faces_uri]


# [START def_detect_labels]
def detect_labels(path):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_label_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    lines = []
    lines.append('\n**Labels:**')

    for label in labels:
        lines.append('* ' + label.description)

    return lines
    # [END migration_label_detection]
# [END def_detect_labels]


# [START def_detect_labels_uri]
def detect_labels_uri(uri):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations

    lines = []
    lines.append('\n**Labels:**')

    for label in labels:
        lines.append('* ' + label.description)

    return lines
# [END def_detect_labels_uri]


# [START def_detect_landmarks]
def detect_landmarks(path):
    """Detects landmarks in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_landmark_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations

    lines = []
    lines.append('\n**Landmarks:**')

    for landmark in landmarks:
        lines.append('* ' + landmark.description)

    return lines
    # [END migration_landmark_detection]
# [END def_detect_landmarks]


# [START def_detect_landmarks_uri]
def detect_landmarks_uri(uri):
    """Detects landmarks in the file located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations

    lines = []
    lines.append('\n**Landmarks:**')

    for landmark in landmarks:
        lines.append('* ' + landmark.description)

    return lines
# [END def_detect_landmarks_uri]


# [START def_detect_logos]
def detect_logos(path):
    """Detects logos in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_logo_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations

    lines = []
    lines.append('\n**Logos:**')

    for logo in logos:
        lines.append('* ' + logo.description)

    return lines
    # [END migration_logo_detection]
# [END def_detect_logos]


# [START def_detect_logos_uri]
def detect_logos_uri(uri):
    """Detects logos in the file located in Google Cloud Storage or on the Web.
    """
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.logo_detection(image=image)
    logos = response.logo_annotations

    lines = []
    lines.append('\n**Logos:**')

    for logo in logos:
        lines.append('* ' + logo.description)

    return lines
# [END def_detect_logos_uri]


# [START def_detect_text]
def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    lines = []
    lines.append('\n**Texts:**')

    for text in texts:
        lines.append('\n* "{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        lines.append('* bounds: {}'.format(','.join(vertices)))

    return lines
    # [END migration_text_detection]
# [END def_detect_text]


# [START def_detect_text_uri]
def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations

    lines = []
    lines.append('\n**Texts:**')

    for text in texts:
        lines.append('\n* "{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        lines.append('* bounds: {}'.format(','.join(vertices)))

    return lines
# [END def_detect_text_uri]


# [START def_detect_web]
def detect_web(path):
    """Detects web annotations given an image."""
    client = vision.ImageAnnotatorClient()

    # [START migration_web_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.web_detection(image=image)
    notes = response.web_detection

    lines = []
    lines.append('\n**Web annotations:**')

    if notes.pages_with_matching_images:
        lines.append('\n{} Pages with matching images retrieved'.format(
               len(notes.pages_with_matching_images)))

        for page in notes.pages_with_matching_images:
            lines.append('* Url   : {}'.format(page.url))

    if notes.full_matching_images:
        lines.append ('\n{} Full Matches found: '.format(
               len(notes.full_matching_images)))

        for image in notes.full_matching_images:
            lines.append('* Url  : {}'.format(image.url))

    if notes.partial_matching_images:
        lines.append ('\n{} Partial Matches found: '.format(
               len(notes.partial_matching_images)))

        for image in notes.partial_matching_images:
            lines.append('* Url  : {}'.format(image.url))

    if notes.web_entities:
        lines.append ('\n{} Web entities found: '.format(len(notes.web_entities)))

        for entity in notes.web_entities:
            lines.append('* Score      : {}'.format(entity.score))
            lines.append('* Description: {}'.format(entity.description))

    return lines
    # [END migration_web_detection]
# [END def_detect_web]


# [START def_detect_web_uri]
def detect_web_uri(uri):
    """Detects web annotations in the file located in Google Cloud Storage."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.web_detection(image=image)
    notes = response.web_detection

    lines = []
    lines.append('\n**Web annotations:**')

    if notes.pages_with_matching_images:
        lines.append('\n{} Pages with matching images retrieved'.format(
               len(notes.pages_with_matching_images)))

        for page in notes.pages_with_matching_images:
            lines.append('* Url   : {}'.format(page.url))

    if notes.full_matching_images:
        lines.append ('\n{} Full Matches found: '.format(
               len(notes.full_matching_images)))

        for image in notes.full_matching_images:
            lines.append('* Url  : {}'.format(image.url))

    if notes.partial_matching_images:
        lines.append ('\n{} Partial Matches found: '.format(
               len(notes.partial_matching_images)))

        for image in notes.partial_matching_images:
            lines.append('* Url  : {}'.format(image.url))

    if notes.web_entities:
        lines.append ('\n{} Web entities found: '.format(len(notes.web_entities)))

        for entity in notes.web_entities:
            lines.append('* Score      : {}'.format(entity.score))
            lines.append('* Description: {}'.format(entity.description))

    return lines
# [END def_detect_web_uri]

################################################################################


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
        image_is_in_Spark = False
        response = requests.request("GET", image_url)

    #print ("Status code: ", response.status_code)


    if response.status_code == 200:

        #Checking if URL is a valid image
        if image_is_in_Spark:
            # Image is in Spark, filename is retrieved from headers
            imgHeaders = response.headers
            #print (imgHeaders)

            if 'image' in imgHeaders['Content-Type']:
                filename = imgHeaders[
                    'Content-Disposition'].replace("attachment; ", "").replace('filename', '').replace('=', '').replace('"', '')
                #Download the image
                with open(filename, 'wb') as f:
                    f.write(response.content)
            else:
                print(image_url + " is not an image")
                exit()
        else:
            response = requests.head(image_url)
            if 'image' not in response.headers.get('content-type'):
                filename = image_url.split("/")[-1]
                rint(image_url + " is not an image")
                exit()
        #Image is valid, let's analyse it with Google Vision API
        print ("\n********************** Analyzing Image **********************")

        if image_is_in_Spark:
            #Image is in Spark, we will download it locally and then send to Google Cloud

            lines = detect_web(filename)
            if len(lines) > 1:
                myStr = '\n'.join(lines)
                print (myStr)

            lines = detect_text(filename)
            if len(lines) > 1:
                myStr = '\n'.join(lines)
                print (myStr)

            lines = detect_faces(filename)
            if len(lines) > 1:
                myStr = '\n'.join(lines)
                print (myStr)

            lines = detect_labels(filename)
            if len(lines) > 1:
                myStr = '\n'.join(lines)
                print (myStr)

            lines = detect_landmarks(filename)
            if len(lines) > 1:
                myStr = '\n'.join(lines)
                print (myStr)

            lines = detect_logos(filename)
            if len(lines) > 1:
                myStr = '\n'.join(lines)
                print (myStr)

        else:
            #Image is not in Spark, we will send the URL to Google Cloud directly
            lines = detect_web_uri(image_url)
            if len(lines) > 1:
                myStr = '\n'.join(lines)
                print (myStr)

            lines = detect_text_uri(image_url)
            if len(lines) > 1:
                myStr = '\n'.join(lines)
                print (myStr)

            lines = detect_faces_uri(image_url)
            if len(lines) > 1:
                myStr = '\n'.join(lines)
                print (myStr)

            lines = detect_labels_uri(image_url)
            if len(lines) > 1:
                myStr = '\n'.join(lines)
                print (myStr)

            lines = detect_landmarks_uri(image_url)
            if len(lines) > 1:
                myStr = '\n'.join(lines)
                pprint (myStr)

            lines = detect_logos_uri(image_url)
            if len(lines) > 1:
                myStr = '\n'.join(lines)
                print (myStr)

    else:
        print ("Invalid URL: ", image_url)
