# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import yaml
import yamlordereddictloader
import markdown
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

src = ""
dst = ""

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

class Recipe(object):

    def __init__(self,path):
        self.mkdn = []
        self.path = path

    def process(self):
        yaml = self.load()
        self.name = yaml.pop('name')
        self.process_dict(yaml,0)
        print "markdown"
        print "\n".join(self.mkdn)
        print "html"
        print markdown.markdown("\n".join(self.mkdn))

    def print_headers(self,h,k):
        self.mkdn.append("<h{h}>{k}</h{h}>".format(h=h,k=k))

    def process_dict(self,d,depth):
        for k,v in d.items():
            # print "\tk is {kk} and v is {vv}".format(kk=k,vv=v)
            if isinstance(v, str):
                self.process_ingredient(k,v)
            elif isinstance(v, dict):
                self.print_headers(depth+1,k)
                self.process_dict(v,depth+1)
            elif isinstance(v, list):
                self.print_headers(depth+1,k)
                self.process_list(v)

    def process_list(self,l):
        self.mkdn.append("\n".join(l))

    # this will receive a hash of ingredients to be made into a UL
    def process_ingredient(self,k,v):
        amount = self.ingredient_amount(v)
        if amount is not None:
            self.mkdn.append("- {amt} {ing}".format(
                amt=amount,
                ing=self.ingredient_name(k)
                ))
        else:
            self.mkdn.append("- {ing}".format(
                ing=k
                ))

    def ingredient_name(self,i):
        ii = [x.strip() for x in i.split('-',1)]
        if len(ii) == 2:
            return "**{main}** *{adj}*".format(main=ii[0], adj=ii[1])
        else:
            return "**{main}**".format(main=i)


    def ingredient_amount(self,a):
        a = a.strip()
        if a == '!':
            return None
        number, measure = a.split(' ', 1)

        try:
            number = int(number)
        except ValueError:
            number = float(number)

        expansion = self.amount_measure(measure)
        if expansion is None:
            measure = measure
        elif number > 1:
            measure = expansion + 's'
        else:
            measure = expansion

        return "{n} {m}".format(n=number,m=measure)

    def amount_measure(self,m):
        return {
                'c': 'cup',
                't': 'teaspoon',
                'T': 'tablespoon',
                'ml': 'milliliter',
                'g': 'gram',
                'p': ''
                }.get(m,None)

    def load(self):
        return self.parse_yaml(self.read_file(self.path))

    def read_file(self,path):
        try:
            with open(path) as f:
                return f.read()
        except Exception,e:
            print "{error} when loading recipe {name}".format(error=e,name=path)

    def parse_yaml(self,text):
        try:
            return yaml.load(text, Loader=yamlordereddictloader.Loader)
        except Exception,e:
            print "{error} when parsing YAML".format(error=e)
