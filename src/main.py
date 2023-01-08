#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: main.py                       #
# Version: 1.0                        #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/1/2             #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/1/9       #
# ################################### #


import argparse
from liberty2json import liberty2json

parser = argparse.ArgumentParser(description='Turn liberty format file(s) into json format file(s).')
parser.add_argument('--libfile', type=str, help='filepath of a liberty format file')
parser.add_argument('--libdir', type=str, help='dirpath of a directory containing liberty format file(s)')
parser.add_argument('--jsondir', type=str, default='./out/', help='dirpath for output json file(s)')
args = parser.parse_args()

if args.libfile == None and args.libdir == None:
    parser.print_help()
    parser.exit(1)

if args.libfile:
    liberty2json(
        filepath=args.libfile,
        outdir=args.jsondir,
    )

if args.libdir:
    liberty2json(
        dirpath=args.libdir,
        outdir=args.jsondir,
    )