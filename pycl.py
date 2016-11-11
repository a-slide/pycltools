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
import sys
from collections import OrderedDict
from subprocess import Popen, PIPE
import gzip

##~~~~~~~ JUPYTER NOTEBOOK SPECIFIC TOOLS ~~~~~~~#

def toogle_code():
    """
    FOR JUPYTER NOTEBOOK ONLY
    Hide code with a clickable link in a jupyter notebook
    """
    # notebook display functions
    from IPython.core.display import display, HTML
    
    display(HTML(
    '''<script>
    code_show=true; 
    function code_toggle() {
     if (code_show){
     $('div.input').hide();
     } else {
     $('div.input').show();
     }
     code_show = !code_show
    } 
    $( document ).ready(code_toggle);
    </script>
    <b><a href="javascript:code_toggle()">Toggle on/off the raw code</a></b>''')
    )

def larger_display (percent=100):
    """
    FOR JUPYTER NOTEBOOK ONLY
    Resize the area of the screen containing the notebook according to a given percentage of the available width 
    *  percent percentage of the width of the screen to use [DEFAULT:100]
    """
    # notebook display functions
    from IPython.core.display import display, HTML
    
    # resizing
    display(HTML("<style>.container {{ width:{0}% !important; }}</style>".format(percent)))
    
def jprint(*args, **kwargs):
    """
    FOR JUPYTER NOTEBOOK ONLY
    Format a string in HTML and print the output. Equivalent of print, but highly customizable
    Many options can be passed to the function.
    * args
        One or several objects that can be cast in str
    ** kwargs
        Formatting options to tweak the html rendering 
        Boolean options : bold, italic, highlight, underlined, striked, subscripted, superscripted
        String oprions: font, color, size, align, background_color
    """
    # notebook display functions
    from IPython.core.display import display, HTML
    
    # Join the different elements together and cast in string 
    s =  " ".join([str(i) for i in args])
    
    # Replace new lines and tab by their html equivalent
    s = s.replace("\n", "<br>").replace("\t", "&emsp;")
    
    # For boolean options
    if "bold" in kwargs and kwargs["bold"]: s = "<b>{}</b>".format(s)
    if "italic" in kwargs and kwargs["italic"]: s = "<i>{}</i>".format(s)
    if "highlight" in kwargs and kwargs["highlight"]: s = "<mark>{}</mark>".format(s)
    if "underlined" in kwargs and kwargs["underlined"]: s = "<ins>{}</ins>".format(s)
    if "striked" in kwargs and kwargs["striked"]: s = "<del>{}</del>".format(s)
    if "subscripted" in kwargs and kwargs["subscripted"]: s = "<sub>{}</sub>".format(s)
    if "superscripted" in kwargs and kwargs["superscripted"]: s = "<sup>{}</sup>".format(s)
    
    # for style options
    style=""
    if "font" in kwargs and kwargs["font"]: style+= "font-family:{};".format(kwargs["font"])
    if "color" in kwargs and kwargs["color"]: style+= "color:{};".format(kwargs["color"])
    if "size" in kwargs and kwargs["size"]: style+= "font-size:{}%;".format(kwargs["size"])
    if "align" in kwargs and kwargs["align"]: style+= "text-align:{};".format(kwargs["align"])
    if "background_color" in kwargs and kwargs["background_color"]: style+= "background-color:{};".format(kwargs["background_color"])
    
    # Format final string
    if style: s = "<p style=\"{}\">{}</p>".format(style,s)
    else: s = "<p>{}</p>".format(s)
        
    display(HTML(s))

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
    """ Return The extension of a file in lower-case. If archived file ("gz", "zip", "xz", "bz2") 
    the method will output the base extension + the archive extension"""
    split_name = path.split("/")[-1].split(".")
    # No extension ? 
    if len (split_name) == 1:
        return ""
    # Manage compressed files
    elif len (split_name) > 2 and split_name[-1].lower() in ["gz", "zip", "xz", "bz2"]:
        return ".{}.{}".format(split_name[-2], split_name[-1]).lower()
    # Normal situation = return the last element of the list
    else:
        return ".{}".format(split_name[-1]).lower()
    
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
    * src
        Source file path
    * dest
        Path of the folder where to copy the source file
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
    gzip a file
    * in_path
        Path of the input uncompressed file
    * out_path
        Path of the output compressed file (facultative)
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
    ungzip a file
    * in_path
        Path of the input compressed file
    * out_path
        Path of the output uncompressed file (facultative)
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
    """Emulate linux head cmd. Handle gziped files"""
    
    try:
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
    # close the file properly
    finally:
        try:
            f.close()
        except:
            pass
 
