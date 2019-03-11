""" Demo 2: processing folder with HTML files """

import os
import multiprocessing
from functools import partial
from itertools import chain

import html2sent

if __name__ == '__main__':
    this_folder = os.path.dirname(os.path.realpath(__file__))
    folder_with_html_files = os.path.join(this_folder, 'demo_htmls')
    fnames = [entry.path for entry in os.scandir(folder_with_html_files)]
    html_contents = [open(fname).read() for fname  in fnames]
    pool = multiprocessing.pool.Pool()
    tokenize_rus = partial(html2sent.tokenize, language='russian')
    sentences = pool.map(tokenize_rus, html_contents)
    sentences = sum(sentences, [])  # convert list-of-lists to a list
    # alt: sentences = list(itertools.chain(*sentences))
    text = '\n'.join(sentences)
    print(text)

