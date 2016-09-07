# -*- coding: utf-8 -*-

"""
@package pycl
@copyright  [GNU General Public License v2](http://www.gnu.org/licenses/gpl-2.0.html)
@author     Adrien Leger - 2016
* <aleg@ebi.ac.uk>
* [Github](https://github.com/a-slide)
"""

# Strandard library imports
from os import access, R_OK, remove, path
from os import mkdir as osmkdir
from gzip import open as gopen
from shutil import copy as shutilCopy
from shutil import Error as shutilError
from sys import stdout
from collections import OrderedDict
from subprocess import Popen, PIPE
import gzip

#~~~~~~~ PREDICATES ~~~~~~~#

def is_readable_file (fp):
    """ Verify the readability of a file or list of file """
    if not access(fp, R_OK):
        raise IOError ("{} is not a valid file".format(fp))

def is_gziped (fp):
    """ Return True if the file is Gziped else False """
    return fp[-2:].lower() == "gz"

#~~~~~~~ PATH MANIPULATION ~~~~~~~#

def file_basename (path):
    """Return the basename of a file without folder location and extension """
    return path.rpartition('/')[2].partition('.')[0]

def file_extension (path):
    """ Return The extension of a file in lower-case """
    return path.rpartition(".")[2].lower()

def file_name (path):
    """ Return The complete name of a file with the extension but without folder location """
    return path.rpartition("/")[2]    

def dir_name (path):
    """ Return the complete path where is located the file without the file name """
    return path.rpartition("/")[0].rpartition("/")[2]

##~~~~~~~ STRING FORMATTING ~~~~~~~#

def supersplit (string, separator=""):
    """like split but can take a list of separators instead of a simple separator """    
    if not separator:
        return string.split()
    
    if type(separator) == str:
        return string.split(separator)
    
    for sep in separator:
        string = string.replace(sep, "#")
    return string.split("#")
    
def rm_blank (name, replace=""):
    """ Replace blank spaces in a name by a given character (default = remove)
    Blanks at extremities are always removed and nor replaced """
    return replace.join(name.split())

#~~~~~~~ FILE MANIPULATION ~~~~~~~#

def copyFile(src, dest):
    """
    Copy a single file to a destination file or folder (with error handling/reporting)
    @param src Source file path
    @param dest Path of the folder where to copy the source file
    """
    try:
        shutilCopy(src, dest)
    # eg. src and dest are the same file
    except shutilError as E:
        print('Error: %s' % E)
    # eg. source or destination doesn't exist
    except IOError as E:
        print('Error: %s' % E.strerror)

def gzip_file (in_path, out_path=None):
    """
    @param in_path Path of the input uncompressed file
    @param out_path Path of the output compressed file (facultative)
    @exception  OSError Can be raise by open
    """
    # Generate a automatic name if none is given
    if not out_path:
        out_path = in_path +".gz"

    # Try to initialize handle for
    try:
        in_handle = open(in_path, "rb")
        out_handle = gopen(out_path, "wb")
        # Write input file in output file
        print ("Compressing {}".format(in_path))
        out_handle.write (in_handle.read())
        # Close both files
        in_handle.close()
        out_handle.close()
        return path.abspath(out_path)

    except IOError as E:
        print(E)
        if path.isfile (out_path):
            try:
                remove (out_path)
            except OSError:
                print ("Can't remove {}".format(out_path))

def gunzip_file (in_path, out_path=None):
    """
    @param in_path Path of the input compressed file
    @param out_path Path of the output uncompressed file (facultative)
    @exception  OSError Can be raise by open
    """
    # Generate a automatic name without .gz extension if none is given
    if not out_path:
        out_path = in_path[0:-3]

    try:
        # Try to initialize handle for
        in_handle = gzip.GzipFile(in_path, 'rb')
        out_handle = open(out_path, "wb")
        # Write input file in output file
        print ("Uncompressing {}".format(in_path))
        out_handle.write (in_handle.read())
        # Close both files
        out_handle.close()
        in_handle.close()
        return path.abspath(out_path)

    except IOError as E:
        print(E)
        if path.isfile (out_path):
            try:
                remove (out_path)
            except OSError:
                print ("Can't remove {}".format(out_path))