def linerange (fp, range_list=[], line_numbering = True):
    """
    Print a range of lines in a file according to a list of start end lists. Handle gziped files
    * fp
        Path to the file to be parsed
    * range_list
        list of start, end coordinates lists or tuples
    * line_numbering
        If True the number of the line will be indicated in front of the line
    
    """
    
    if not range_list:
        n_line = fastcount(fp)
        range_list=[[0,2],[n_line-3, n_line-1]]
    
    try:
        f = gopen(fp, "rt") if is_gziped(fp) else open (fp, "r")
        previous_line_empty = False
        for n, line in enumerate(f):
            line_print = False
            for start, end in range_list:
                if start <= n <= end:
                    if line_numbering:
                        l = "{}\t{}".format(n, line.strip())
                    else:
                        l= line.strip()
                    print (l)
                    line_print = True
                    previous_line_empty = False
                    break
                    
            if not line_print:
                if not previous_line_empty:
                    print("...")
                    previous_line_empty = True
                    
    # close the file properly
    finally:
        try:
            f.close()
        except:
            pass
    
def colsum (fp, colrange=None, separator="", header=False, ignore_hashtag_line=False, max_items=10, ret_type="md"):
    """
    Create a summary of selected columns of a file
    * fp
        Path to the file to be parsed
    * colrange
        A list of column index to parse
    * separator
        A character or a list of characters to split the lines 
    * ignore_hashtag_line
        skip line starting with a # symbol
    * max_items
        maximum item per line
    * ret_type
        Possible return types:
        md = markdown formatted table,
        dict = raw parsing dict,
        report = Indented_text_report
    """ 
        
    res_dict = OrderedDict()
    
    with open(fp, "r") as f:
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

def fastcount(fp):
    """Efficient way to count the number of lines in a file. Handle gziped files"""
    try:
        f = gopen(fp, "rt") if is_gziped(fp) else open (fp, "r")
        lines = 0
        buf_size = 1024 * 1024
        read_f = f.read # loop optimization

        buf = read_f(buf_size)
        while buf:
            lines += buf.count('\n')
            buf = read_f(buf_size)

    # close the file properly
    finally:
        try:
            f.close()
            return lines
        except:
            pass
    
def simplecount(fp, ignore_hashtag_line=False):
    """Simple way to count the number of lines in a file with more options"""
    lines = 0
    try:
        f = gopen(fp, "rt") if is_gziped(fp) else open (fp, "r")
    
        for line in f:
            if ignore_hashtag_line and line[0] == "#":
                continue
            lines += 1
            
    # close the file properly
    finally:
        try:
            f.close()
            return lines
        except:
            pass

#~~~~~~~ DIRECTORY MANIPULATION ~~~~~~~#
  
