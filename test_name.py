import os
import argparse
from pprint import pprint
import io
import multiprocessing as mp
import urllib
from urllib.request import Request, urlopen
from pyresparser import ResumeParser
from pyresparser.utils import extract_text

file_path = 'Cv_TahaHasan.pdf'
text_raw = extract_text(file_path, '.pdf')

print('--- Extracted Text Start ---')
print(text_raw)
print('--- Extracted Text End ---')

def get_remote_data():
    try:
        remote_file = 'https://github.com/tahahasan01/pyresparser/raw/master/Cv_TahaHasan.pdf'
        print('Extracting data from: {}'.format(remote_file))
        req = Request(remote_file, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        _file = io.BytesIO(webpage)
        _file.name = remote_file.split('/')[-1]
        resume_parser = ResumeParser(_file)
        return [resume_parser.get_extracted_data()]
    except urllib.error.HTTPError:
        return 'File not found. Please provide correct URL for resume file.'


def get_local_data():
    data = ResumeParser('Cv_TahaHasan.pdf').get_extracted_data()
    return data


def test_for_name():
    data = get_local_data()
    assert 'Taha Hasan' == data[0]['name']
    data = get_remote_data()
    assert 'Taha Hasan' == data[0]['name']


def test_for_email():
    data = get_remote_data()
    assert 'tahahasan279@gmail.com' == data[0]['email']


def main():
    test_for_name()
    test_for_email()


if __name__ == '__main__':
    main()