#~~~~~~~ FILE INFORMATION ~~~~~~~#
            
def head (file, n=10, ignore_hashtag_line=False):
    """Emulate linux head cmd. Also works for gzip files"""
    
    f = gopen(file, "rt") if is_gziped(file) else open (file, "r")
    
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
    print()
    f.close()
 
def linerange (file, range_list=[]):
    """Print a range of lines in a file according to a list of start end lists"""
    if not range_list:
        n_line = fastcount(file)
        range_list=[[0,2],[n_line-3, n_line-1]]
    
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
            print("")

def colsum (file, colrange=None, separator="", header=False, ignore_hashtag_line=False, max_items=10, ret_type="md"):
    """
    Create a summary of selected columns of a file
    Possible return types: md = markdown formatted table, dict = raw parsing dict, report = Indented_text_report
    """ 
        
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
                #print("Header found")
                continue
                
            # Get the number of col if not given and handle the first line            
            if not colrange:
                colrange = [i for i in range(len(ls))]
                #print("Found {} colums".format(len(ls)))
                
            # Manage the first valid line
            #print("First line found")
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

    # Return directly the whole dict            
    if ret_type == "dict":
        return res_dict
    
    # Return an indented text report 
    if ret_type == "report":
        return dict_to_report(res_dict, tab="\t", sep="\t", sort_dict=True, max_items=max_items)

    # Create a Markdown table output per colums
    elif ret_type == "md":
        buffer=""
        for colnum, col_dict in res_dict.items():
            if header:
                buffer+= dict_to_md(col_dict, header_dict[colnum], "Count", transpose=True, sort_by_val=True, max_items=max_items)
            else:
                buffer+= dict_to_md(col_dict, colnum, "Count", transpose=True, sort_by_val=True, max_items=max_items)
            buffer+='\n'
        return buffer
        
    else:
        print ("Invalid return type")

def fastcount(file):
    """Efficient way to count the number of lines in a file"""
    f = open(file)                  
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)
    return lines

def simplecount(filename, ignore_hashtag_line=False):
    """Simple way to count the number of lines in a file with more options"""
    lines = 0
    for line in open(filename):
        if ignore_hashtag_line and line[0] == "#":
            continue
        lines += 1
    return lines


#~~~~~~~ DIRECTORY MANIPULATION ~~~~~~~#
  
def mkdir(fp, level=1):
    """
    Reproduce the ability of UNIX "mkdir -p" command
    (ie if the path already exits no exception will be raised).
    Can create nested directories by recursivity
    @param  fp path name where the folder should be created
    @level  level   level in the path where to start to create the directories.
                    Used by the program for the recursive creation of directories
    @exception  OSError or PermissionError can be raise by os.mkdir
    """
        
    # Extract the path corresponding to the current level of subdirectory and create it if needed
    fp = path.abspath(fp)
    split_path = fp.split("/")
    cur_level = split_path[level-1]
    cur_path = "/".join(split_path[0:level])
    if cur_path:
        _mkdir(cur_path)
    
    # If the path is longer than the current level cpntinue to call mkdir recursively
    if len(fp.split("/")) > level:
        mkdir(fp, level=level+1)

def _mkdir (fp):
    if path.exists(fp) and path.isdir(fp):
        #print ("Entering {}".format(fp))
        pass
    else:
        print ("Creating {}".format(fp))
        osmkdir(fp)

#~~~~~~~ SHELL MANIPULATION ~~~~~~~#

def make_cmd_str(prog_name, opt_dict={}, opt_list=[]):
    """
    Create a Unix like command line string from a
    @param prog_name Name (if added to the system path) or path of the program
    @param opt_dict Dictionary of option arguments such as "-t 5". The option flag have to
    be the key (without "-") and the the option value in the dictionary value. If no value is
    requested after the option flag "None" had to be assigned to the value field.
    @param opt_list List of simple command line arguments
    @exemple make_cmd_str("bwa", {"b":None, t":6, "i":"../idx/seq.fa"}, ["../read1", "../read2"])
    """
    
    # Start the string by the name of the program
    cmd = "{} ".format(prog_name)

    # Add options arguments from opt_dict
    if opt_dict:
        for key, value in opt_dict.items():
            if value:
                cmd += "{} {} ".format(key, value)
            else:
                cmd += "{} ".format(key)

    # Add arguments from opt_list
    if opt_list:
        for value in opt_list:
            cmd += "{} ".format(value)

    return cmd


