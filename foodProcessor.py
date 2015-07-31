# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import yaml
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

src = ""
dst = ""

def read_recipe(path):
    try:
        with open(path) as f:
            return f.read()
    except Exception,e:
        print "{error} when loading recipe {name}".format(error=e,name=path)

def transform(item):
    for v in item.values():
        if type(v) == type('str'):
            process_ingredient(v)

# takes a tuple
def process_ingredient(i):
    expand_amount(b[1])
    # flip
    # bold ingredient name
    # expand letter
    # handle dashes (to italics)

def expand_amount(a):
    if a == '!':
        return ''
    number, measure = a.split(' ', 1)
    resulting_measure = expand_measure(measure)
    try:
        number = int(number)
    except ValueError:
        number = float(number)
    if resulting_measure is None:
        measure = measure
    elif number > 1:
        measure = resulting_measure + 's'
    else:
        measure = resulting_measure
    return "{n} {m}".format(n=number,m=measure)

def expand_measure(m):
    return {
            'c': 'cup',
            't': 'teaspoon',
            'T': 'tablespoon',
            'ml': 'milliliter',
            'g': 'gram',
            'p': ''
            }.get(m,None)

def parse_yaml(text):
    return yaml.load(text)

def handle_args():
    parser = argparse.ArgumentParser(description='process a folder of recipes into a static site')
    parser.add_argument("input", help="the folder of (YAML) recipes to process")
    parser.add_argument("output", help="the destination folder for output")
    args = parser.parse_args()
    src = fullpath(args.input)
    dst = fullpath(args.output)

def fullpath(path):
    return os.path.realpath(os.path.expanduser(path))

def check_destination(target):
    if not os.path.exists(target): os.makedirs(target)

def gather():
    return [os.path.basename(f) for f in glob.glob(os.path.join(src,'*.recipe'))]

def process_raw(files):
    pool = Pool(3)
    recipes = pool.map(handle_recipe,files)
    pool.close()
    pool.join()
    return recipes

def handle_recipe(recipe_path):
    return recipe

def main():
    handle_args()
    go()
