# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import yaml
import markdown
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
def process_ingredient(p):
    amount = expand_amount(p[1])
    if amount is not None:
        expand_ingredient(p[0])
        # return the flipped join of the two
    else:
        pass
        # just return p[0]
    # flip
    # bold ingredient name
    # handle dashes (to italics)

def expand_ingredient(i):
    ii = i.split('-')
    if len(ii) == 2:
        return "**{main}** *{adj}*".format(main=ii[0], adj=ii[1])
    else:
        return "**{main}**".format(main=i)


def expand_amount(a):
    if a == '!':
        return None
    number, measure = a.split(' ', 1)
    try:
        number = int(number)
    except ValueError:
        number = float(number)
    expansion = expand_measure(measure)
    if expansion is None:
        measure = measure
    elif number > 1:
        measure = expansion + 's'
    else:
        measure = expansion
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
