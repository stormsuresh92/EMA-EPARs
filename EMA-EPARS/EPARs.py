import requests
import logging
import time
import os
from alive_progress import alive_bar


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
    }

logging.basicConfig(filename='Logfile.log', level=logging.DEBUG, 
                    format='%(asctime)s-%(message)s', datefmt='%d-%b-%y %H-%M-%S')

print('WRITING PDF FILES...')
cur_dir = os.getcwd()
pdf = cur_dir + '/Downloaded Labels'
if not os.path.exists(pdf):
    os.mkdir(pdf)

with alive_bar(1860, bar='classic2', spinner='classic') as bar:   
    with open('Input.txt') as file:
        for url in file:
            epar_name = url.strip().split('/')[-1]
            base = 'https://www.ema.europa.eu/en/documents/product-information/'
            endpoint = '-epar-product-information_en.pdf'
            constructed_url = base + epar_name + endpoint
            r = requests.get(constructed_url, stream=True, headers=headers)
            with open(pdf + '/' + epar_name + '.pdf', 'wb') as f:
                f.write(r.content)
                time.sleep(1)
                bar()
        

input()
