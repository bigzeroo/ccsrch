# CCSRCH

CCSRCH is a cross-platform tool for searching filesystems for credit card information.

### Copyright

Copyright (c) 2023 hwz <huowuzhao@gmail.com><br>
Copyright (c) 2012 UQ COMS3000 Assignment 2 Group (CCFinders) <uni@roganartu.com>  
Copyright (c) 2007 Mike Beekey <zaphod2718@yahoo.com>

This application is licensed under the GNU General Public License (see below & COPYING).

This project is a fork of CCSRCH as maintained by Mike Beekey at: http://sourceforge.net/projects/ccsrch/ - it is based on the last version (1.0.3) which was released in August 2007.

This readme is based on the readme from [https://github.com/roganartu/ccsrch]

### Using CCSRCH

```none
Usage: ./ccsrch <options> <start path>
  where <options> are:
    -b             Add the byte offset into the file of the number
    -e             Include the Modify Access and Create times in terms
                   of seconds since the epoch
    -f             Just output the filename with potential PAN data
    -j             Include the Modify Access and Create times in terms
                   of normal date/time
    -o <filename>  Output the data to the file <filename> vs. standard out
    -t <1 or 2>    Check if the pattern follows either a Track 1
                   or 2 format
    -T             Check for both Track 1 and Track 2 patterns
    -s             Stop parsing a file as soon as CHD is found
    -h             Usage information
```

**Examples:**

Generic search for credit card data starting in current directory with output to screen:

`ccsrch ./`

Generic search for credit card data starting in c:\storage with output to mycard.log:

`ccsrch -o mycard.log c:\storage`

Search for credit card data but stop processing a file as soon as CHD is found

`ccsrch -s c:\storage`

Search for credit card data and check for Track 2 data formats with output to screen:

`ccsrch -t 2 ./`

Search for credit card data and check for Track 2 data formats with output to file c.log:

`ccsrch -t 2 -o c.log ./`

### Output

All output is tab deliminated with the following order (depending on the parameters):

* Source File
* Line Number (not supported for all file types)
* Card Type
* Card Number
* Byte Offset
* Modify Time
* Access Time
* Create Time
* Track Pattern Match

### Assumptions

The following assumptions are made throughout the program searching for the 
card numbers:

1. Cards can be a minimum of 14 numbers and up to 16 numbers.
2. Card numbers must be contiguous. The only characters ignored when processing the files are carriage returns, new line feeds, and nulls.
3. Files are treated as raw binary objects and processed one character at a time.
4. Solo and Switch cards are not processed in the prefix search.
5. gzip, zip and tar archives are extracted and the archive files processed. Any other archive types must be manually extracted and checked.
6. The core of .xlsx and .docx files are extracted and then processed. All tag metadata is ignored (ie: any data between < and >). Any data between tags is processed as a contiguous block.
7. The line numbers for .docx and pdf files are unlikely to be hugely accurate. This is mostly due to the way they are extracted/converted before processing. They should give you a good idea of where to look, however.
8. XML data is processed as ASCII. If there is CHD spanning across multiple XML elements ccsrch will not find it. This could potentially be remedied by maintaining a second buffer for inside tags

**Prefix Logic**  
The following prefixes are used to validate the potential card numbers that have passed the mod 10 (Luhn) algorithm check.

Original Sources for Credit Card Prefixes:  
http://javascript.internet.com/forms/val-credit-card.html  
http://www.erikandanna.com/Business/CreditCards/credit_card_authorization.htm

### Logic Checks

```none
Card Type: MasterCard
Valid Length: 16
Valid Prefixes: 51, 52, 53, 54, 55

Card Type: VISA
Valid Length: 16
Valid Prefix: 4

Card Type: Discover
Valid Length: 16
Valid Prefix: 6011

Card Type: JCB
Valid Length: 16
Valid Prefixes: 3088, 3096, 3112, 3158, 3337, 3528, 3529

Card Type: American Express
Valid Length: 15
Valid Prefixes: 34, 37

Card Type: EnRoute
Valid Length: 15
Valid Prefixes: 2014, 2149

Card Type: JCB
Valid Length: 15
Valid Prefixes: 1800, 2131, 3528, 3529

Card Type: Diners Club, Carte Blanche
Valid Length: 14
Valid Prefixes: 36, 300, 301, 302, 303, 304, 305, 380, 381, 382, 383, 384, 385, 386, 387, 388
```

### Known Issues

One typical observation/complaint is the number of false positives that still come up. You will need to manually review and remove these. Certain patterns will repeatedly come up which match all of the criteria for valid cards, but are clearly bogus. If there are enough cries for help, I may add some additional sanity checks into the logic such as bank information. In addition, there are certain system files which clearly should not have cardholder data in them and can be ignored.  There may be an "ignore file list" in a new release to reduce the amount of stuff to go through, however this will impact the speed of the tool.

Note that since this program opens up each file and processes it, obviously the access time (in epoch seconds) will change.  If you are going to do forensics, one assumes that you have already collected an image following standard forensic practices and either have already collected and preserved the MAC times, or are using this tool on a copy of the image.

For the track data search feature, the tool just examines the preceding characters before the valid credit card number and either the delimiter, or the delimeter and the characters (e.g. expiration date) following the credit card number. This public release does not perform a full pattern match using the Track 1 or Track 2 formats.

We have found that for some POS software log files are generated that not only wrap across multiple lines, but insert hex representations of the ASCII values of the PAN data as well. Furthermore, these log files may contain track data. Remember that the only way that ccsrch will find the PAN data and track data is if it is contiguous. In certain instances you may luck out because the log files will contain an entire contigous PAN and will get flagged. We would encourage you to visually examine the files identified for confirmation. Introducing logic to capture all of the crazy possible storage representations of PAN and track data we've seen would make this tool a beast.

Please note that ccsrch recurses through the filesystem given a start directory and will attempt to open any file or object read-only one at a time. Given that this could be performance or load intensive depending on the existing load on the system or its configuration, we recommend that you run the tool on a subset or sample of directories first in order to get an idea of the potential impact. We disclaim all liability for any performance impact, outages, or problems ccsrch could cause.

Due to Windows not having a GNU licensed, portable pdftotext tool, it has no PDF parsing support.

### Porting

This tool has been successfully compiled and run on the following operating systems: FreeBSD, Linux, SCO 5.0.4-5.0.7, Solaris 8, AIX 4.1.X, Windows 2000, Windows XP, and Windows 7.  If you have any issues getting it to run on any systems, please contact the author.

### Building

#### Linux/Unix and OSX:  

```none
$ wget -O ccsrch.tar.gz https://github.com/roganartu/ccsrch/tarball/master
$ tar -xvzf ccsrch.tar.gz 
$ cd roganartu-ccsrch-<rev>/
$ make all
```  
You must have build-essential installed in order to make binaries.
Linux Users: Ensure you have pdftotext installed on your system. It is in the poppler-utils package which is included by default on most Unix systems.
OSX Users: pdftotext is not available to you through package managers. There is an included precompiled OSX binary, so you need not worry.

#### Windows:  
Install [Cygwin](http://www.cygwin.com/) ([installer](http://cygwin.com/setup.exe))  
Ensure you select the following packages for installation:
`file gzip tar unzip gcc-core gcc make`

After installing Cygwin, follow the instructions for installing on Unix systems, as shown above, using the cygwin terminal.

### Contributing

1. Contact me. Your modifications might already exist, be in progress or not be wanted
2. Fork
3. Make changes
4. Make tests. Your changes will not be accepted without tests
5. Submit a pull request

Don't change the version numbers. If you have to change the them, do it in a separate commit so I can ignore it when merging your pull request.

### Revisions

1.2.4 (Dec. 5, 2023):
* Added Print out the row where the card number is and the contents of the previous and next row of the row where the card number is,
  so that you can quickly determine whether it is a real card number.
* Added Ignore card number function and exclude suffix file scanning （These two functions come from the earliest version of ccsrch, and I added them here again.）
  https://github.com/bigzeroo/adamcaudill-ccsrch/blob/master/ccsrch.c

1.2.3 (Oct. 8, 2012):

* Added Windows installation instructions
* Changed gunzip to gzip

1.2.2 (Oct. 8, 2012):

* Fixed bug with display of results when .xlsx, .docx etc were extracted from within an archive
* General cleanup and refactor
* Updated Readme to reflect most recent changes
* Added second detect_file_type pass (omitting the --mime flag) if type resolves to UNKNOWN
* Added audio filetype detection and expended video detection. Added basic tests

1.2.1 (Oct. 8, 2012):

* Added ODS and OTS Open Document Spreadsheet handling
* Added ODS and OTS tests
* Fixed bug with temp directory removal

1.2.0 (Oct. 8, 2012):

* Added .docx Word handling
* Added .docx tests
* Added .xlsx tests
* Refactored test suite

1.1.0 (Oct. 8, 2012):

* Added .xlsx Excel handing
* Fixed pdf handling
* Added pdf tests
* Added debugging output
* Cleaned up pdf output in results

1.0.10 (Oct. 7, 2012):

* Added more possible mime types for Word and Excel files
* Added basic .xls Excel file parsing
* Added pdftotext docs to comply with license

1.0.9 (Oct. 7, 2012):

* Fixed pdf parsing on OSX
* Fixed potential segfault in print_result

1.0.8 (Oct. 7, 2012):

* Added line numbers to results
* Added compressed file tests
* Added checking of sub process exit codes
* Cleaned up compiler warnings

1.0.7 (Oct. 7, 2012):

* Added gzip and tar handling
* Added PDF handling

1.0.6 (Oct. 6, 2012):

* Added shortcut option
* Fixed unzip occasionally handing at prompt
* Added more file type detections
* Changed core of file type detection to use mime types instead of file tool strings
* Fixed bug with handling of absolute search paths

1.0.5 (Oct. 6, 2012):

* Modified character ignore logic to allow dynamic modification of ignore characters, depending on filetype.
* Added zip archive handling. Supports recursive extraction.
* Fixed bug in test suite regarding newer versions of waitpid
* Added file type detection using POSIX fork and file
* Added executable, image and binary detection and skipping using file type detection

1.0.4 (Sep. 3, 2012):

* Added basic test suite
* Detect parsing of log file through absolute paths, symlinks and hardlinks

1.0.3 (Aug. 28, 2007):

* Added the ability to just output filenames of potential PAN data.
* Removed the 13 digit VISA  number check.
* Cleaned up some error and signal handling that varied across operating systems.

1.0.2 (Dec. 12, 2005):

* Added some additional track data format assumptions for track 1.

1.0.1 (Sep. 27, 2005):

* Added options for searching files for track data patterns.
* Added the ability to select certain output options on the command line.

0.9.3 (Jul. 28, 2005):

* Removed extraneous calls.
* Simplified parameter passing. 
* Fixed non-portable type issues. 
* Removed debugging info.

0.9.1 (Jul. 15, 2005):

* Initial release.

### Contributors

#### New Source (From 1.0.4)
Tony L, Ashley K, Jonathan D, Justin V, Nils A, Dan B, Michael H

#### Original Source (Up to 1.0.3) - May be wrong. Hard to track down
John A, Kyley S, Anand S, Chris L, Mitch A, Bill L, Phoram M

### License

This program is free software; you can redistribute it and/or modify it under  the terms of the GNU General Public License as published by the Free  Software Foundation; either version 2 of the License, or (at your option)  any later version.
 
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

##程序的逻辑以及整体流程<br>
ccsrch.c和mods.c这两个C语言代码文件组成了ccsrch程序的源代码，它们共同工作来执行文件系统中的信用卡信息扫描任务。结合这两个代码文件，我们可以详细分析整个程序的执行流程和逻辑结构。

1. 程序的整体目标
ccsrch程序的主要目标是递归扫描指定的目录及其子目录中的文件，查找潜在的信用卡信息。该程序支持多种文件类型，能够解压缩压缩文件，解析特定格式的文档（如PDF、DOCX、XLSX），并使用多种算法和规则来检测和验证信用卡号。

2. 程序的主要组成部分
ccsrch的源代码可以分为两大部分：

ccsrch.c：这是程序的核心文件，负责整体控制流程、文件和目录扫描、信用卡号检测、输出结果等。
mods.c：提供了各种辅助功能，例如文件类型检测、文件解压缩、字符过滤、管道和进程管理等。
3. 整体执行流程分析
下面是ccsrch程序的整体执行流程，分为各个步骤进行详细分析：

1. 程序启动 (main 函数)
解析命令行参数：在main函数中，程序首先解析命令行参数，以确定扫描的选项和设置（如输出选项、要忽略的文件类型或信用卡号等）。常用选项包括：
-b：打印信用卡号在文件中的字节偏移。
-e：以纪元时间格式打印文件的修改、访问和创建时间。
-f：只打印文件名。
-o <filename>：将结果输出到指定文件。
-n <list>：排除特定的文件扩展名。
-i <filename>：忽略指定文件中的信用卡号。
初始化程序：调用initialise_mods函数对全局变量和状态进行初始化。该函数执行以下操作：
获取当前工作目录。
初始化跳过字符数组skipchars。
清空相关计数器（如跳过的可执行文件计数器、提取的归档文件计数器）。
设置初始状态（如父文件和文件类型跟踪）。
2. 打开日志文件 (可选)
如果指定了日志文件，程序会尝试打开日志文件以记录结果。
3. 设置信号处理函数
使用signal_proc函数设置信号处理程序，以便在接收到终止信号（如SIGINT、SIGTERM）时能够进行清理操作。
4. 检查输入路径
目录或文件判断：
使用check_dir函数检查指定的输入路径是目录还是文件。如果是目录，则调用proc_dir_list递归扫描该目录及其子目录中的所有文件；如果是文件，则直接调用ccsrch函数扫描该文件。
5. 递归扫描目录 (proc_dir_list 函数)
目录遍历：
使用opendir和readdir函数打开和读取目录中的每个文件和子目录。
对于每个条目，程序通过get_file_stat函数获取文件的状态信息，并检查其类型。
如果是子目录，则递归调用proc_dir_list函数继续遍历。
如果是普通文件，则调用ccsrch函数对文件进行扫描。
在目录扫描过程中，如果检测到特定的文件类型或满足特定条件，则可以根据命令行参数来决定是否跳过或解析该文件。
6. 文件扫描 (ccsrch 函数)
打开文件：使用fopen以二进制模式打开文件，并初始化必要的缓冲区和变量。
检测文件类型：
调用detect_file_type函数检测文件类型。该函数使用file命令来获取文件的MIME类型或其他类型信息，并返回一个枚举值（如ASCII、PDF、ZIP等）。
根据文件类型，程序决定如何处理文件。如果是可执行文件、图像、视频或音频文件，通常会跳过这些文件。
如果是压缩文件（如ZIP、GZIP、TAR）或特定类型文件（如PDF、DOCX、XLSX），则调用相应的处理函数进行解压和解析：
ZIP 文件：调用unzip_and_parse函数。
GZIP 文件：调用gunzip_and_parse函数。
TAR 文件：调用untar_and_parse函数。
PDF 文件：调用convert_and_parse_pdf函数。
XLSX 文件：调用parse_xlsx函数。
DOCX 文件：调用parse_docx函数。
处理文件内容：
读取文件内容到缓冲区ccsrch_buf，逐字符扫描内容。
使用buf_strstr函数和其他字符串匹配函数查找潜在的信用卡号模式（如卡号前缀、长度等）。
如果发现符合信用卡号格式的数据，则调用luhn_check函数执行Luhn算法验证其合法性。
对每个检测到的信用卡号，调用print_result函数输出结果。
7. 解析解压缩文件 (mods.c 文件中的函数)
解压缩和解析：
对于ZIP、GZIP、TAR等文件，程序使用子进程执行解压缩命令（如unzip、gzip、tar），并将结果输出重定向到管道中。
解压缩完成后，调用proc_dir_list函数递归解析解压后的目录或文件。
PDF 和文档文件解析：
使用类似的流程，将PDF文件转换为文本文件，或解压缩XLSX和DOCX文件，提取有用的内容进行扫描。
8. 处理扫描结果
对于每个检测到的信用卡号，调用print_result函数输出结果。
根据命令行参数的设置，结果可以打印到标准输出或写入日志文件。
输出的内容可能包括文件名、信用卡号、文件偏移量、时间戳等详细信息。
9. 结束处理
在扫描完成后，调用cleanup_shtuff和process_cleanup函数执行清理操作：
关闭日志文件（如果打开）。
释放动态分配的内存。
输出扫描统计信息（如扫描的文件数、匹配的信用卡号数量、跳过的文件数量等）。
4. 流程图总结
启动和初始化

解析命令行参数
初始化全局变量和状态
打开日志文件（如果指定）
信号处理设置

设置信号处理程序以应对程序中断
输入路径处理

检查输入路径（文件或目录）
如果是目录，递归扫描
如果是文件，直接扫描
文件类型检测和处理

检测文件类型
根据类型选择解析方法（直接扫描或解压缩后扫描）
内容扫描

扫描文件内容，查找潜在的信用卡信息
验证和输出结果
清理和退出

执行清理操作
输出统计信息
5. 关键特性和优化
灵活性：支持多种文件类型和格式的扫描，包括压缩文件、文档文件和PDF文件。
模块化设计：通过将主要功能拆分为不同的函数模块，增强了代码的可读性和可维护性。
高效性：使用管道和子进程（fork）来执行解压缩和文件类型检测命令，实现了并行和异步处理。
健壮性：通过大量的错误处理和信号管理，确保在文件操作、内存分配和进程管理中尽可能地避免程序崩溃。
6. 总结
ccsrch程序结合了ccsrch.c和mods.c文件的功能，实现了一个功能强大、灵活、高效的信用卡信息扫描工具。通过递归扫描目录、检测文件类型、解压缩和解析特定类型的文件，该程序能够在各种文件格式和环境下识别潜在的信用卡信息，并提供详细的扫描结果和统计信息。

##代码的调用关系以及执行逻辑<br>

```plaintext
ccsrch 程序的详细执行流程
1. 程序入口 (main 函数)
程序的入口是main函数：
解析命令行参数以获取用户提供的选项和文件/目录路径。
调用initialise_mods()进行初始化操作，设置全局变量和状态。
根据用户提供的日志文件选项，调用open_logfile()尝试打开日志文件。
使用signal_proc()设置信号处理函数，以处理可能的中断信号（如SIGINT、SIGTERM等）。
调用check_dir()函数检查输入路径是否是目录。
如果是目录，则调用proc_dir_list()递归扫描该目录及其子目录中的所有文件。
如果是文件，则直接调用ccsrch()函数扫描该文件。

2. 初始化模块 (initialise_mods 函数)
initialise_mods()：初始化一些全局变量和状态。
调用getcwd()获取当前工作目录。
设置skipchars为空，并调用reset_skip_chars()初始化跳过字符集（如空格、换行符等）。
清空计数器，如skipped_executable_count、extracted_archive_count。
初始化与解压缩文件处理相关的变量，如extracted_parent和filetype_parent。

3. 检查输入路径 (check_dir 函数)
check_dir(char *name)：检查输入路径是否为目录。
调用opendir()尝试打开目录。
如果打开成功，返回1表示是目录；否则返回0表示是文件。

4. 递归扫描目录 (proc_dir_list 函数)
proc_dir_list(char *instr)：递归扫描指定目录中的所有文件和子目录。
使用opendir()打开目录，readdir()读取每个目录项。
对于每个目录项，调用get_file_stat()获取文件状态信息。
如果是子目录，则递归调用proc_dir_list()继续扫描。
如果是普通文件，则调用ccsrch()对文件进行扫描。
检查文件类型，使用is_allowed_file_type()判断文件是否被排除在外。
对每个文件调用ccsrch()函数进行信用卡号扫描。

5. 获取文件状态 (get_file_stat 函数)
get_file_stat(char *inputfile, struct stat *fileattr)：获取文件的状态信息。
调用stat()函数获取文件状态，将状态信息存储在fileattr中。
返回0表示成功，返回-1表示失败。

6. 文件扫描和信用卡号检测 (ccsrch 函数)
ccsrch(char *filename)：核心扫描函数，用于对文件内容进行信用卡号检测。
调用fopen()以二进制模式打开文件，获取文件描述符infd。
初始化文件名currfilename、字节偏移量byte_offset等变量。
调用detect_file_type()检测文件类型，决定文件如何处理。
如果文件类型为可执行文件、图像、视频、音频或其他不需要处理的类型，则跳过该文件。
如果文件类型为压缩文件（ZIP、GZIP、TAR）或特定文档（PDF、DOCX、XLSX），则调用相应的处理函数进行解压缩和解析：
ZIP：unzip_and_parse(filename)
GZIP：gunzip_and_parse(filename)
TAR：untar_and_parse(filename)
PDF：convert_and_parse_pdf(filename)
XLSX：parse_xlsx(filename)
DOCX：parse_docx(filename, false)
如果是普通文件类型（如文本文件），则继续读取文件内容到缓冲区ccsrch_buf。
使用buf_strstr()函数查找潜在的信用卡号模式，逐字符进行扫描。
如果检测到潜在的信用卡号，调用luhn_check()函数执行Luhn算法验证其合法性。
对每个验证通过的信用卡号，调用print_result()函数输出结果。

7. 文件类型检测 (detect_file_type 函数)
detect_file_type(char *filename)：检测文件的类型。
调用pipe_and_fork()创建管道和子进程，用于执行file命令来获取文件类型信息。
解析file命令的输出，以确定文件的类型（如ASCII文本、PDF、ZIP、GZIP等）。
返回相应的文件类型枚举值（file_type）。

8. 解压缩和解析文件 (mods.c 中的解压缩和解析函数)
unzip_and_parse(char *filename)：解压缩ZIP文件并解析其内容。

调用mkdtemp()创建一个临时目录以解压缩文件。
调用pipe_and_fork()创建管道和子进程，执行unzip命令解压文件到临时目录。
解压完成后，调用proc_dir_list()递归扫描解压后的目录。
删除临时目录，释放资源。
gunzip_and_parse(char *filename)：解压缩GZIP文件并解析其内容。

使用mkstemp()创建一个临时文件以保存解压缩后的内容。
使用pipe_and_fork()创建管道和子进程，执行gzip命令解压文件到临时文件。
解压完成后，调用ccsrch()扫描临时文件。
删除临时文件，释放资源。
untar_and_parse(char *filename)：解压缩TAR文件并解析其内容。

使用mkdtemp()创建一个临时目录以解压缩文件。
使用pipe_and_fork()创建管道和子进程，执行tar命令解压文件到临时目录。
解压完成后，调用proc_dir_list()递归扫描解压后的目录。
删除临时目录，释放资源。
convert_and_parse_pdf(char *filename)：将PDF文件转换为文本文件并解析其内容。

使用mkstemp()创建一个临时文件以保存转换后的文本。
使用pipe_and_fork()创建管道和子进程，执行pdftotext命令将PDF文件转换为文本文件。
转换完成后，调用ccsrch()扫描转换后的文本文件。
删除临时文件，释放资源。
parse_xlsx(char *filename)：解析XLSX文件。

将XLSX文件作为ZIP文件解压缩，并提取相关的XML内容进行扫描。
调用ccsrch()扫描提取的XML文件。
parse_docx(char *filename, bool ods)：解析DOCX文件。

类似于XLSX文件的处理方式，将DOCX文件作为ZIP文件解压缩并提取XML内容。
调用ccsrch()扫描提取的XML文件。

9. 打印结果 (print_result 函数)
print_result(char *cardname, int cardlen, long byte_offset)：打印和记录扫描结果。
生成包含文件名、信用卡号、字节偏移量等信息的结果字符串。
根据选项决定输出到标准输出还是日志文件。
调用find_card()函数查找文件中包含卡号的行。

10. 查找文件中的卡号行 (find_card 函数)
find_card(char *currfilename)：使用awk和strings命令查找文件中包含卡号的行。
创建管道和子进程，调用strings命令提取文本数据。
使用awk命令提取包含卡号的行及其前后行，以便更好地确认卡号的真实性。

11. 结束处理和清理 (cleanup_shtuff 和 process_cleanup 函数)
cleanup_shtuff()：清理操作，包括输出扫描统计信息和释放动态分配的内存。
process_cleanup()：用于在接收到信号时调用的清理函数。调用cleanup_shtuff()并关闭日志文件。

12. 信号处理 (signal_proc 函数)
signal_proc()：设置信号处理程序，确保在接收到SIGHUP、SIGTERM、SIGINT、SIGQUIT等信号时调用process_cleanup()进行清理操作.
```

## 函数调用关系图
```plaintext
main()
  ├── initialise_mods()
  ├── open_logfile()
  ├── signal_proc()
  ├── check_dir()
  │   ├── if (directory) ──> proc_dir_list()
  │   │                        ├── get_file_stat()
  │   │                        ├── is_allowed_file_type()
  │   │                        └── ccsrch()
  │   │                            ├── detect_file_type()
  │   │                            │   └── pipe_and_fork()
  │   │                            ├── unzip_and_parse()
  │   │                            │   ├── mkdtemp()
  │   │                            │   ├── pipe_and_fork()
  │   │                            │   ├── proc_dir_list()
  │   │                            │   └── remove_directory()
  │   │                            ├── gunzip_and_parse()
  │   │                            │   ├── mkstemp()
  │   │                            │   ├── pipe_and_fork()
  │   │                            │   └── remove()
  │   │                            ├── untar_and_parse()
  │   │                            │   ├── mkdtemp()
  │   │                            │   ├── pipe_and_fork()
  │   │                            │   ├── proc_dir_list()
  │   │                            │   └── remove_directory()
  │   │                            ├── convert_and_parse_pdf()
  │   │                            │   ├── mkstemp()
  │   │                            │   ├── pipe_and_fork()
  │   │                            │   └── remove()
  │   │                            ├── parse_xlsx()
  │   │                            │   ├── mkdtemp()
  │   │                            │   ├── pipe_and_fork()
  │   │                            │   ├── ccsrch()
  │   │                            │   └── remove_directory()
  │   │                            ├── parse_docx()
  │   │                            │   ├── mkdtemp()
  │   │                            │   ├── pipe_and_fork()
  │   │                            │   ├── ccsrch()
  │   │                            │   └── remove_directory()
  │   │                            └── luhn_check()
  │   │                                └── print_result()
  │   │                                    └── find_card()
  └── cleanup_shtuff()
      └── process_cleanup()

```