def bash_basic(cmd):
    """Sent basic bash command"""
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    print(stdout.decode())
    print (stderr.decode())


def bash(cmd, stdin=None, ret_stderr=False, ret_stdout=True, str_output=True):
    """
    Run a command line in the default shell and return the standard output
    @param  cmd A command line string formatted as a string
    @param  stdinput    Facultative parameters to redirect an object to the standard input
    @param  ret_stderr  If True the standard error output will be returned
    @param  ret_stdout  If True the standard output will be returned
    @param  str_output  Transform the std output in a string instead of the bytes-like object
    @note If ret_stderr and ret_stdout are True a tuple will be returned and if both are False
    None will be returned
    @return If no standard error return the standard output as a string
    @exception  OSError Raise if a message is return on the standard error output
    @exception  (ValueError,OSError) May be raise by Popen
    """

    # Execute the command line in the default shell
    if stdin:
        proc = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate(input=stdin)
    else:
        proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()

    if proc.returncode == 1:
        msg = "An error occured during execution of following command :\n"
        msg += "COMMAND : {}\n".format(cmd)
        msg += "STDERR : {}\n".format(stderr.decode())
        print (msg)
        return None

    # Else return data according to user choices is returned
    if str_output:
        if ret_stdout and ret_stderr:
            return stdout.decode(), stderr.decode()
        elif ret_stdout:
            return stdout.decode()
        elif ret_stderr:
            return stderr.decode()
        
    else:
        if ret_stdout and ret_stderr:
            return stdout, stderr
        elif ret_stdout:
            return stdout
        elif ret_stderr:
            return stderrOrderedDict
   
    # Last possibility
    return None

##~~~~~~~ DICTIONNARY FORMATTING ~~~~~~~#

def dict_to_md (
    d,
    key_label="",
    value_label="",
    transpose=False,
    sort_by_key=False,
    sort_by_val=True,
    max_items=None):
    """Def to transform a dict into a markdown formated table"""
    
    # Preprocess dict
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
    
    # Prepare output
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

def dict_to_report (
    d,
    tab="\t",
    ntab=0,
    sep=":",
    sort_dict=True,
    max_items=None):
    """Recursive function to return a text report from nested dict or OrderedDict objects"""
    
    # Preprocess dict
    if sort_dict:
        
        # Verify that all value in the dict are numerical
        all_num = True
        for value in d.values():
            if not type(value) in [int, float]:
                all_num = False
        
        # Sort dict by val only if it contains numerical values       
        if all_num:
            d = OrderedDict(reversed(sorted(d.items(), key=lambda t: t[1])))
            
            if max_items and len(d)>max_items:
                d2 = OrderedDict()
                n=0
                for key, value in d.items():
                    d2[key]=value
                    n+=1
                    if n >= max_items:
                        break
                d2["..."]="..."
                d=d2
                    
        # Else sort alphabeticaly by key
        else:
            d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
    
    # Prepare output
    report = ""
    for name, value in d.items():
        if type(value) == OrderedDict or type(value) == dict:
            report += "{}{}\n".format(tab*ntab, name)
            report += dict_to_report(value, tab=tab, ntab=ntab+1, sep=sep, sort_dict=sort_dict, max_items=max_items)
        else:
            report += "{}{}{}{}\n".format(tab*ntab, name, sep, value)
    return report        

