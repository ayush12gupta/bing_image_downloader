from pathlib import Path
import os
import sys
import urllib.request
import urllib
import imghdr
import posixpath
import re
import pandas as pd

'''
Python api to download image form Bing.
Author: Guru Prasad (g.gaurav541@gmail.com)
'''


class Bing:
    def __init__(self, query, limit, output_dir, adult, timeout, links, fname, queries, filters=''):
        self.download_count = 0
        self.query = query
        self.output_dir = output_dir
        self.adult = adult
        self.filters = filters
        self.links = links
        self.file = fname
        if len(fname):
            self.start = int(fname[-1].split('.')[0]) + 1
        else:
            self.start = '1'
        self.queries = queries

        assert type(limit) == int, "limit must be integer"
        self.limit = limit
        assert type(timeout) == int, "timeout must be integer"
        self.timeout = timeout

        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        self.page_counter = 0

    def save_image(self, link, file_path):
        request = urllib.request.Request(link, None, self.headers)
        image = urllib.request.urlopen(request, timeout=self.timeout).read()
        file = file_path.split('/')
        if not imghdr.what(None, image):
            # print('[Error]Invalid image, not saving {}\n'.format(link))
            raise
        with open(file_path, 'wb') as f:
            f.write(image)
            self.file.append(file[-1])
            self.links.append(link)
            self.queries.append(file[-2])

    def download_image(self, link):
        self.download_count += 1

        # Get the image link
        try:
            path = urllib.parse.urlsplit(link).path
            filename = posixpath.basename(path).split('?')[0]
            file_type = filename.split(".")[-1]
            if file_type.lower() not in ["jpe", "jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "webp", "jpg"]:
                file_type = "jpg"

            # Download the image
            # print("[%] Downloading Image #{} from {}".format(self.download_count + int(self.start)-1, link))
#             if link not in self.links:
            self.save_image(link, "{}/{}/{}/".format(os.getcwd(), self.output_dir, self.query) + "{}.{}".format(
                str(self.download_count + int(self.start) - 1), file_type))
            # print("[%] File Downloaded !\n")
#             else:
#                 self.download_count -= 1
#                 print("[!] Duplicate Image")
        except Exception as e:
            self.download_count -= 1
            # print("[!] Issue getting: {}\n[!] Error:: {}".format(link, e))

    def run(self):
        while self.download_count < self.limit:
            print('\n\n[!!]Indexing page: {}\n'.format(self.page_counter + 1))
            # Parse the page source and download pics
            request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(self.query) \
                          + '&first=' + str(self.page_counter) + '&count=' + str(self.limit) \
                          + '&adlt=' + self.adult + '&qft=' + self.filters
            request = urllib.request.Request(request_url, None, headers=self.headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf8')
            links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)

            # print("[%] Indexed {} Images on Page {}.".format(len(links), self.page_counter + 1))
            # print("\n===============================================\n")

            for link in links:
                if self.download_count < self.limit:
                    self.download_image(link)
                else:
                    print("\n\n[%] Done. Downloaded {} images of '{}'.".format(self.download_count, self.query))
                    # print("\n===============================================\n")
                    break

            self.page_counter += 1
    
        return self.links, self.file, self.queries
