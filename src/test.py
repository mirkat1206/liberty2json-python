#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: test.py                       #
# Version: 1.0                        #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/1/10            #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/1/10       #
# ################################### #

import json
from liberty import liberty

lib = liberty(filepath='./test.json')
print('\n--------------------------------------\n')

print(lib.name)
print(lib.list_attributes())
print(lib.get_attribute('technology'))
print(lib.get_attributes(['technology', 'delay_model']))
print(lib.list_cells())
print(lib.get_cells())
print('\n--------------------------------------\n')

cel = lib.get_cell(lib.list_cells()[0])
print(cel.name)
print(cel.list_attributes())
print(cel.get_attribute('cell_footprint'))
print(cel.get_attributes(['cell_footprint', 'area']))
print(cel.list_pins())
print(cel.get_pins())
print(cel.list_input_pins())
print(cel.get_input_pins())
print(cel.list_output_pins())
print(cel.get_output_pins())
print(cel.list_inout_pins())
print('\n--------------------------------------\n')

pinn = cel.get_pin(cel.list_output_pins()[0])
print(pinn.name)
print(pinn.list_attributes())
print(pinn.get_attribute('related_power_pin'))
print('\n--------------------------------------\n')