class dict_to_html(OrderedDict):
    """
    Overridden dict class which takes a 2 level dict and renders an HTML Table in IPython Notebook
    Using the magic repr_html_
    {'a':{'val1':2,'val2':3},'b':{'val1':4,'val2':5},'c':{'val1':7,'val2':8}}
    """

    def __init__ (self, d):
        for key in sorted(d.keys()):
            self[key] = d[key]
            
    def _repr_html_(self):
        html = ["<table width=100%>"]
        
        first_col = False
        for key, val in self.items():

            # Add Columns header for the first line
            if not first_col:
                html.append("<tr><td> </td>")
                subkeys = sorted(val.keys())
                for subkey in subkeys:
                    html.append("<td><b>{}</b></td>".format(subkey))
                first_col = True
                html.append("</tr>")
                
            # Add row header and values
            html.append("<tr><td><b>{}</b></td>".format(key))
            for subkey in subkeys:
                html.append("<td>{}</td>".format(self[key][subkey]))
            html.append("</tr>")

        # End the table
        html.append("</table>")   
        
        return ''.join(html)

##~~~~~~~ TABLE FORMATTING ~~~~~~~#

def reformat_table(
    input_file,
    output_file,
    init_template=[],
    final_template=[],
    header = '',
    keep_original_header = True,
    header_from_final_template = False,
    replace_internal_space='_',
    replace_null_val="*",
    subst_dict={},
    filter_dict=[],
    predicate=None,
    standard_template=None):
    """
    Reformat a table given an initial and a final line templates indicated as a list where numbers
    indicate the data column and strings the formatting characters
    
    @param  input_file   A file with a structured text formatting (uncompressed)
    @param  output_file   A file path to output the reformatted table
    @param  init_template   A list of indexes and separators describing the structure of the input file
            Example initial line = "chr1    631539    631540    Squires|id1    0    +"
            Initial template = [0,"\t",1,"\t",2,"\t",3,"|",4,"\t",5,"\t",6]
            Alternatively, instead of the numbers, string indexes can be used, but they need to be enclosed in curly brackets to
            differentiate them from the separators. This greatly simplify the writing of the final template.
            Example initial line = "chr1    631539    631540    Squires|id1    0    +"
            Initial template = ["{chrom}","\t","{start}","\t","{end}","|","{name}","\t","{score}","\t","{strand}"]
    @param  final_template  A list of indexes and separators describing the required structure of the output file. Name indexes need to 
            match indexes of the init_template and have to follow the same synthax
            Example final line = "chr1    631539    631540    m5C|-|HeLa|22344696    -    -"
            Final template = [0,"\t",1,"\t",2,"\tm5C|-|HeLa|22344696\t-\t",6]
    @param  header   A string to write as a file header at the beginning of the file
    @param  keep_original_header   If True the original header of the input file will be copied at the beginning of the output file [DEFAULT:True]
    @param  header_from_final_template  Generate a header according to the name or number of the fields given in the final_template [DEFAULT:True]
    @param  replace_internal_space  All internal blank space will be replaced by this character [DEFAULT:"_"]
    @param  replace_null_val   Field with no value will be replaced by this character [DEFAULT:"*"]
    @param  subst_dict   Nested dictionary of substitution per position to replace specific values by others [DEFAULT:None]
            Example: { 0:{"chr1":"1","chr2":"2"}, 3:{"Squires":"5376774764","Li":"27664684"}}
    @param  filter_dict  A dictionary of list per position  to filter out lines  with specific values [DEFAULT:None]
            Example: { 0:["chr2", "chr4"], 1:["46767", "87765"], 5:["76559", "77543"]}
    @param  predicate   A lambda predicate function for more advance filtering operations [DEFAULT:None]
            Example:  lambda val_dict: abs(int(val_dict[1])-int(val_dict[2])) <= 2000
    @param  standard_template   Existing standard template to parse the file  instead of providing one manually. List of saved templates:
        - "gff3_ens_gene" = Template for ensembl gff3 fields. Select only the genes lines and decompose to individual elements.
        - "gff3_ens_transcript" = Template for ensembl gff3 fields. Select only the transcript lines and decompose to individual elements.
    """
    
    # Verify if the user provided a standard template and parameter the function accordingly
    # If needed the predicate2 variable will be used to filter the data according to the template
    if standard_template:
        
        if standard_template == "gff3_ens_gene":
            print("Using gff3 ensembl gene template. Non-gene features will be filtered out")
            
            init_template = ["{seqid}","\t","{source}","\t","{type}","\t","{start}","\t","{end}","\t","{score}","\t","{strand}","\t","{phase}",
            "\tID=","{ID}",
            ";gene_id=","{gene_id}",
            ";gene_type=","{gene_type}",
            ";gene_status=","{gene_status}",
            ";gene_name=","{gene_name}",
            ";level=","{level}",
            ";havana_gene=","{havana_gene}"]
                        
            predicate2 = lambda v:v["type"]=="gene"
            
        if standard_template == "gff3_ens_transcript":
            print("Using gff3 ensembl transcript template. Non-transcript features will be filtered out")
            
            init_template = ["{seqid}","\t","{source}","\t","{type}","\t","{start}","\t","{end}","\t","{score}","\t","{strand}","\t","{phase}",
            "\tID=","{ID}",
            ";Parent=","{Parent}",
            ";gene_id=","{gene_id}",
            ";transcript_id=","{transcript_id}",
            ";gene_type=","{gene_type}",
            ";gene_status=","{gene_status}",
            ";gene_name=","{gene_name}",
            ";transcript_type=","{transcript_type}",
            ";transcript_status=","{transcript_status}",
            ";transcript_name=","{transcript_name}",
            ";level=","{level}",
            ";transcript_support_level=","{transcript_support_level}",
            ";tag=","{tag}",
            ";havana_gene=","{havana_gene}",
            ";havana_transcript=","{havana_transcript}"]
            
            predicate2 = lambda v:v["type"]=="transcript"
                       
    else:
        predicate2 = None
    
    
    # Print the pattern of decomposition and recomposition
    print ("Initial template values")
    print (_template_to_str(init_template))
    print ("Final template values")
    print (_template_to_str(final_template))

    # Iterate over the input file 
    with open (input_file, "r") as infile, open (output_file, "w") as outfile:
        total = fail = success = filtered_out = 0
        if header:
            outfile.write(header)
        if header_from_final_template:
            outfile.write(_template_to_str(final_template)+"\n")
            
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
                    val_dict = raw_val,
                    replace_internal_space = replace_internal_space,
                    replace_null_val = replace_null_val,
                    subst_dict = subst_dict,
                    filter_dict = filter_dict,
                    predicate=predicate,
                    predicate2= predicate2)
                assert clean_val, "The line #{} was filter according to the filter dictionnary:\n{}".format(total,line)
            except AssertionError as E:
                filtered_out+=1
                continue
            
            # Recompose the line
            formated_line = _reformat_line(
                val_dict = clean_val,
                template = final_template)
            outfile.write(formated_line)
            success+=1
            
    print ("{} Lines processed\t{} Lines pass\t{} Lines filtered out\t{} Lines fail".format(total, success, filtered_out, fail))

