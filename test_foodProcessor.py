# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
import foodProcessor as fp
from foodProcessor import Recipe as R

r = R('')
r_simple = R('test/simple.recipe')
r_complex = R('test/test.recipe')
r_numerics = R('test/numeric_instructions.recipe')

def test_read_recipe():
    yaml = r_simple.load()
    assert yaml['name'] == 'apple pie'
    assert yaml['what'] == { 'flour': '2 c' }
    assert yaml['how']  == [ 'Preheat oven to 425°F / 220°C' ]

def test_file_dne():
    r_dne = R('test/does_not_exist')
    yaml = r_dne.load()

def test_file_bad_data():
    r_bad = R('test/bad.recipe')
    yaml = r_bad.load()

def test_file_bad_name():
    r_bad = R('test/bad_name.recipe')
    result = r_bad.process()

def test_amount_measure():
    assert r.amount_measure('ml') == 'milliliter'
    assert r.amount_measure('c') == 'cup'
    assert r.amount_measure('t') == 'teaspoon'
    assert r.amount_measure('T') == 'tablespoon'
    assert r.amount_measure('p') == ''
    assert r.amount_measure('foo') == None

def test_ingredient_amount():
    assert r.ingredient_amount('2 c') == '2 cups'
    assert r.ingredient_amount('0.5 t') == '0.5 teaspoon'
    assert r.ingredient_amount('2 pinches') == '2 pinches'
    assert r.ingredient_amount('!') == None

def test_ingredient_name():
    assert r.ingredient_name('flour - sifted') == '**flour** _sifted_'
    assert r.ingredient_name('sugar') == '**sugar**'
    assert r.ingredient_name('sugar - with - dashes') == '**sugar** _with - dashes_'

def test_process_ingredient():
    r_proc_test = R('')
    value_result_hash = {
        'flour: 2 c': '- 2 cups **flour**',
        'sugar: !': '- sugar',
        'berries - halved: 1 g': '- 1 gram **berries** _halved_',
        }
    for value,result in value_result_hash.items():
        k,v = value.split(':')
        r_proc_test.process_ingredient(k,v)
        assert result in r_proc_test.mkdn
