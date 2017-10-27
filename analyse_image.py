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


#image_url = "https://api.ciscospark.com/v1/contents/Y2lzY29zcGFyazovL3VzL0NPTlRFTlQvMjNiYWRmMjAtYmFmNi0xMWU3LWEwYTEtMTU0ODdmM2MyYzQ3LzA"
#image_url = "https://upload.wikimedia.org/wikipedia/commons/c/c0/Opera_House_and_ferry._Sydney.jpg"
image_url = "http://justfunfacts.com/wp-content/uploads/2015/11/sydney-opera-house-2.jpg"


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

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))
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

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))
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
    print('Labels:')

    for label in labels:
        print(label.description)
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
    print('Labels:')

    for label in labels:
        print(label.description)
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
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude'.format(lat_lng.latitude))
            print('Longitude'.format(lat_lng.longitude))
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
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
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
    print('Logos:')

    for logo in logos:
        print(logo.description)
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
    print('Logos:')

    for logo in logos:
        print(logo.description)
# [END def_detect_logos_uri]


# [START def_detect_safe_search]
def detect_safe_search(path):
    """Detects unsafe features in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_safe_search_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Safe search:')

    print('adult: {}'.format(likelihood_name[safe.adult]))
    print('medical: {}'.format(likelihood_name[safe.medical]))
    print('spoofed: {}'.format(likelihood_name[safe.spoof]))
    print('violence: {}'.format(likelihood_name[safe.violence]))
    # [END migration_safe_search_detection]
# [END def_detect_safe_search]


# [START def_detect_safe_search_uri]
def detect_safe_search_uri(uri):
    """Detects unsafe features in the file located in Google Cloud Storage or
    on the Web."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Safe search:')

    print('adult: {}'.format(likelihood_name[safe.adult]))
    print('medical: {}'.format(likelihood_name[safe.medical]))
    print('spoofed: {}'.format(likelihood_name[safe.spoof]))
    print('violence: {}'.format(likelihood_name[safe.violence]))
# [END def_detect_safe_search_uri]


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
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
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
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
# [END def_detect_text_uri]


# [START def_detect_properties]
def detect_properties(path):
    """Detects image properties in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_image_properties]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:')

    for color in props.dominant_colors.colors:
        print('fraction: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))
    # [END migration_image_properties]
# [END def_detect_properties]


# [START def_detect_properties_uri]
def detect_properties_uri(uri):
    """Detects image properties in the file located in Google Cloud Storage or
    on the Web."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print('Properties:')

    for color in props.dominant_colors.colors:
        print('frac: {}'.format(color.pixel_fraction))
        print('\tr: {}'.format(color.color.red))
        print('\tg: {}'.format(color.color.green))
        print('\tb: {}'.format(color.color.blue))
        print('\ta: {}'.format(color.color.alpha))
# [END def_detect_properties_uri]


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

    if notes.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved'.format(
               len(notes.pages_with_matching_images)))

        for page in notes.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if notes.full_matching_images:
        print ('\n{} Full Matches found: '.format(
               len(notes.full_matching_images)))

        for image in notes.full_matching_images:
            print('Url  : {}'.format(image.url))

    if notes.partial_matching_images:
        print ('\n{} Partial Matches found: '.format(
               len(notes.partial_matching_images)))

        for image in notes.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if notes.web_entities:
        print ('\n{} Web entities found: '.format(len(notes.web_entities)))

        for entity in notes.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))
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

    if notes.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved'.format(
               len(notes.pages_with_matching_images)))

        for page in notes.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if notes.full_matching_images:
        print ('\n{} Full Matches found: '.format(
               len(notes.full_matching_images)))

        for image in notes.full_matching_images:
            print('Url  : {}'.format(image.url))

    if notes.partial_matching_images:
        print ('\n{} Partial Matches found: '.format(
               len(notes.partial_matching_images)))

        for image in notes.partial_matching_images:
            print('Url  : {}'.format(image.url))

    if notes.web_entities:
        print ('\n{} Web entities found: '.format(len(notes.web_entities)))

        for entity in notes.web_entities:
            print('Score      : {}'.format(entity.score))
            print('Description: {}'.format(entity.description))
# [END def_detect_web_uri]


# [START def_detect_crop_hints]
def detect_crop_hints(path):
    """Detects crop hints in an image."""
    client = vision.ImageAnnotatorClient()

    # [START migration_crop_hints]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)

    crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in hint.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
    # [END migration_crop_hints]
# [END def_detect_crop_hints]


# [START def_detect_crop_hints_uri]
def detect_crop_hints_uri(uri):
    """Detects crop hints in the file located in Google Cloud Storage."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in hint.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
# [END def_detect_crop_hints_uri]


# [START def_detect_document]
def detect_document(path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    # [START migration_document_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    for page in document.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)

            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)

            block_text = ''
            for symbol in block_symbols:
                block_text = block_text + symbol.text

            print('Block Content: {}'.format(block_text))
            print('Block Bounds:\n {}'.format(block.bounding_box))
    # [END migration_document_text_detection]
# [END def_detect_document]


# [START def_detect_document_uri]
def detect_document_uri(uri):
    """Detects document features in the file located in Google Cloud
    Storage."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    for page in document.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)

            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)

            block_text = ''
            for symbol in block_symbols:
                block_text = block_text + symbol.text

            print('Block Content: {}'.format(block_text))
            print('Block Bounds:\n {}'.format(block.bounding_box))
# [END def_detect_document_uri]

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
            else:
                print(str(filename) + " is not an image")
                exit()
        else:
            response = requests.head(image_url)
            if 'image' not in response.headers.get('content-type'):
                filename = image_url.split("/")[-1]
                rint(str(filename) + " is not an image")
                exit()
        #Image is valid, let's analyse it with Google Vision API
        print ("\n********************** Analysing Image **********************")

        if image_is_in_Spark:
            #Image is in Spark, we will download it locally and then send to Google Cloud
            with open(filename, 'wb') as f:
                f.write(response.content)

            print ("\n\nDetecting web entities")
            detect_web(filename)

            print ("\n\nDetecting text from local image")
            detect_text(filename)

        else:
            #Image is not in Spark, we will send the URL to Google Cloud directly
            print ("\n\nDetecting web entities")
            detect_web_uri(image_url)

            print ("\n\nDetecting text from URI")
            detect_text_uri(image_url)

    else:
        print ("Invalid URL: ", image_url)