def _is_str_key (element):
    return type(element)==str and element[0]=="{" and element[-1]=="}"
    
def _is_str_sep (element):
    return type(element)==str and (element[0]!="{" or element[-1]!="}")

def _template_to_str(template):
    l=[]
    for element in template:
        if _is_str_sep(element):
            l.append(element)
        elif _is_str_key(element):
            l.append(element[1:-1])
        elif type(element) == int:
            l.append(str(element))
    return "".join(l)

def _decompose_line(line, template):
    """Helper function for reformat_table. Decompose a line in a dictionnary and extract the values given a template list"""
    
    val_dict = OrderedDict()
    
    # Remove the first element from the line if this is a separator
    if _is_str_sep(template[0]):
        val, sep, line = line.partition(template[0])
        template = template[1:]
    
    # Decompose the line
    last_key = None
    for element in template:
        # if found a str key, store it and remove the curly brackets
        if _is_str_key(element):
            last_key = element[1:-1]
        # if numerical key, just store it
        if type(element) == int:
            last_key = element
        if _is_str_sep(element):
            # Verify the values before filling the dict
            assert last_key != None, "Problem in the init template"
            assert last_key not in val_dict, "Duplicated key in the init template"
            val, sep, line = line.partition(element)
            val_dict[last_key] = val
            last_key = None
    
    # Manage last element of the template if it is a key
    if last_key:
        val_dict[last_key] = line
    
    return val_dict

