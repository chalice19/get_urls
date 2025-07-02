#!/usr/bin/python3

import aiohttp
import argparse
import asyncio
import json
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse

output_urls = {}

def only_links(href):
    return href and not href.startswith(('mailto:', 'tel:', 'sms:', 'javascript:'))

def absolute_link(href):
    return href.startswith(('http://', 'https://', '//'))

def add_scheme(url, relative_url):
    return f"{urlparse(relative_url).scheme}:{url}"

def split_link(link):
    # assuming the link has format 'http[s]://...'
    third_slash = link.find('/', 8)
    if third_slash != -1:
        return link[:third_slash], link[third_slash:]
    return link.rstrip('/'), '/'

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

def collect_links(response, url):    
    soup = BeautifulSoup(response, 'html.parser')
    for a_tag in soup.find_all('a', href=only_links):
        link = a_tag.get('href')
        if absolute_link(link):
            if link.startswith('//'):
                link = add_scheme(link, url)

            base, relative = split_link(link)
            output_urls[base] = output_urls.get(base, []) + [relative]
        else:
            output_urls[url] = output_urls.get(url, []) + [link]

async def read_urls(urls): 
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        for i, result in enumerate(results):
            collect_links(result, urls[i])

parser = argparse.ArgumentParser(description='Find links on the given pages')
parser.add_argument('-u', '--url', action='append', help='I will happily eat a url link provided here', required=True)
parser.add_argument('-o', '--output', help='In which format do you want me to give you the result?',
                    choices=['stdout', 'json'], default='stdout')

args = parser.parse_args()
use_json = args.output == 'json'

asyncio.run(read_urls(args.url))

if use_json:
    js = json.dumps(output_urls, indent=2)
    print(js)

else:
    for base in output_urls:
        for path in output_urls[base]:
            print(base + path)
