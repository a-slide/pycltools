# pycl 1.0.4 package documentation

---

**pycl is a package written in python3 containing a collection of generic functions and classes for file parsing, manipulation...**

---

pycl contains many functions organized in several categories:

* jupyter notebook specific tools
* file predicates
* path manipulation
* string formatting
* file manipulation
* file information/parsing
* directory manipulation
* shell manipulation
* dictionnary formatting
* table formatting
* web tools
* functions tools
* ssh tools

Many of the function replicate bash commands in pure python.

Please be aware that pycl is an experimental package that is still under development. It was tested under Linux Ubuntu 16.04 and in an HPC 
environment running under Red Hat Enterprise 7.1. You are welcome to raise issues, contribute to the development and submit patches or
updates.

* Author: Adrien Leger - aleg@ebi.ac.uk

* URL: https://github.com/a-slide/pycoQC

* Licence: GPLv3

## Installation

Ideally, before installation, create a clean python3 virtual environment to deploy the package, using virtualenvwrapper for example (see http://www.simononsoftware.com/virtualenv-tutorial-part-2/).

### Option 1: Direct installation with pip from github

Install the package with pip.

```bash
pip3 install git+https://github.com/a-slide/pycl.git
```

To update the package:

```bash
pip3 install git+https://github.com/a-slide/pycl.git --upgrade
```

### Option 2: Clone the repository and install locally in develop mode

With this option, the package will be locally installed in “editable” or “develop” mode. This allows the package to be both installed and editable in project form. This is the recommended option if you wish to participate to the development of the package. As for the option before, the required dependencies will be automatically installed.

```bash
git clone https://github.com/a-slide/pycl.git
cd pycl
chmod u+x setup.py
pip3 install -e ./
```

With this option you can also run the testing notebook located in the source directory *pycl/test_pycl.ipynb*

### Option 3: Local installation without pip 

This option is also suitable if you are interested in further developing the package, but requires a little bit more hands-on.

* Clone the repository locally

```bash
git clone https://github.com/a-slide/pycl.git
```

* Add the package directory (./pycl/pycl) to you python3 PATH (depending on you OS and whether you want it to be permanent ot not)

## Python packages optional dependencies:

* *['notebook']* for function *bash_update*

* *['pandas']* for function *reformat_table*

* *['notebook']* for function *toogle_code*

* *['pandas']* for function *count_uniq*

* *['notebook']* for function *jhelp*

* *['httplib2']* for function *url_exist*

* *['notebook']* for function *jprint*

* *['paramiko']* for function *scp*

* *['notebook']* for function *larger_display*

## Usage

### Using pycl

Import pycl main class

```python
from pycl import pycl
```

Sample data files are provided with the package for testing purpose. Depending on your installation choice, they could be found either directly in the *pycl/data* directory or using *pkg_resources* (see https://setuptools.readthedocs.io/en/latest/pkg_resources.html). Here is the list of the test files:

* Small_m5C_Squires_hg38.bed

* gencode_sample.gff3

* RADAR_clean.txt

* sample_100.sam

* RADAR_Secondary.txt.gz

* Small_m5C_Squires_hg38_reformat.bed

* sample.sam

* stdout.txt

* Small_editing_Peng_hg38_reformat.bed

* sample_100.bam

* RADAR_Secondary.txt

* test_dir

* RADAR_Main.txt

* Small_editing_Peng_hg38.bed

* RADAR_Secondary_copy.txt

A list of the available functions is provided below. Functions are comprehensively detailed in the testing notebook provided with the package or in html version on nbviewer: [link to test_notebook](https://nbviewer.jupyter.org/github/a-slide/pycl/blob/master/pycl/test_pycl.ipynb?flush_cache=true)

<b>bam_sample</b> (fp_in, fp_out, n_reads, verbose=False, **kwargs)

Sample reads from a SAM/BAM file and write in a new file

* fp_in

Path to the input file in .bam/.sam/.cram (the format will be infered from extension)

* fp_out

Path to the output file in .bam/.sam/.cram (the format will be infered from extension)

* n_reads

number of reads to sample

    ________________________________________________________________________________

<b>bash</b> (cmd, live='stdout', print_stdout=True, ret_stdout=False, log_stdout=None, print_stderr=True, ret_stderr=False, log_stderr=None, **kwargs)

More advanced version of bash calling with live printing of the standard output and possibilities to log the redirect

the output and error as a string return or directly in files. If ret_stderr and ret_stdout are True a tuple will be returned and if

both are False None will be returned

* cmd

A command line string formatted as a string

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

    ________________________________________________________________________________

<b>bash_basic</b> (cmd, **kwargs)

Sent basic bash command

    ________________________________________________________________________________

<b>bash_update</b> (cmd, update_freq=1, **kwargs)

FOR JUPYTER NOTEBOOK

Run a bash command and print the output in the cell. The output is updated each time until the output is None.

This is suitable for monitoring tasks that log events until there is nothing else to print such as bjobs or bpeeks.

* cmd

A command line string formatted as a string

* update_freq

The frequency of output updating in seconds [DEFAULT: 1]

    ________________________________________________________________________________

<b>cat</b> (fp, max_lines=100, line_numbering=False, max_char_line=150, **kwargs)

Emulate linux cat cmd but with line cap protection. Handle gziped files

* fp

Path to the file to be parsed

* max_lines

Maximal number of lines to print

* line_numbering

If True the number of the line will be indicated in front of the line

* max_char_line

Maximal number of character to print per line

    ________________________________________________________________________________

<b>colsum</b> (fp, colrange=None, separator='', header=False, ignore_hashtag_line=False, max_items=10, ret_type='md', **kwargs)

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

    ________________________________________________________________________________

<b>copyFile</b> (src, dest, **kwargs)

Copy a single file to a destination file or folder (with error handling/reporting)

* src

Source file path

* dest

Path of the folder where to copy the source file

    ________________________________________________________________________________

<b>count_uniq</b> (fp, colnum, select_values=None, drop_values=None, skip_comment='#', sep='\t', **kwargs)

Count unique occurences in a specific column of a tabulated file

* fp

Path to the file to be parsed (gzipped or not)

* colnum

Index number of the column to summarize

* select_values

Select specific lines in the file based on a dictionary containing column index(es) and valu(es) or list

of values to select. Exemple {2:["exon", "transcript"], 4:"lincRNA"}. DEFAULT=None

* drop_values

Same think that select_value but will drop the lines instead. DEFAULT=None

* skip_comment

Drop any comment lines starting with this character. DEFAULT="#"

* sep

Character or list of characters to use in order to split the lines. Exemple ["	",";"]. DEFAULT="	"

    ________________________________________________________________________________

<b>dict_to_md</b> (d, key_label='', value_label='', transpose=False, sort_by_key=False, sort_by_val=True, max_items=None, **kwargs)

Transform a dict into a markdown formated table

    ________________________________________________________________________________

<b>dict_to_report</b> (d, tab='\t', ntab=0, sep=':', sort_dict=True, max_items=None, **kwargs)

Recursive function to return a text report from nested dict or OrderedDict objects

    ________________________________________________________________________________

<b>dir_name</b> (fp, **kwargs)

Return the name of the directory where the file is located

    ________________________________________________________________________________

<b>dir_path</b> (fp, **kwargs)

Return the directory path of a file

    ________________________________________________________________________________

<b>extensions</b> (fp, comp_ext_list=['gz', 'tgz', 'zip', 'xz', 'bz2'], **kwargs)

Return The extension of a file in lower-case. If archived file ("gz", "tgz", "zip", "xz", "bz2")

the method will output the base extension + the archive extension as a string

    ________________________________________________________________________________

<b>extensions_list</b> (fp, comp_ext_list=['gz', 'tgz', 'zip', 'xz', 'bz2'], **kwargs)

Return The extension of a file in lower-case. If archived file ("gz", "tgz", "zip", "xz", "bz2")

the method will output the base extension + the archive extension as a list

    ________________________________________________________________________________

<b>fastcount</b> (fp, **kwargs)

Efficient way to count the number of lines in a file. Handle gziped files

    ________________________________________________________________________________

<b>file_basename</b> (fp, **kwargs)

Return the basename of a file without folder location and extension

    ________________________________________________________________________________

<b>file_name</b> (fp, **kwargs)

Return The complete name of a file with the extension but without folder location

    ________________________________________________________________________________

<b>get_package_file</b> (package, fp='', **kwargs)

Verify the existence of a file from the package data and return a file path

* package

Name of the package

* fp

Relative path to the file in the package. Usually package_name/data/file_name

if the path points to a directory the directory arborescence will be printed

    ________________________________________________________________________________

<b>gunzip_file</b> (fpin, fpout=None, **kwargs)

ungzip a file

* fpin

Path of the input compressed file

* fpout

Path of the output uncompressed file (facultative)

    ________________________________________________________________________________

<b>gzip_file</b> (fpin, fpout=None, **kwargs)

gzip a file

* fpin

Path of the input uncompressed file

* fpout

Path of the output compressed file (facultative)

    ________________________________________________________________________________

<b>has_extension</b> (fp, ext, pos=-1, raise_exception=False, **kwargs)

Test presence of extension in a file path

* ext

Single extension name or list of extension names  without dot. Example ["gz, "fa"]

* pos

Postition of the extension in the file path. -1 for the last, -2 for the penultimate and so on [DEFAULT -1 = Last position]

    ________________________________________________________________________________

<b>head</b> (fp, n=10, line_numbering=False, ignore_comment_line=False, comment_char='#', max_char_line=150, **kwargs)

Emulate linux head cmd. Handle gziped files

* fp

Path to the file to be parsed

* n

Number of lines to print starting from the begining of the file (Default 10)

* line_numbering

If True the number of the line will be indicated in front of the line (Default False)

* ignore_comment_line

Skip initial lines starting with a specific character (Default False)

* comment_char

Character or string for ignore_comment_line argument (Default "#")

* max_char_line

Maximal number of character to print per line (Default 150)

    ________________________________________________________________________________

<b>is_gziped</b> (fp, **kwargs)

Return True if the file is Gziped else False

    ________________________________________________________________________________

<b>is_readable_file</b> (fp, raise_exception=True, **kwargs)

Verify the readability of a file or list of file

    ________________________________________________________________________________

<b>jhelp</b> (function, full=False, **kwargs)

Print a nice looking help string based on the name of a declared function. By default print the function definition and description

* function

Name of a declared function or class method

* full

If True, the help string will included a description of all arguments

    ________________________________________________________________________________

<b>jprint</b> (*args, **kwargs)

FOR JUPYTER NOTEBOOK ONLY

Format a string in HTML and print the output. Equivalent of print, but highly customizable. Many options can be passed to the function.

* *args

One or several objects that can be cast in str

* **kwargs

Formatting options to tweak the html rendering

Boolean options : bold, italic, highlight, underlined, striked, subscripted, superscripted

String oprions: font, color, size, align, background_color, line_height

    ________________________________________________________________________________

<b>larger_display</b> (percent=100, **kwargs)

FOR JUPYTER NOTEBOOK ONLY

Resize the area of the screen containing the notebook according to a given percentage of the available width

*  percent percentage of the width of the screen to use [DEFAULT:100]

    ________________________________________________________________________________

<b>linerange</b> (fp, range_list=[], line_numbering=True, max_char_line=150, **kwargs)

Print a range of lines in a file according to a list of start end lists. Handle gziped files

* fp

Path to the file to be parsed

* range_list

list of start, end coordinates lists or tuples

* line_numbering

If True the number of the line will be indicated in front of the line

* max_char_line

Maximal number of character to print per line

    ________________________________________________________________________________

<b>linesample</b> (fp, n_lines=100, line_numbering=True, max_char_line=150, **kwargs)

Randomly sample lines in a file and print them. Handle gziped files

* fp

Path to the file to be parsed

* n_lines

Number of lines to sample in the file

* line_numbering

If True the number of the line will be indicated in front of the line

* max_char_line

Maximal number of character to print per line

    ________________________________________________________________________________

<b>make_cmd_str</b> (prog_name, opt_dict={}, opt_list=[], **kwargs)

Create a Unix like command line string from the prog name, a dict named arguments and a list of unmammed arguments

exemple make_cmd_str("bwa", {"b":None, t":6, "i":"../idx/seq.fa"}, ["../read1", "../read2"])

* prog_name

Name (if added to the system path) or path of the program

* opt_dict

Dictionary of option arguments such as "-t 5". The option flag have to be the key (without "-") and the the option value in the

dictionary value. If no value is requested after the option flag "None" had to be assigned to the value field.

* opt_list

List of simple command line arguments

    ________________________________________________________________________________

<b>mkdir</b> (fp, level=1, **kwargs)

Reproduce the ability of UNIX "mkdir -p" command

(ie if the path already exits no exception will be raised).

Can create nested directories by recursivity

* fp

path name where the folder should be created

* level

level in the path where to start to create the directories. Used by the program for the recursive creation of directories

    ________________________________________________________________________________

<b>print_arg</b> (**kwargs)

Print calling function named and unnamed arguments

    ________________________________________________________________________________

<b>reformat_table</b> (input_file, output_file='', return_df=False, init_template=[], final_template=[], header='', keep_original_header=True, header_from_final_template=False, replace_internal_space='_', replace_null_val='*', subst_dict={}, filter_dict=[], predicate=None, standard_template=None, verbose=False, **kwargs)

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

Initial template = [0,"	",1,"	",2,"	",3,"|",4,"	",5,"	",6]

Alternatively, instead of the numbers, string indexes can be used, but they need to be enclosed in curly brackets to

differentiate them from the separators. This greatly simplify the writing of the final template.

Example initial line = "chr1    631539    631540    Squires|id1    0    +"

Initial template = ["{chrom}","	","{start}","	","{end}","|","{name}","	","{score}","	","{strand}"]

*  final_template

A list of indexes and separators describing the required structure of the output file. Name indexes need to match indexes of the

init_template and have to follow the same synthax  [DEFAULT:Same that init template]

Example final line = "chr1    631539    631540    m5C|-|HeLa|22344696    -    -"

Final template = [0,"	",1,"	",2,"	m5C|-|HeLa|22344696	-	",6]

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

    ________________________________________________________________________________

<b>rm_blank</b> (name, replace='', **kwargs)

Replace blank spaces in a name by a given character (default = remove)

Blanks at extremities are always removed and nor replaced

    ________________________________________________________________________________

<b>scp</b> (hostname, local_file, remote_dir, username=None, rsa_private_key=None, ssh_config='~/.ssh/config', **kwargs)

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

    ________________________________________________________________________________

<b>simplecount</b> (fp, ignore_hashtag_line=False, **kwargs)

Simple way to count the number of lines in a file with more options

    ________________________________________________________________________________

<b>supersplit</b> (string, separator='', **kwargs)

like split but can take a list of separators instead of a simple separator

    ________________________________________________________________________________

<b>tail</b> (fp, n=10, line_numbering=False, max_char_line=150, **kwargs)

Emulate linux tail cmd. Handle gziped files

* fp

Path to the file to be parsed

* n

Number of lines to print starting from the end of the file

* line_numbering

If True the number of the line will be indicated in front of the line

* max_char_line

Maximal number of character to print per line

    ________________________________________________________________________________

<b>toogle_code</b> (**kwargs)

FOR JUPYTER NOTEBOOK ONLY

Hide code with a clickable link in a jupyter notebook

    ________________________________________________________________________________

<b>url_exist</b> (url, **kwargs)

Predicate verifying if an url exist without downloading all the link

    ________________________________________________________________________________

<b>wget</b> (url, out_name='', progress_block=100000000, **kwargs)

Download a file from an URL to a local storage.

*  url

A internet URL pointing to the file to download

*  outname

Name of the outfile where (facultative)

*  progress_block

size of the byte block for the progression of the download

    ________________________________________________________________________________

## Authors and Contact

Adrien Leger - 2017

Enright's group, EMBL EBI

* <aleg@ebi.ac.uk>
* [Github](https://github.com/a-slide)