def mkdir(fp, level=1):
    """
    Reproduce the ability of UNIX "mkdir -p" command
    (ie if the path already exits no exception will be raised).
    Can create nested directories by recursivity
    * fp
        path name where the folder should be created
    *level
        level in the path where to start to create the directories. Used by the program for the recursive creation of directories
    """
        
    # Extract the path corresponding to the current level of subdirectory and create it if needed
    fp = path.abspath(fp)
    split_path = fp.split("/")
    cur_level = split_path[level-1]
    cur_path = "/".join(split_path[0:level])
    if cur_path:
        _mkdir(cur_path)
    
    # If the path is longer than the current level continue to call mkdir recursively
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
    Create a Unix like command line string from the prog name, a dict named arguments and a list of unmammed arguments
    exemple make_cmd_str("bwa", {"b":None, t":6, "i":"../idx/seq.fa"}, ["../read1", "../read2"])
    * prog_name
        Name (if added to the system path) or path of the program
    * opt_dict
        Dictionary of option arguments such as "-t 5". The option flag have to be the key (without "-") and the the option value in the
        dictionary value. If no value is requested after the option flag "None" had to be assigned to the value field.
    * opt_list
        List of simple command line arguments
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
    print (stdout.decode())
    print (stderr.decode())


def bash(cmd, live="stdout", print_stdout=True, ret_stdout=False, log_stdout=None, print_stderr=True, ret_stderr=False, log_stderr=None):
    """
    More advanced version of bash calling with live printing of the standard output and possibilities to log the redirect
    the output and error as a string return or directly in files. If ret_stderr and ret_stdout are True a tuple will be returned and if
    both are False None will be returned
    * cmd A command line string formatted as a string
    * print_stdout
        If True the standard output will be LIVE printed through the system standard output stream
    * ret_stdout
        If True the standard output will be returned as a string
    * log_stdout
        If a filename is given, the standard output will logged in this file
    * print_stderr
        If True the standard error will be printed through the system standard error stream
    * ret_stderr
        If True the standard error will be returned as a string
    * log_stderr
        If a filename is given, the standard error will logged in this file 
    """
    
    #empty str buffer
    stdout_str = ""
    stderr_str = ""
    
    # First execute the command parse the output
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    
    # Only 1 standard stream can be output at the time stdout or stderr
    while proc.poll() is None:
        
        # Live parse stdout
        if live == "stdout":
            for line in iter(proc.stdout.readline, b''):
                if print_stdout:
                    sys.stdout.write(line)
                if ret_stdout or log_stdout:
                    stdout_str += line.decode()
                            
        # Live parse stderr
        elif live == "stderr":
            for line in iter(proc.stderr.readline, b''):
                if print_stderr:
                    sys.stderr.write(line)
                if ret_stderr or log_stderr:
                    stderr_str += line.decode()
            
    # Verify that the command was successful and if not print error message and raise an exception
    if proc.returncode >= 1:
        sys.stderr.write("Error code #{} during execution of the command : {}\n".format(proc.returncode, cmd))
        sys.stderr.write(proc.stderr.read())
        return None
    
    if live != "stdout" and (print_stdout or ret_stdout or log_stdout):
        for line in iter(proc.stdout.readline, b''):
            if print_stdout:
                sys.stdout.write(line)
            if ret_stdout or log_stdout:
                stdout_str += line.decode()
    
    if live != "stderr" and (print_stderr or ret_stderr or log_stderr):
        for line in iter(proc.stderr.readline, b''):
            if print_stderr:
                sys.stderr.write(line)
            if ret_stderr or log_stderr:
                stderr_str += line.decode()

    # Write log in file if requested
    if log_stdout:
        with open (log_stdout, "w") as fp:
            fp.write(stdout_str)

    if log_stderr:
        with open (log_stderr, "w") as fp:
            fp.write(stderr_str)
            
    # Return standard output and err if requested
    if ret_stdout and ret_stderr:
        return (stdout_str, stderr_str)
    if ret_stdout:
        return stdout_str
    if ret_stderr:
        return stderr_str
    return None


def bash_update(cmd, update_freq=1):
    """
    FOR JUPYTER NOTEBOOK
    Run a bash command and print the output in the cell. The output is updated each time until the output is None.
    This is suitable for monitoring tasks that log events until there is nothing else to print such as bjobs or bpeeks.    
    * cmd
        A command line string formatted as a string
    * update_freq
        The frequency of output updating in seconds [DEFAULT: 1]
    """

    # imports
    from time import sleep
    from IPython.display import clear_output

    # Init stdout buffer
    stdout_prev= "" 

    # Loop and update the line is something changes
    while True:
        stdout = bash(cmd, ret_stderr=False, ret_stdout=True, print_stderr=False, print_stdout=False)
        if stdout != stdout_prev:
            clear_output()
            print (stdout)
            stdout_prev = stdout
        if not stdout:
            print("All done")
            break
        
        sleep(update_freq)

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

    def __init__ (self, d, max_col=20, max_row=20):
        # Preprocess dict
        i=0
        for k1, v1 in d.items():
            i+=1
            if i > max_col:
                break
            self[k1] = OrderedDict()
            j=0
            for k2, v2 in v1.items():
                j+=1
                if j > max_row:
                    break
                self[k1][k2]=v2
            
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
    output_file="",
    return_df=False,
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
    standard_template=None,
    verbose=False):
    """
    Reformat a table given an initial and a final line templates indicated as a list where numbers
    indicate the data column and strings the formatting characters
    
    *  input_file
        A file with a structured text formatting (gzipped or not)
    *  output_file
        A file path to output the reformatted table (if empty will not write in a file)
    *  return_df
        If true will return a pandas dataframe containing the reformated table (Third party pandas package required) by default the columns
        will be names after the final template [DEFAULT:False]
    *  init_template
        A list of indexes and separators describing the structure of the input file
            Example initial line = "chr1    631539    631540    Squires|id1    0    +"
            Initial template = [0,"\t",1,"\t",2,"\t",3,"|",4,"\t",5,"\t",6]
            Alternatively, instead of the numbers, string indexes can be used, but they need to be enclosed in curly brackets to
            differentiate them from the separators. This greatly simplify the writing of the final template.
            Example initial line = "chr1    631539    631540    Squires|id1    0    +"
            Initial template = ["{chrom}","\t","{start}","\t","{end}","|","{name}","\t","{score}","\t","{strand}"]
    *  final_template
        A list of indexes and separators describing the required structure of the output file. Name indexes need to match indexes of the
        init_template and have to follow the same synthax  [DEFAULT:Same that init template]
            Example final line = "chr1    631539    631540    m5C|-|HeLa|22344696    -    -"
            Final template = [0,"\t",1,"\t",2,"\tm5C|-|HeLa|22344696\t-\t",6]
    *  header
        A string to write as a file header at the beginning of the file
    *  keep_original_header
        If True the original header of the input file will be copied at the beginning of the output file [DEFAULT:True]
    *  header_from_final_template
        Generate a header according to the name or number of the fields given in the final_template [DEFAULT:True]
    *  replace_internal_space
        All internal blank space will be replaced by this character [DEFAULT:"_"]
    *  replace_null_val
        Field with no value will be replaced by this character [DEFAULT:"*"]
    *  subst_dict
        Nested dictionary of substitution per position to replace specific values by others [DEFAULT:None]
            Example: { 0:{"chr1":"1","chr2":"2"}, 3:{"Squires":"5376774764","Li":"27664684"}}
    *  filter_dict
        A dictionary of list per position  to filter out lines  with specific values [DEFAULT:None]
            Example: { 0:["chr2", "chr4"], 1:["46767", "87765"], 5:["76559", "77543"]}
    *  predicate
        A lambda predicate function for more advance filtering operations [DEFAULT:None]
            Example:  lambda val_dict: abs(int(val_dict[1])-int(val_dict[2])) <= 2000
    *  standard_template
        Existing standard template to parse the file  instead of providing one manually. List of saved templates:
        - "gff3_ens_gene" = Template for ensembl gff3 fields. Select only the genes lines and decompose to individual elements.
        - "gff3_ens_transcript" = Template for ensembl gff3 fields. Select only the transcript lines and decompose to individual elements.
        - "gtf_ens_gene" = Template for ensembl gft fields. Select only the genes lines and decompose to individual elements
    * verbose
        If True will print detailed information [DEFAULT:False]
    """
    
    if verbose:
        print_arg()

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

        if standard_template == "gtf_ens_gene":
            print("Using gtf ensembl gene template. Non-gene features will be filtered out")
            
            init_template = ["{seqid}","\t","{source}","\t","{type}","\t","{start}","\t","{end}","\t","{score}","\t","{strand}","\t","{phase}",
            "\tgene_id \"","{gene_id}",
            "\"; gene_type \"","{gene_type}",
            "\"; gene_status \"","{gene_status}",
            "\"; gene_name \"","{gene_name}",
            "\"; level ","{level}",
            "; havana_gene \"","{havana_gene}"]
                        
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
    
    if not final_template:
        if verbose:
            print ("No final template given. Create final template from init template")
        final_template = init_template
    
    # Print the pattern of decomposition and recomposition
    if verbose:
        print ("Initial template values")
        print (_template_to_str(init_template))
        print ("Final template values")
        print (_template_to_str(final_template))

    #Init counters
    total = fail = success = filtered_out = 0
    
    # Init an empty panda dataframe if required
    if return_df:
        import pandas as pd
        df = pd.DataFrame(columns = _template_to_list(final_template))
    
    # init empty handlers
    infile = outfile = None
    try:
        # open the input file gziped or not
        infile = gopen(input_file, "rt") if input_file[-2:].lower()=="gz" else open(input_file, "r")
        
        # open the output file if required
        if output_file:
            outfile = open (output_file, "wt")
            if header:
                outfile.write(header)
            if header_from_final_template:
                outfile.write(_template_to_str(final_template)+"\n")
                    
        for line in infile:
            
            # Original header lines
            if line[0] == "#":
                # write in file if required
                if output_file:
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
            
            # Fill the dataframe if needed
            if return_df:
                df.at[len(df)]= _reformat_list (val_dict=clean_val, template=final_template)
            
            # Recompose the line and write in file if needed
            if output_file:
                formated_line = _reformat_line (val_dict=clean_val, template=final_template)
                outfile.write(formated_line)
            
            success+=1
    
    # Close the files properly
    finally:
        if infile:
            infile.close()
        if outfile:
            outfile.close()
    
    if return_df:
        return df
    
    if verbose:
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

def _template_to_list(template):
    l=[]
    for element in template:
        if _is_str_key(element):
            l.append(element[1:-1])
        elif type(element) == int:
            l.append(str(element))
    return l

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
    """Helper function for reformat_table. Reassemble a line from a dict of values and a template list"""
    
    line = ""
    try:
        for element in template:
            if _is_str_sep(element):
                line+=element
            elif type(element) == int:
                line+=val_dict[element]
            elif _is_str_key(element):
                line+=val_dict[element[1:-1]]
            
    except IndexError as E:
        print (E)
        print (val_dict)
        print (template)
        raise
        
    return line+"\n"

def _reformat_list (val_dict, template):
    """Helper function for reformat_table. Reassemble a list from a dict of values and a template list"""
    
    l=[]
    try:
        for element in template:
            if type(element) == int:
                l.append(val_dict[element])
            elif _is_str_key(element):
                l.append(val_dict[element[1:-1]])
            
    except IndexError as E:
        print (E)
        print (val_dict)
        print (template)
        raise
        
    return l

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
    *  url
        A internet URL pointing to the file to download
    *  outname
        Name of the outfile where (facultative)
    *  progress_block
        size of the byte block for the progression of the download
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

##~~~~~~~ FUNCTIONS TOOLS ~~~~~~~#

def print_arg():
    """
    Print calling function named and unnamed arguments
    """
    # import the function inspection module
    from inspect import getargvalues, stack
    # Parse all arg
    posname, kwname, args = getargvalues(stack()[1][0])[-3:]
    # For enumerated named arguments
    if args:
        print("Enumerated named argument list:")
        for i, j in args.items():
            if i != posname and i != kwname:
                print("\t{}: {}".format(i,j))   
        # For **kwarg arguments
        if kwname:
            print("Unenumerated named arguments list:")
            for i, j in args[kwname].items():
                print("\t{}: {}".format(i,j)) 
        args.update(args.pop(kwname, []))
        if posname:
            print("Unnamed positional arguments list:")
            for i in args[posname]:
                print("\t{}".format(i))

##~~~~~~~ SSH TOOLS ~~~~~~~#

def scp (hostname, local_file, remote_dir, username=None, rsa_private_key=None, ssh_config="~/.ssh/config"):
    """
    Copy a file over ssh in a target remote directory
    * hostname
        Name of the host ssh server 
    * username
        name of the user
    * rsa_private_key
        path to the rsa private key
    * local_file
        path to the local file
    * remote_dir
        path to the target directory
    * ssh_config
        use as an alternative method instead of giving the username and rsa_private_key. Will fetch them from the config file directly
    """
    # function import
    import paramiko
    
    if not username or not rsa_private_key:
        print ("Parse the ssh config file")
        ssh_config = path.expanduser(ssh_config)
        # Find host in the host list of the ssh config file
        with open (ssh_config) as conf:
            host_dict = OrderedDict()
            host=None
            for line in conf:
                if not line.startswith("#"): 
                    if line.startswith("Host"):
                        host = line.strip().split()[1]
                        host_dict[host] = OrderedDict()
                    else:
                        ls = line.strip().split()
                        if len(ls) == 2: 
                            host_dict[host][ls[0]]= ls[1]
        
        try:
            username = host_dict[hostname]["User"]
            rsa_private_key = path.expanduser(host_dict[hostname]["IdentityFile"])
            hostname = host_dict[hostname]["Hostname"]
        except KeyError as E:
            print(E)
            print('Hostname not found in the config file or config not containing User, IdentityFile and Hostname')
            raise
                          
    # now, connect and use paramiko Transport to negotiate SSH2 across the connection
    print ('Establishing SSH connection to: {} ...'.format(hostname))
    with paramiko.Transport(hostname) as t:
        t.start_client()

        try:
            key = paramiko.RSAKey.from_private_key_file(rsa_private_key)
            t.auth_publickey(username, key)
            print ('... Success!')

        except Exception as e:
            print ('... Failed loading {}'.format(rsa_private_key))

        assert t.is_authenticated(), 'RSA key auth failed!'
        
        sftp = t.open_session()
        sftp = paramiko.SFTPClient.from_transport(t)
        
        if remote_dir.startswith ("~"):
            remote_dir = "."+remote_dir[1:]
        
        try:
            sftp.mkdir(remote_dir)
            print ('Create directory {}'.format(remote_dir))
        except IOError as e:
            print ('Assuming {} exists'.format(remote_dir))

        remote_file = remote_dir + '/' + path.basename(local_file)

        print ('Copying local file from {} to {}:{}'.format(local_file, hostname, remote_file))
        sftp.put(local_file, remote_file)
        print ('All operations complete!')
