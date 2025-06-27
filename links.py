#!/usr/bin/python3

import argparse
import json
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse

def only_links(href):
    return href and not href.startswith(('mailto:', 'tel:', 'sms:', 'javascript:'))

def absolute_link(href):
    return href.startswith(('http://', 'https://', '//'))

def add_scheme(url, relative_url):
    return f"{urlparse(relative_url).scheme}:{url}"

def split_link(url):
    # assuming the link has format 'http[s]://...'
    third_slash = link.find('/', 8)
    if third_slash != -1:
        return link[:third_slash], link[third_slash:]
    return link, '/'

parser = argparse.ArgumentParser(description='Find links on the given pages')
parser.add_argument('-u', '--url', action='append', help='I will happily eat a url link provided here')
parser.add_argument('-o', '--output', help='In which format do you want me to give you the result?',
                    choices=['stdout', 'json'], default='stdout')

args = parser.parse_args()
input_urls = args.url
use_json = args.output == 'json'

output_urls = {}
for url in input_urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for a_tag in soup.find_all('a', href=only_links):
        link = a_tag.get('href')
        assert link != None

        if absolute_link(link):
            if link.startswith('//'):
                link = add_scheme(link, url)

            base, relative = split_link(link)
            output_urls[base] = output_urls.get(base, []) + [relative]
        else:
            output_urls[url] = output_urls.get(url, []) + [link]
            assert link.find('www') == -1

if use_json:
    js = json.dumps(output_urls, indent=2)
    print(js)

else:
    for base in output_urls:
        for path in output_urls[base]:
            print(base + path)
