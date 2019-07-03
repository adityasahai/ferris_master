import json
from random import randint
import requests
import imghdr
import os
import re


class DownloadImage:
    def __init__(self, product_file, image_path, dummy_image):
        with open(product_file, 'r') as f:
            self.product_json = json.loads(f.read())
        self.filenames = set()
        self.image_path = image_path
        self.dummy_image = dummy_image

    def populate_image(self):
        for product in self.product_json:
            if self.is_valid_url(product["images_url"]):
                product["image_file"] = self.get_image(product["images_url"])
            else:
                product["image_file"] = self.get_dummy_image()

    def save_product_json(self):
        with open('product_data_json_with_images.json',
                  'w') as f:
            f.write(json.dumps(self.product_json))

    def gen_file_name(self):
        string = []
        for _ in range(6):
            string.append(chr(ord('a') + randint(0, 25)))
        f_name = ''.join(string)
        if f_name not in self.filenames:
            self.filenames.add(f_name)
            return f_name
        else:
            return self.gen_file_name()

    def get_image(self, url):
        f_name = self.gen_file_name()
        r = requests.get(url)
        filepath = '{}/{}'.format(self.image_path, f_name)
        with open(filepath, 'wb') as f:
            f.write(r.content)
        file_format = imghdr.what(filepath)
        if file_format is not None:
            new_filename = '{}.{}'.format(filepath, file_format)
            os.rename(filepath, new_filename)
            return new_filename
        else:
            return self.get_dummy_image()

    def is_valid_url(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

    def get_dummy_image(self):
        return '{}/{}'.format(self.image_path, self.dummy_image)
