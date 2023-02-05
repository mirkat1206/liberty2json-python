#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: liberty2json.py               #
# Version: 1.0                        #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/1/2             #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/1/9       #
# ################################### #

import os
import glob
import json


class liberty2json():
    """Convert Liberty library files to JSON files.
    
    Args:
        filepath (str)  : Path to a single Liberty library file.
        dirpath (str)   : Path to a directory containing Liberty library files.
        outdir (str)    : Output directory for JSON files.
        tab (str)       : Indentation string for JSON output.
    """
    def __init__(self, filepath='', dirpath='', outdir='./out/', tab='  '):
         # create output directory if it does not exist
        if os.path.exists(outdir) == False:
            os.mkdir(outdir)

        self.filepath = filepath
        self.dirpath = dirpath
        self.outdir = outdir
        self.tab = tab
        self.lines = []

        if self.filepath != '':
            self.to_json(self.filepath)
        
        if self.dirpath != '':
            for filepath in glob.glob(self.dirpath + '/*.lib'):
                self.to_json(filepath)

    def set_outdir(self, outdir):
        """Set output directory for JSON files.
        
        Args:
            outdir (str): Output directory for JSON files.
        """        
        self.outdir = outdir

    def to_json(self, libpath):
        """Convert a single Liberty library file to JSON and write it to a file.
        
        Args:
            libpath (str): Path to the Liberty library file.
        """
        # set outpath
        outpath = os.path.basename(libpath)
        outpath = outpath[:outpath.find('.')]
        outpath = self.outdir + '/' + outpath + '.json'

        # return if .json algready exists
        if os.path.exists(outpath):
            print(f'Already exists: {outpath}')
            return

        # parse .lib
        self.lines = self._parse(libpath)
        _, library_content, _, _ = self._parse_group(0)

        # write .json
        with open(outpath, 'w') as fout:
            fout.write(json.dumps(library_content, indent=self.tab))
            print(f'Finished writing: {outpath}')

    def _is_group(self, line):
        """Check if the line indicates the start of a group.
        
        Args:
            line (str): Line from the Liberty library file.
        
        Returns:
            bool: True if the line indicates the start of a group, False otherwise.
        """
        return line[-1] == '{'

    def _is_endgroup(self, line):
        """Check if the line indicates the end of a group.
        
        Args:
            line (str): Line from the Liberty library file.
        
        Returns:
            bool: True if the line indicates the end of a group, False otherwise.
        """
        return line[-1] == '}'

    def _is_attribute(self, line):
        """Check if the line is an attribute statement.
        
        Args:
            line (str): Line from the Liberty library file.
        
        Returns:
            bool: True if the line is an attribute statement, False otherwise.
        """
        return line[-1] == ';' and line.find('define') == -1

    def _is_define(self, line):
        """Check if the line is a define statement.
        
        Args:
            line (str): Line from the Liberty library file.
        
        Returns:
            bool: True if the line is a define statement, False otherwise.
        """
        return line[-1] == ';' and line.find('define') != -1

    def _parse_group(self, idx):
        """Parse the lines in a group.
        
        Args:
            idx (int): Current line index.
        
        Returns:
            int : Next line index after the group.
            dict: Group content in the form of a dictionary.
            str : Group type.
            str : Group name.
        
        Raises:
            AssertionError: If the group has the wrong format.
        """
        if self._is_group(self.lines[idx]) == False:
            raise AssertionError(f'Error: wrong format of group description of '
                                 f'{self.current_libpath} at line {idx}: {self.lines[idx]}')
        # initialize
        parent_content = {}
        
        # get group type/name
        parent_type = self.lines[idx]
        parent_type = parent_type[:parent_type.find('(')].strip()
        parent_name = self.lines[idx]
        parent_name = parent_name[parent_name.find('(') + 1:parent_name.rfind(')')]
        parent_name = parent_name.replace('\"', '')

        # set alias
        parent_content[parent_type] = {}
        parent_content[parent_type][parent_name] = {}
        content = parent_content[parent_type][parent_name]

        # get childgroups/attributes/defines
        idx += 1
        while True:
            if self._is_group(self.lines[idx]): # get subgroups
                idx, child_content, child_type, child_name = self._parse_group(idx)
                if child_name == "":
                    if child_type in content.keys():
                        content[child_type].append(child_content[child_type][child_name])
                    else:
                        content[child_type] = [child_content[child_type][child_name]]
                else:
                    if child_type in content.keys():
                        content[child_type][child_name] = child_content[child_type][child_name]
                    else:
                        content[child_type] = {}
                        content[child_type][child_name] = child_content[child_type][child_name]
            elif self._is_attribute(self.lines[idx]): # get subattributes
                line =  self.lines[idx]
                if line.find(':') != -1:
                    attr_type = line[:line.find(':')].strip()
                    attr_value = line[line.find(':') + 1:line.find(';')].strip()
                    attr_value = attr_value.replace('\"', '')
                    if attr_type in content.keys():
                        raise AssertionError(f'Error: the attribute {attr_type} has already defined\n')
                    else:
                        content[attr_type] = attr_value
                else:
                    attr_type = line[:line.find('(')].strip()
                    attr_value = line[line.find('(') + 1:line.find(')')].strip()
                    attr_value = attr_value.replace('\"', '')
                    if attr_type in content.keys():
                        content[attr_type].append(attr_value)
                    else:
                        content[attr_type] = []
                        content[attr_type].append(attr_value)
            elif self._is_define(self.lines[idx]): # ignore defines
                pass
            elif self._is_endgroup(self.lines[idx]):
                break
            else:
                raise AssertionError(f'Wrong format of {self.current_libpath} ' + 
                                     f'at line {idx}: {self.lines[idx-1]}\n{self.lines[idx]}')
            idx += 1

        # if only one element exist in a list, turn list into non-list
        for child_type in content.keys():
            if type(content[child_type]) is list:
                if len(content[child_type]) == 1 :
                    content[child_type] = content[child_type][0]

        return idx, parent_content, parent_type, parent_name

    def _check_endofline(self, lines):
        """Check if the end of line is either '{' or '}' or ';'.
        
        Args:
            line (str)  : Line from the Liberty library file.
            idx (int)   : Current line index.
        
        Returns:
            bool: True if the end of line is either '{' or '}' or ';', False otherwise.
        
        Raises:
            AssertionError: If the end of line is not '{' nor '}' nor ';'.
        """        
        for idx, line in enumerate(lines):
            if (self._is_group(line) or self._is_endgroup(line) or self._is_attribute(line) or self._is_define(line)) is False:
                raise AssertionError(f'Error: wrong format of {self.current_libpath} ' +
                                     f'at line {idx}: {line}')

    def _parse(self, filepath):
        """Parse the lines in a Liberty library file, and remove the redundant characters.
        
        Args:
            libpath (str): Path to the Liberty library file.
        
        Returns:
            list: Lines from the Liberty library file.
        """        
        with open(filepath) as f:
            lines = f.read()

            # remove redundant characters
            lines = lines.replace('\t', '')
            lines = lines.replace('\\\n', '')
            
            # remove comment
            while lines.find('/*') != -1:
                lines = lines[:lines.find('/*')] + lines[lines.find('*/') + 2:]
            
            # split lines
            lines = lines.replace('{', '{\n')
            lines = lines.splitlines()
            lines = [line.strip() for line in lines if len(line.strip()) > 0]
            
            # check format
            self._check_endofline(lines)
        return lines


if __name__ == '__main__':
    # method 1
    lib2json = liberty2json(
        filepath='./test.lib',
        outdir='.'
    )
    # method 2
    lib2json = liberty2json()
    lib2json.set_outdir('.')
    lib2json.to_json('./test.lib')