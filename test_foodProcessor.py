# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
import foodProcessor as fp
from foodProcessor import Recipe as R

def test_read_basic_recipe():
    r = R('test/simple.recipe')
    yaml = r.load('test/simple.recipe')
    assert yaml['name'] == 'apple pie'
    assert yaml['what'] == { 'flour': '2 c' }
    assert yaml['how']  == [ 'Preheat oven to 425°F / 220°C' ]

def test_expand_amount_measure():
    r = R('')
    assert r.expand_amount_measure('ml') == 'milliliter'
    assert r.expand_amount_measure('c') == 'cup'
    assert r.expand_amount_measure('t') == 'teaspoon'
    assert r.expand_amount_measure('T') == 'tablespoon'
    assert r.expand_amount_measure('p') == ''
    assert r.expand_amount_measure('foo') == None

def test_expand_ingredient_amount():
    assert R.expand_ingredient_amount('2 c') == '2 cups'
    assert R.expand_ingredient_amount('0.5 t') == '0.5 teaspoon'
    assert R.expand_ingredient_amount('2 pinches') == '2 pinches'
    assert R.expand_ingredient_amount('!') == None

def test_expand_ingredient_name():
    assert R.expand_ingredient_name('flour - sifted') == '**flour** *sifted*'
    assert R.expand_ingredient_name('sugar') == '**sugar**'
    assert R.expand_ingredient_name('sugar - with - dashes') == '**sugar** *with - dashes*'

# def test_process_ingredient():
#     assert fp.process_ingredient('flour: 2 c'.split(':')) == '- 2 cups **flour**'
#     assert fp.process_ingredient('sugar: !'.split(':')) == '- sugar'
#     assert fp.process_ingredient('berries - halved: 1 g'.split(':')) == '- 1 gram **berries** *halved*'

def test_process_ingredients():
    test_data = {'flour - sifted': '2 c', 'sugar': '100 g'}
    result_data = ['- 2 cups **flour** *sifted*', '- 100 grams **sugar**']
    assert R.process_ingredient_batch(test_data) == result_data
