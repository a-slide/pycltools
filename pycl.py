# -*- coding: utf-8 -*-

"""
@package pycl
@copyright  [GNU General Public License v2](http://www.gnu.org/licenses/gpl-2.0.html)
@author     Adrien Leger - 2016
* <aleg@ebi.ac.uk>
* [Github](https://github.com/a-slide)
"""

# Sent basic bash command
def bash(cmd):
    from subprocess import Popen, PIPE
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    print(stdout.decode())
    print (stderr.decode())
            
# Emulate linux head cmd 
def head (file, n=10):
	
    with open(file, "r") as f:
        for i in range(n):
            try:
                print (next(f)[:-1])
            except StopIteration:
                print ("Only {} lines in the file".format(i))
                break         
  
# Def to transform a dict into a markdown formated table
def dict_to_md (d, key_label="", value_label="", transpose=False, sort_by_key=False, sort_by_val=False):
    
    #Function imports
    from collections import OrderedDict

    if sort_by_key:
        d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
        
    if sort_by_val:
        d= OrderedDict(sorted(d.items(), key=lambda t: t[1]))
    
    if transpose:
        buffer = "|{}|".format(key_label)
        for key in d.keys():
            buffer += "{}|".format(key)
        buffer += "\n|:---|"
        for _ in range(len(d)):
            buffer += ":---|"
        buffer += "\n|{}|".format(value_label)
        for value in d.values():
            buffer += "{}|".format(value)
        buffer += "\n"
        
    else:
        buffer = "|{}|{}|\n|:---|:---|\n".format(key_label, value_label)
        for key, value in d.items():
            buffer += "|{}|{}|\n".format(key, value)
    
    return buffer


# like split but can take a list of separators instead of a simple separator 
def supersplit (string, separator=""):
    
    if not separator:
        return string.split()
    
    if type(separator) == str:
        return string.split(separator)
    
    for sep in separator:
        string = string.replace(sep, "#")
    return string.split("#")


# Create a summary of selected columns of a file
def colsum (file, colrange=None, separator="", header=False, ignore_hashtag_line=False):
	#Function imports
	from collections import OrderedDict
	
	res_dict = OrderedDict()
	
	with open(file, "r") as f:
		# Manage the first line
		first_line = False
		header_found = False
		while not first_line:
			
			line = next(f)

			if ignore_hashtag_line and line[0] == "#":
				continue
			
			# Split the first line
			ls = supersplit(line, separator)

			if header and not header_found:
				header_dict = {}
				for colnum, val in enumerate(ls):
					header_dict[colnum]= val
				header_found = True
				print("Header found")
				continue
				
			# Get the number of col if not given and handle the first line			
			if not colrange:
				colrange = [i for i in range(len(ls))]
				print("Found {} colums".format(len(ls)))
				
			# Manage the first valid line
			print("First line found")
			for colnum in colrange:
				res_dict[colnum] = OrderedDict()
				val = ls[colnum].strip()
				res_dict[colnum][val]=1
			first_line = True
		
		# Continue to read and parse the lines
		for line in f:
			ls = supersplit(line, separator)
			for colnum in colrange:
				val = ls[colnum].strip()
				if val not in res_dict[colnum]:
					res_dict[colnum][val] = 0
				res_dict[colnum][val]+=1
				
	# Create a Markdown table output per colums
	for colnum, col_dict in res_dict.items():
		if header:
			print (dict_to_md(col_dict, header_dict[colnum], "Count", transpose=True, sort_by_val=True))
		else:
			print (dict_to_md(col_dict, colnum, "Count", transpose=True, sort_by_val=True))
