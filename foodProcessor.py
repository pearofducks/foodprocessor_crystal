# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import yaml
import markdown
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

src = ""
dst = ""

def import_recipe(path):
    return parse_yaml(read_file(path))

def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except Exception,e:
        print "{error} when loading recipe {name}".format(error=e,name=path)

def parse_yaml(text):
    try:
        return yaml.load(text)
    except Exception,e:
        print "{error} when parsing YAML".format(error=e)

def process_dict(d):
    i = d.items()[0]
    if type(i) == type('str'):
        process_ingredient_batch(d)
    elif type(i) == type('dict'):
        process_dict(d)

# this will receive a hash of ingredients to be made into a UL
def process_ingredient_batch(d):
    ul = []
    for i in d.items():
        ul.append(process_ingredient(i))
    return ul


# takes a tuple
def process_ingredient(p):
    amount = expand_amount(p[1])
    if amount is not None:
        return "- {amt} {ing}".format(
            amt=amount,
            ing=expand_ingredient(p[0])
            )
    else:
        return "- {ing}".format(
            ing=p[0]
            )

def expand_ingredient(i):
    ii = [x.strip() for x in i.split('-',1)]
    if len(ii) == 2:
        return "**{main}** *{adj}*".format(main=ii[0], adj=ii[1])
    else:
        return "**{main}**".format(main=i)


def expand_amount(a):
    a = a.strip()
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
