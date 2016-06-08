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
def head (file, n=10, ignore_hashtag_line=False):
    with open(file, "r") as f:
        line_num = 0
        while (line_num < n):
            try:
                line = next(f)[:-1]
                if ignore_hashtag_line and line[0] == "#":
                    continue
                print (line)
                line_num+=1
            
            except StopIteration:
                print ("Only {} lines in the file".format(line_num))
                break         
 
# Print a range of lines in a file according to a list of start end lists 
def linerange (file, range_list=[[0,10]]):
    for start, end in (range_list):
        found_first_line = found_last_line = False
        with open(file, "r") as f:
            for n, line in enumerate(f):
                if n >= start:
                    found_first_line = True
                    print ("{}\t{}".format(n, line[0:-1]))
                if n >= end:
                    found_last_line = True
                    break
            if found_first_line == False:
                print ("Start coordinate out of line range: {}".format(start))
            if found_last_line == False:
                print ("End coordinate out of line range: {}".format(end))
            print()

# Efficient way to count the number of lines in a file
def linecount(file):
    f = open(file)                  
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)
    return lines    

# Def to transform a dict into a markdown formated table
def dict_to_md (
    d,
    key_label="",
    value_label="",
    transpose=False,
    sort_by_key=False,
    sort_by_val=True,
    max_items=None):
    
    #Function imports
    from collections import OrderedDict
    
    if sort_by_key:
        d = OrderedDict(reversed(sorted(d.items(), key=lambda t: t[0])))
        
    if sort_by_val:
        d = OrderedDict(reversed(sorted(d.items(), key=lambda t: t[1])))
        
    if max_items and len(d)>max_items:
        d2 = OrderedDict()
        n = 0
        for key, value in d.items():
            d2[key]=value
            n+=1
            if n >= max_items:
                break
        d2["..."]="..."
        d=d2
    
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
def colsum (file, colrange=None, separator="", header=False, ignore_hashtag_line=False, max_items=10):
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
            print (dict_to_md(col_dict, header_dict[colnum], "Count", transpose=True, sort_by_val=True, max_items=max_items))
        else:
            print (dict_to_md(col_dict, colnum, "Count", transpose=True, sort_by_val=True, max_items=max_items))


# Reformat a table given an intial and a final line templates indicated as a list where numbers
# indicate the data column and strings the formating characters
# Example initial line = "chr1    631539    631540    Squires|id1    0    +"
# Initial template = [0,"\t",1,"\t",2,"\t",3,"|",4,"\t",5,"\t",6]
# Example final line = "chr1    631539    631540    m5C|-|HeLa|22344696    -    -"
# Final template = [0,"\t",1,"\t",2,"\tm5C|-|HeLa|22344696\t-\t",6]
# A nested dictionnary of substitution per position can also be provided to replace
# specific values by others :
# subst_dict = { 0:{"chr1":"1","chr2":"2"}, 3:{"Squires":"5376774764","Li":"27664684"}}
# in addition a dictionnary of list per position can be provided to fiter out lines 
# with specific values :
# filter_dict =  { 0:["chr2", "chr4"], 1:["46767", "87765"], 5:["76559", "77543"]}

def reformat_table(
    input_file,
    output_file,
    init_template,
    final_template,
    header = '',
    keep_original_header = True,
    replace_internal_space='_',
    replace_null_val="*",
    subst_dict={},
    filter_dict=[]):
    
    with open (input_file, "r") as infile, open (output_file, "w") as outfile:
        
        total = fail = success = filtered_out = 0
        
        if header:
            outfile.write(header)    
        
        for line in infile:
            
            # Original header lines
            if line[0] == "#":
                if keep_original_header:
                    outfile.write(line)                 
                continue
            
            total+=1
            
            # Decompose the original line            
            try:
                raw_val = _decompose_line(
                    line = line,
                    template = init_template)
                assert raw_val, "Decomposing the line #{} resulted in an empty value list:\n{}".format(total,line)
            
            except AssertionError as E:
                fail+=1
                continue
            
            # Filter and clean the values 
            try:
                clean_val = _clean_values(
                    val_list = raw_val,
                    replace_internal_space = replace_internal_space,
                    replace_null_val = replace_null_val,
                    subst_dict = subst_dict,
                    filter_dict = filter_dict)
                assert clean_val, "The line #{} was filter according to the filter dictionnary:\n{}".format(total,line)
            
            except AssertionError as E:
                filtered_out+=1
                continue
            
            # Recompose the line
            formated_line = _reformat_line(
                val_list = clean_val,
                template = final_template)
                
            outfile.write(formated_line)
            success+=1
            
    print ("{} Lines processed\t{} Lines pass\t{} Lines filtered out\t{} Lines fail\n".format(total, success, filtered_out, fail))
    
    
# Helper function for reformat_table. Decompose a line and extract the values given a template list
def _decompose_line(line, template):
    
    val_list = []
    
    # Remove the first element from the line if this is a str
    if type(template[0]) == str:
        val, sep, line = line.partition(template[0])
        template = template[1:]
    
    # Decompose the line
    for element in template:
        if type(element) == str:
            val, sep, line = line.partition(element)
            val_list.append(val)
    
    # Manage last element of the template if it is a number
    if type(template[-1]) == int:
        val_list.append(line)
    
    return val_list


# Helper function for reformat_table. Clean the extracted values
def _clean_values (val_list, replace_internal_space=None, replace_null_val="*", subst_dict={}, filter_dict={}):
    
    for pos in range(len(val_list)):
        val_list[pos] = val_list[pos].strip()
        
        # Replace the empty field by a given char
        if replace_null_val and not val_list[pos]:
            val_list[pos] = replace_null_val
        
        # Replace internal spaces by underscores
        if replace_internal_space:
            val_list[pos] = val_list[pos].replace(" ","_")
        
        # Filter line based on the filter_dict
        if pos in filter_dict:
            if val_list[pos] in filter_dict[pos]:
                return None
                
        if pos in subst_dict:
            # Use the substitution dict exept if the value is not in the dict in this case use the default value 
            if val_list[pos] in subst_dict[pos]:
                val_list[pos] = subst_dict[pos][val_list[pos]]    
    
    return val_list

# Helper function for reformat_table. Reassemble a line from a list of values and a template list
def _reformat_line (val_list, template):
    
    line = ""
    try:
        for element in template:
            if type(element) == str:
                line+=element
            if type(element) == int:
                line+=val_list[element]
    except IndexError as E:
        print (E)
        print (val_list)
        print (template)
        raise
        
    return line+"\n"
