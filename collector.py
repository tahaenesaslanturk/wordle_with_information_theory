#!/usr/bin/python
# -*- coding: utf8 -*-

import urllib3
import re

alphabet = u"ABCÇDEFGHIİJKLMNOÖPRSŞTUÜVYZ"

def readPage(letter):
    url = u"http://tr.wiktionary.org/wiki/Vikisözlük:Sözcük_listesi_(" + letter + ")"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        
    }
    
    manager = urllib3.PoolManager()
    response = None
    
    try:
        response = manager.request('GET', url.encode('utf-8'), headers=headers)
        content = response.data.decode('utf-8')
        words = re.findall(r'<li><a[^>]*>([^<]+)<\/a>', content)
        if words:
            words.pop()  # Removing the last unwanted word, if needed
        print("Read the letter ", letter)
        return words
    except urllib3.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return []
    finally:
        if response is not None:
            response.release_conn()

def getWordList():
    words = []
    for letter in alphabet:
        words += readPage(letter)
    return words

def writeToFile(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(getWordList()))

writeToFile("words.txt")