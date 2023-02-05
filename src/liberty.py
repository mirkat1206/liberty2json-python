#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: liberty.py                    #
# Version: 1.0                        #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/1/4             #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/2/5       #
# ################################### #

import os
import json


class Group():
    def __init__(self, name='', content={}):
        self.content = content
        self.name = name

    def list_attributes(self):
        return [*self.content.keys()]

    def get_attribute(self, attr=''):
        return self.content[attr]
    
    def get_attributes(self, attrs=[]):
        if attrs == []:
            attrs = self.list_attributes()
        if type(attrs) is str:
            attrs = [attrs]
        return {k: v for k, v in self.content.items() if k in attrs}


class Pin(Group):
    def __init__(self, name='', content={}):
        super().__init__(name, content)


class Cell(Group):
    def __init__(self, name='', content={}):
        super().__init__(name, content)

    def list_pins(self):
        return [*self.content['pin'].keys()]

    def get_pin(self, pinname=''):
        return Pin(pinname, self.content['pin'][pinname])

    def get_pins(self, pinnames=[]):
        if pinnames == []:
            pinnames = self.list_pins()
        return {pinname: Pin(pinname, self.content['pin'][pinname]) for pinname in pinnames}

    def list_input_pins(self):
        return [k for k, v in self.content['pin'].items() if v['direction'] == 'input']

    def get_input_pins(self):
        return self.get_pins(self.list_input_pins())
    
    def list_output_pins(self):
        return [k for k, v in self.content['pin'].items() if v['direction'] == 'output']

    def get_output_pins(self):
        return self.get_pins(self.list_input_pins())

    def list_inout_pins(self):
        return [k for k, v in self.content['pin'].items() if v['direction'] == 'inout']

    def get_inout_pins(self):
        return self.get_pins(self.list_input_pins())
    

class Liberty(Group):
    def __init__(self, filepath=''):
        if filepath != '' and os.path.exists(filepath) == False:
            raise AssertionError(f'Error: {filepath} does not exist')
        
        self.filepath = filepath
        if self.filepath != '':
            self.read(filepath)

    def read(self, filepath):
        with open(filepath) as f:
            data = json.load(f)
        name = [*data['library'].keys()][0]
        super().__init__(name, data['library'][name])

    def list_cells(self):
        return [*self.content['cell'].keys()]

    def get_cell(self, cellname=''):
        return Cell(cellname, self.content['cell'][cellname])

    def get_cells(self, cellnames=[]):
        if cellnames == []:
            cellnames = self.list_cells()
        return {cellname: Cell(cellname, self.content['cell'][cellname]) for cellname in cellnames}