def _clean_values (
    val_dict,
    replace_internal_space=None,
    replace_null_val=None,
    subst_dict={},
    filter_dict={},
    predicate=None,
    predicate2=None):
    """Helper function for reformat_table. Clean the extracted values"""
    
    for key in val_dict.keys():
        # Strip the heading and trailing blank spaces 
        val_dict[key] = val_dict[key].strip()
                
        # Replace the empty field by a given char
        if replace_null_val and not val_dict[key]:
            val_dict[key] = replace_null_val
        
        # Replace internal spaces by underscores
        if replace_internal_space:
            val_dict[key] = val_dict[key].replace(" ","_")
        
        # Filter line based on the filter_dict
        if key in filter_dict and val_dict[key] in filter_dict[key]:
            return None
        
        # Filter line base on predicate function
        if predicate and not predicate(val_dict):
            return None
        
        # Filter line base on an eventual second predicate function
        if predicate2 and not predicate2(val_dict):
            return None
        
        # Use the substitution dict exept if the value is not in the dict in this case use the default value
        if key in subst_dict and val_dict[key] in subst_dict[key]:
            val_dict[key] = subst_dict[key][val_dict[key]]    
    
    return val_dict

def _reformat_line (val_dict, template):
    """Helper function for reformat_table. Reassemble a line from a list of values and a template list"""
    
    line = ""
    try:
        for element in template:
            if _is_str_sep(element):
                line+=element
            if type(element) == int:
                line+=val_dict[element]
            if _is_str_key(element):
                line+=val_dict[element[1:-1]]
            
    except IndexError as E:
        print (E)
        print (val_dict)
        print (template)
        raise
        
    return line+"\n"

##~~~~~~~ WEB TOOLS ~~~~~~~#

def url_exist (url):
    """ Predicate verifying if an url exist without downloading all the link"""
    
    # third party import
    import httplib2
    
    # Chek the url
    h = httplib2.Http()
    
    try:
        resp = h.request(url, 'HEAD')
        return int(resp[0]['status']) < 400
    except:
        return False


def wget(url, out_name="", progress_block=100000000):
    """
    Download a file from an URL to a local storage.
    @param  url             A internet URL pointing to the file to download
    @param  outname         Name of the outfile where (facultative)
    @param  progress_block  size of the byte block for the progression of the download
    """
    
    def size_to_status (size):
        if size >= 1000000000:
            status = "{} GB".format(round(size/1000000000, 1))
        elif size >= 1000000:
            status = "{} MB".format(round(size/1000000, 1))
        elif size >= 1000:
            status = "{} kB".format(round(size/1000, 1))
        else :
            status = "{} B".format(size)
        return status
    
    # function specific imports 
    from urllib.request import urlopen
    from urllib.parse import urlsplit
    from urllib.error import HTTPError, URLError
    
    # Open the url and retrieve info
    try:
        u = urlopen(url)
        scheme, netloc, path, query, fragment = urlsplit(url)
    except (HTTPError, URLError, ValueError) as E:
        print (E)
        return None
        
    # Attribute a file name if not given
    if not out_name:
        out_name = file_name(path)
        if not out_name:
            out_name = 'output.file'

    # Create the output file and 
    with open(out_name, 'wb') as fp:
        
        # Retrieve file meta information 
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_size = meta_func("Content-Length")
        if meta_size:
            file_size = int(meta_func("Content-Length")[0])
            print("Downloading: {}\tBytes: {}".format(url, file_size))
        else:
            file_size=None
            print("Downloading: {}\tSize unknown".format(url))
        
        # Buffered reading of the file to download
        file_size_dl = 0
        block_sz = 1000000
        
        last_pblock = progress_block
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            fp.write(buffer)
            
            # Progress bar
            file_size_dl += len(buffer)
            
            if file_size_dl >= last_pblock:
                status = "{} Downloaded".format(size_to_status(file_size_dl))
                if file_size: 
                    status += "\t[{} %]".format (round(file_size_dl*100/file_size, 2))
                print(status)
                last_pblock += progress_block
        
        # Final step of the progress bar
        status = "{} Downloaded".format(size_to_status(file_size_dl))
        if file_size: 
            status += "\t[100 %]"
        print(status)
        
    return out_name
