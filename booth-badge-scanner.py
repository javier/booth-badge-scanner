import cv2
import numpy as np
import argparse
import os
import sys
from urllib.parse import urlparse
import requests
import vobject
import csv
from glob import glob
from pyzbar.pyzbar import decode
from PIL import Image

def read_image_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image_array, -1)
    return image

def read_image_from_file(file_path):
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)  # Convert image to grayscale
    if image is not None:
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return image

def decode_qr_code(image):
    pil_image = Image.fromarray(image)
    decoded_objects = decode(pil_image)
    if decoded_objects:
        # Returning decoded text and the raw bytes for potential fallback usage
        return decoded_objects[0].data.decode('utf-8'), decoded_objects[0].data.decode('utf-8')
    return None, None

def read_vcard_from_data(data):
    try:
        return vobject.readOne(data), None
    except vobject.base.ParseError as e:
        print(f"Warning: Partial VCARD detected due to parsing error: {e}")
        return None, data  # Returning None for VCARD and raw data

def process_image_source(source):
    try:
        result = urlparse(source)
        if result.scheme in ['http', 'https']:
            return read_image_from_url(source)
        else:
            return read_image_from_file(source)
    except Exception as e:
        print(f"Failed to process the source {source} with error {e}")
        return None

def output_csv(vcards, raw_data_list, sources):
    fieldnames = ['Source', 'RawData']  # Basic fields
    for vcard in vcards:
        if vcard:
            for line in vcard.contents:
                fieldnames.append(line)
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for vcard, raw_data, source in zip(vcards, raw_data_list, sources):
        row = {'Source': source, 'RawData': raw_data if raw_data else ""}
        if vcard:
            for line in vcard.contents:
                row[line] = vcard.contents[line][0].valueRepr()
        writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description="Extract VCARD from QR codes in images.")
    parser.add_argument('source', nargs='+', help="URL, file path to the image, or a file with a list of them, or a directory.")
    parser.add_argument('--csv', action='store_true', help="Output as CSV to stdout.")
    args = parser.parse_args()

    sources = []
    if os.path.isdir(args.source[0]):
        sources = [os.path.join(args.source[0], f) for f in os.listdir(args.source[0]) if os.path.isfile(os.path.join(args.source[0], f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    elif os.path.isfile(args.source[0]) and not args.source[0].lower().endswith(('.png', '.jpg', '.jpeg')):
        with open(args.source[0], 'r') as file:
            sources = [line.strip() for line in file.readlines()]
    else:
        sources = args.source

    vcards = []
    raw_data_list = []

    for source in sources:
      image = process_image_source(source)
      if image is not None:  # Explicitly check for None
        qr_data, raw_data = decode_qr_code(image)
        if qr_data:
            vcard, raw_fallback_data = read_vcard_from_data(qr_data)
            vcards.append(vcard)
            raw_data_list.append(raw_fallback_data if raw_fallback_data else raw_data)
        else:
            print(f"No QR code found in the image from {source}.")
            vcards.append(None)
            raw_data_list.append(None)
      else:
        print(f"Failed to load image from {source}.")
        vcards.append(None)
        raw_data_list.append(None)

    if args.csv:
        output_csv(vcards, raw_data_list, sources)
    else:
        for vcard, raw_data, source in zip(vcards, raw_data_list, sources):
            print(f"Source: {source}")
            if vcard:
                print("VCARD Information:")
                vcard.prettyPrint()
            elif raw_data:
                print("Raw QR Data:")
                print(raw_data)

if __name__ == '__main__':
    main()


