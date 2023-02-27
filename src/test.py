#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: test.py                       #
# Version: 1.0.0                      #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/1/10            #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/2/5       #
# ################################### #

from liberty import Liberty


lib = Liberty(filepath='./test.json')
print('\n--------------------------------------\n')

print(lib.name)
print(lib.list_attributes())
print(lib.get_attribute('technology'))
print(lib.get_attributes(['technology', 'delay_model']))
print(lib.list_cells())
print(lib.get_cells())
print('\n--------------------------------------\n')

cell = lib.get_cell(lib.list_cells()[0])
print(cell.name)
print(cell.list_attributes())
print(cell.get_attribute('cell_footprint'))
print(cell.get_attributes(['cell_footprint', 'area']))
print(cell.list_pins())
print(cell.get_pins())
print(cell.list_input_pins())
print(cell.get_input_pins())
print(cell.list_output_pins())
print(cell.get_output_pins())
print(cell.list_inout_pins())
print('\n--------------------------------------\n')

pin = cell.get_pin(cell.list_output_pins()[0])
print(pin.name)
print(pin.list_attributes())
print(pin.get_attribute('related_power_pin'))
print('\n--------------------------------------\n')