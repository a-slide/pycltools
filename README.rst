
pycl 1.0.dev1
=============

--------------

**pycl is a package written in python3 containing a collection of
generic functions and classes for file parsing, manipulation...**

--------------

pycl contains many functions organized in several categories:

-  jupyter notebook specific tools
-  file predicates
-  path manipulation
-  string formatting
-  file manipulation
-  file information/parsing
-  directory manipulation
-  shell manipulation
-  dictionnary formatting
-  table formatting
-  web tools
-  functions tools
-  ssh tools

Many of the function replicate bash commands in pure python.

Please be aware that pycl is an experimental package that is still under
development. It was tested under Linux Ubuntu 16.04 and in an HPC
environment running under Red Hat Enterprise 7.1. You are welcome to
raise issues, contribute to the development and submit patches or
updates.

Installation
------------

Ideally, before installation, create a clean python3 virtual environment
to deploy the package, using virtualenvwrapper for example (see
http://www.simononsoftware.com/virtualenv-tutorial-part-2/).

Option 1: Direct installation with pip from github
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the package with pip.

.. code:: python

    pip3 install git+https://github.com/a-slide/pycl.git

To update the package:

.. code:: python

    pip3 install git+https://github.com/a-slide/pycl.git --upgrade

Option 2: Clone the repository and install locally in develop mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With this option, the package will be locally installed in “editable” or
“develop” mode. This allows the package to be both installed and
editable in project form. This is the recommended option if you wish to
participate to the development of the package. As for the option before,
the required dependencies will be automatically installed.

.. code:: python

    git clone https://github.com/a-slide/pycl.git
    cd pycl
    chmod u+x setup.py
    pip3 install -e ./

With this option you can also run the testing notebook located in the
source directory *pycl/test\_pycl.ipynb*

Option 3: Local installation without pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This option is also suitable if you are interested in further developing
the package, but requires a little bit more hands-on.

-  Clone the repository locally

.. code:: python

    git clone https://github.com/a-slide/pycl.git

-  Add the package directory (./pycl/pycl) to you python3 PATH
   (depending on you OS and whether you want it to be permanent ot not)

Installing dependencies (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default pycl will not request any third party dependencies during
installation, instead dependencies are called on a function basis when
needed. If a dependency is missing, the function will display an error
message indicating the missing dependency. If one plan to use all the
function in pycl they can install the following dependencies: \* pandas
0.20.0+ \* httplib2 0.9.0+ \* paramiko 2.0.0 \* notebook 4.0.0+

Usage
-----

Using pycl
~~~~~~~~~~

Import pycl main class

.. code:: python

    from pycl import pycl

Sample data files are provided with the package for testing purpose.
Depending on your installation choice, they could be found either
directly in the *pycl/data* directory or using *pkg\_resources* (see
https://setuptools.readthedocs.io/en/latest/pkg\_resources.html). Here
is the list of the test files:

-  Small\_m5C\_Squires\_hg38.bed
-  gencode\_sample.gff3
-  RADAR\_clean.txt
-  RADAR\_Secondary.txt.gz
-  Small\_m5C\_Squires\_hg38\_reformat.bed
-  stdout.txt
-  Small\_editing\_Peng\_hg38\_reformat.bed
-  RADAR\_Secondary.txt
-  RADAR\_Main.txt
-  Small\_editing\_Peng\_hg38.bed


A list of the available functions is provided below. Functions are
comprehensively detailed in the testing notebook provided with the
package or in html version on nbviewer: `link to
test\_notebook <https://nbviewer.jupyter.org/github/a-slide/pycl/blob/master/pycl/test_pycl.ipynb?flush_cache=true>`__

**bash**

bash(cmd, live='stdout', print\_stdout=True, ret\_stdout=False,
log\_stdout=None, print\_stderr=True, ret\_stderr=False,
log\_stderr=None)

More advanced version of bash calling with live printing of the standard
output and possibilities to log the redirect the output and error as a
string return or directly in files. If ret\_stderr and ret\_stdout are
True a tuple will be returned and if both are False None will be
returned \* cmd A command line string formatted as a string \*
print\_stdout If True the standard output will be LIVE printed through
the system standard output stream \* ret\_stdout If True the standard
output will be returned as a string \* log\_stdout If a filename is
given, the standard output will logged in this file \* print\_stderr If
True the standard error will be printed through the system standard
error stream \* ret\_stderr If True the standard error will be returned
as a string \* log\_stderr If a filename is given, the standard error
will logged in this file

--------------

**bash\_basic**

bash\_basic(cmd)

Sent basic bash command

--------------

**bash\_update**

bash\_update(cmd, update\_freq=1) FOR JUPYTER NOTEBOOK Run a bash
command and print the output in the cell. The output is updated each
time until the output is None. This is suitable for monitoring tasks
that log events until there is nothing else to print such as bjobs or
bpeeks. \* cmd A command line string formatted as a string \*
update\_freq The frequency of output updating in seconds [DEFAULT: 1]

--------------

**cat**

cat(fp, max\_lines=100, line\_numbering=False)

Emulate linux cat cmd but with line cap protection. Handle gziped files

--------------

**colsum**

colsum(fp, colrange=None, separator='', header=False,
ignore\_hashtag\_line=False, max\_items=10, ret\_type='md')

Create a summary of selected columns of a file \* fp Path to the file to
be parsed \* colrange A list of column index to parse \* separator A
character or a list of characters to split the lines \*
ignore\_hashtag\_line skip line starting with a # symbol \* max\_items
maximum item per line \* ret\_type Possible return types: md = markdown
formatted table, dict = raw parsing dict, report =
Indented\_text\_report

--------------

**copyFile**

copyFile(src, dest)

Copy a single file to a destination file or folder (with error
handling/reporting) \* src Source file path \* dest Path of the folder
where to copy the source file

--------------

**count\_uniq**

count\_uniq(fp, colnum, select\_values=None, drop\_values=None,
skip\_comment='#', sep=':raw-latex:`\t`')

Count unique occurences in a specific column of a tabulated file \* fp
Path to the file to be parsed (gzipped or not) \* colnum Index number of
the column to summarize \* select\_values Select specific lines in the
file based on a dictionary containing column index(es) and valu(es) or
list of values to select. Exemple {2:["exon", "transcript"],
4:"lincRNA"}. DEFAULT=None \* drop\_values Same think that select\_value
but will drop the lines instead. DEFAULT=None \* skip\_comment Drop any
comment lines starting with this character. DEFAULT="#" \* sep Character
or list of characters to use in order to split the lines. Exemple ["
",";"]. DEFAULT=" "

--------------

**dict\_to\_md**

dict\_to\_md(d, key\_label='', value\_label='', transpose=False,
sort\_by\_key=False, sort\_by\_val=True, max\_items=None)

Def to transform a dict into a markdown formated table

--------------

**dict\_to\_report**

dict\_to\_report(d, tab=':raw-latex:`\t`', ntab=0, sep=':',
sort\_dict=True, max\_items=None)

Recursive function to return a text report from nested dict or
OrderedDict objects

--------------

**dir\_name**

dir\_name(path)

Return the complete path where is located the file without the file name

--------------

**fastcount**

fastcount(fp)

Efficient way to count the number of lines in a file. Handle gziped
files

--------------

**file\_basename**

file\_basename(path)

Return the basename of a file without folder location and extension

--------------

**file\_extension**

file\_extension(path)

Return The extension of a file in lower-case. If archived file ("gz",
"zip", "xz", "bz2") the method will output the base extension + the
archive extension

--------------

**file\_name**

file\_name(path)

Return The complete name of a file with the extension but without folder
location

--------------

**gunzip\_file**

gunzip\_file(in\_path, out\_path=None)

ungzip a file \* in\_path Path of the input compressed file \* out\_path
Path of the output uncompressed file (facultative)

--------------

**gzip\_file**

gzip\_file(in\_path, out\_path=None)

gzip a file \* in\_path Path of the input uncompressed file \* out\_path
Path of the output compressed file (facultative)

--------------

**head**

head(fp, n=10, line\_numbering=False, ignore\_hashtag\_line=False)

Emulate linux head cmd. Handle gziped files

--------------

**is\_gziped**

is\_gziped(fp)

Return True if the file is Gziped else False

--------------

**is\_readable\_file**

is\_readable\_file(fp)

Verify the readability of a file or list of file

--------------

**jprint**

jprint(\*args,**kwargs)

FOR JUPYTER NOTEBOOK ONLY Format a string in HTML and print the output.
Equivalent of print, but highly customizable Many options can be passed
to the function. \* args One or several objects that can be cast in str
\* kwargs Formatting options to tweak the html rendering Boolean options
: bold, italic, highlight, underlined, striked, subscripted,
superscripted String oprions: font, color, size, align,
background\_color, line\_height

--------------

**larger\_display**

larger\_display(percent=100)

FOR JUPYTER NOTEBOOK ONLY Resize the area of the screen containing the
notebook according to a given percentage of the available width \*
percent percentage of the width of the screen to use [DEFAULT:100]

--------------

**linerange**

linerange(fp, range\_list=[], line\_numbering=True)

Print a range of lines in a file according to a list of start end lists.
Handle gziped files \* fp Path to the file to be parsed \* range\_list
list of start, end coordinates lists or tuples \* line\_numbering If
True the number of the line will be indicated in front of the line

--------------

**make\_cmd\_str**

make\_cmd\_str(prog\_name, opt\_dict={}, opt\_list=[])

Create a Unix like command line string from the prog name, a dict named
arguments and a list of unmammed arguments exemple make\_cmd\_str("bwa",
{"b":None, t":6, "i":"../idx/seq.fa"}, ["../read1", "../read2"]) \*
prog\_name Name (if added to the system path) or path of the program \*
opt\_dict Dictionary of option arguments such as "-t 5". The option flag
have to be the key (without "-") and the the option value in the
dictionary value. If no value is requested after the option flag "None"
had to be assigned to the value field. \* opt\_list List of simple
command line arguments

--------------

**mkdir**

mkdir(fp, level=1)

Reproduce the ability of UNIX "mkdir -p" command (ie if the path already
exits no exception will be raised). Can create nested directories by
recursivity \* fp path name where the folder should be created \*level
level in the path where to start to create the directories. Used by the
program for the recursive creation of directories

--------------

**print\_arg**

print\_arg()

Print calling function named and unnamed arguments

--------------

**reformat\_table**

reformat\_table(input\_file, output\_file='', return\_df=False,
init\_template=[], final\_template=[], header='',
keep\_original\_header=True, header\_from\_final\_template=False,
replace\_internal\_space='\_', replace\_null\_val='\*', subst\_dict={},
filter\_dict=[], predicate=None, standard\_template=None, verbose=False)

Reformat a table given an initial and a final line templates indicated
as a list where numbers indicate the data column and strings the
formatting characters

-  input\_file A file with a structured text formatting (gzipped or not)
-  output\_file A file path to output the reformatted table (if empty
   will not write in a file)
-  return\_df If true will return a pandas dataframe containing the
   reformated table (Third party pandas package required) by default the
   columns will be names after the final template [DEFAULT:False]
-  init\_template A list of indexes and separators describing the
   structure of the input file Example initial line = "chr1 631539
   631540 Squires\|id1 0 +" Initial template = [0," ",1," ",2,"
   ",3,"\|",4," ",5," ",6] Alternatively, instead of the numbers, string
   indexes can be used, but they need to be enclosed in curly brackets
   to differentiate them from the separators. This greatly simplify the
   writing of the final template. Example initial line = "chr1 631539
   631540 Squires\|id1 0 +" Initial template = ["{chrom}","
   ","{start}"," ","{end}","\|","{name}"," ","{score}"," ","{strand}"]
-  final\_template A list of indexes and separators describing the
   required structure of the output file. Name indexes need to match
   indexes of the init\_template and have to follow the same synthax
   [DEFAULT:Same that init template] Example final line = "chr1 631539
   631540 m5C\|-\|HeLa\|22344696 - -" Final template = [0," ",1," ",2,"
   m5C\|-\|HeLa\|22344696 - ",6]
-  header A string to write as a file header at the beginning of the
   file
-  keep\_original\_header If True the original header of the input file
   will be copied at the beginning of the output file [DEFAULT:True]
-  header\_from\_final\_template Generate a header according to the name
   or number of the fields given in the final\_template [DEFAULT:True]
-  replace\_internal\_space All internal blank space will be replaced by
   this character [DEFAULT:"\_"]
-  replace\_null\_val Field with no value will be replaced by this
   character [DEFAULT:"\*"]
-  subst\_dict Nested dictionary of substitution per position to replace
   specific values by others [DEFAULT:None] Example: {
   0:{"chr1":"1","chr2":"2"},
   3:{"Squires":"5376774764","Li":"27664684"}}
-  filter\_dict A dictionary of list per position to filter out lines
   with specific values [DEFAULT:None] Example: { 0:["chr2", "chr4"],
   1:["46767", "87765"], 5:["76559", "77543"]}
-  predicate A lambda predicate function for more advance filtering
   operations [DEFAULT:None] Example: lambda val\_dict:
   abs(int(val\_dict[1])-int(val\_dict[2])) <= 2000
-  standard\_template Existing standard template to parse the file
   instead of providing one manually. List of saved templates:

   -  "gff3\_ens\_gene" = Template for ensembl gff3 fields. Select only
      the genes lines and decompose to individual elements.
   -  "gff3\_ens\_transcript" = Template for ensembl gff3 fields. Select
      only the transcript lines and decompose to individual elements.
   -  "gtf\_ens\_gene" = Template for ensembl gft fields. Select only
      the genes lines and decompose to individual elements

-  verbose If True will print detailed information [DEFAULT:False]

--------------

**rm\_blank**

rm\_blank(name, replace='')

Replace blank spaces in a name by a given character (default = remove)
Blanks at extremities are always removed and nor replaced

--------------

**scp**

scp(hostname, local\_file, remote\_dir, username=None,
rsa\_private\_key=None, ssh\_config='~/.ssh/config')

Copy a file over ssh in a target remote directory \* hostname Name of
the host ssh server \* username name of the user \* rsa\_private\_key
path to the rsa private key \* local\_file path to the local file \*
remote\_dir path to the target directory \* ssh\_config use as an
alternative method instead of giving the username and rsa\_private\_key.
Will fetch them from the config file directly

--------------

**simplecount**

simplecount(fp, ignore\_hashtag\_line=False)

Simple way to count the number of lines in a file with more options

--------------

**supersplit**

supersplit(string, separator='')

like split but can take a list of separators instead of a simple
separator

--------------

**tail**

tail(fp, n=10, line\_numbering=False)

Emulate linux tail cmd. Handle gziped files

--------------

**toogle\_code**

toogle\_code()

FOR JUPYTER NOTEBOOK ONLY Hide code with a clickable link in a jupyter
notebook

--------------

**url\_exist**

url\_exist(url) Predicate verifying if an url exist without downloading
all the link

--------------

**wget**

wget(url, out\_name='', progress\_block=100000000)

Download a file from an URL to a local storage. \* url A internet URL
pointing to the file to download \* outname Name of the outfile where
(facultative) \* progress\_block size of the byte block for the
progression of the download

Authors and Contact
-------------------

Adrien Leger - 2017

Enright's group, EMBL EBI

-  aleg@ebi.ac.uk
-  `Github <https://github.com/a-slide>`__
