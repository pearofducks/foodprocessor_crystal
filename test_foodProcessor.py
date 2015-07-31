# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
import foodProcessor

def test_read_basic_recipe():
    text = foodProcessor.read_recipe('test/simple.recipe')
    yaml = foodProcessor.parse_yaml(text)
    assert yaml['name'] == 'apple pie'
    assert yaml['what'] == { 'flour': '2 c' }
    assert yaml['how']  == [ 'Preheat oven to 425°F / 220°C' ]

def test_transform_yaml():
    pass
    # assert foodProcessor.transform({ 'flour': '2 c' }) == '<li>2 cups <strong>flour</strong></li>'

def test_expand_measure():
    assert foodProcessor.expand_measure('ml') == 'milliliter'
    assert foodProcessor.expand_measure('c') == 'cup'
    assert foodProcessor.expand_measure('t') == 'teaspoon'
    assert foodProcessor.expand_measure('T') == 'tablespoon'
    assert foodProcessor.expand_measure('p') == ''
    assert foodProcessor.expand_measure('foo') == None

def test_expand_amount():
    assert foodProcessor.expand_amount('2 c') == '2 cups'
    assert foodProcessor.expand_amount('0.5 t') == '0.5 teaspoon'
    assert foodProcessor.expand_amount('2 pinches') == '2 pinches'
    assert foodProcessor.expand_amount('!') == ''
