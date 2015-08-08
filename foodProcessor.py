# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import sys
import glob
import argparse
import codecs
import yaml
import yamlordereddictloader
import markdown
from multiprocessing import Pool
from distutils.dir_util import copy_tree as cp_r
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

def handle_args():
    global i,o
    parser = argparse.ArgumentParser(description='process a folder of recipes into a static site')
    parser.add_argument("input", help="the folder of (YAML) recipes to process")
    parser.add_argument("output", help="the destination folder for output")
    args = parser.parse_args()
    i = fullpath(args.input)
    o = fullpath(args.output)

def fullpath(path):
    return os.path.realpath(os.path.expanduser(path))

def check_destination(target):
    if not os.path.exists(target): os.makedirs(target)

def gather():
    return glob.glob(os.path.join(i,'*.recipe'))

def process_food(files):
    pool = Pool(3)
    recipes = pool.map(handle_recipe,files)
    pool.close()
    pool.join()
    return recipes

def handle_recipe(recipe_path):
    return Recipe(recipe_path).process()

def copy_statics():
    cp_r(os.path.join(i,'copy'), o)

def process_site(recipes):
    env = Environment(
            loader=FileSystemLoader(os.path.join(i,'templates')),
            trim_blocks=True
            )
    index = env.get_template('index.html')
    recipe = env.get_template('recipe.html')
    write_html(
            index.render(recipes=recipes),
            'index.html'
            )
    for r in recipes:
        write_html(
                recipe.render(recipe=r),
                "{}.html".format(r.name)
                )

def write_html(html,dest):
    with codecs.open(os.path.join(o,dest),'w',encoding='utf8') as f:
        f.write(html)

def main():
    handle_args()
    check_destination(o)
    recipes = process_food(gather())
    process_site(recipes)

class Recipe(object):

    def __init__(self,path):
        self.mkdn = []
        self.path = path

    def process(self):
        yaml = self.load()
        self.name = yaml.pop('name')
        self.process_dict(yaml,2)
        return self

    def process_dict(self,d,depth):
        for k,v in d.items():
            if isinstance(v, str):
                self.process_ingredient(k,v)
            elif isinstance(v, dict):
                self.print_headers(depth+1,k)
                self.add_space()
                self.process_dict(v,depth+1)
                self.add_space()
            elif isinstance(v, list):
                self.print_headers(depth+1,k)
                self.add_space()
                self.process_list(v)

    def process_list(self,l):
        for line in l:
            self.mkdn.append(line)
            self.add_space()

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
            return "**{main}** _{adj}_".format(main=ii[0], adj=ii[1])
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
            try:
                number = float(number)
            except ValueError,e:
                print "Error processing {}, {}".format(self.path,e)
                sys.exit(1)
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

    def markdown(self):
        return "\n".join(self.mkdn)

    def html(self):
        return markdown.markdown(self.markdown())

    def print_headers(self,h,k):
        self.mkdn.append("{h}{k}".format(h="#"*h,k=k))

    def add_space(self):
        if not self.mkdn[-1] == "":
            self.mkdn.append("")

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


if __name__ == '__main__':
    main()
