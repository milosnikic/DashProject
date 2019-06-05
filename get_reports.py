import codecs
import os
import json
import requests
import pandas as pd

milos = 'https://crowdsensing.elab.fon.bg.ac.rs/controller.php?action=vratiMac&mac=1C:15:1F:A3:D5:5E'
nikola = 'https://crowdsensing.elab.fon.bg.ac.rs/controller.php?action=vratiMac&mac=50:04:B8:71:D9:33'
kristina = 'https://crowdsensing.elab.fon.bg.ac.rs/controller.php?action=vratiMac&mac=B4:CE:F6:80:3F:41'

urls = [milos, nikola, kristina]


def save_reports_to_file(urls):
    for i, url in enumerate(urls):
        with open(str(i) + '_report.json', 'w') as f:
            text = ''
            response = requests.get(url, verify=False)
            text += response.text
            f.write(text)


def load_file_to_json(file):
    with open(file, 'r') as f:
        text = f.read()
        json_obj = json.loads(text)
    return json_obj


# save_reports_to_file(urls)
pd.options.display.max_columns = None
# print(pd.read_json('0_report.json'))
# print(pd.read_json('1_report.json').head())
# print(pd.read_json('2_report.json').head())
