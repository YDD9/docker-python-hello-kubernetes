---
layout: post
title:  "shell"
date:   2017-12-19 14:58:39 +0100
comments: true
categories: shell
---

- [1) What is Linux?](#1-what-is-linux)
- [2) What is the difference between UNIX and LINUX?](#2-what-is-the-difference-between-unix-and-linux)
- [3) What is BASH?](#3-what-is-bash)
- [4) What is Linux Kernel?](#4-what-is-linux-kernel)
- [5) What is LILO?](#5-what-is-lilo)
- [6) What is a swap space?](#6-what-is-a-swap-space)
- [7) What is the advantage of open source?](#7-what-is-the-advantage-of-open-source)
- [9) Does it help for a Linux system to have multiple desktop environments installed?](#9-does-it-help-for-a-linux-system-to-have-multiple-desktop-environments-installed)
- [10) What is the basic difference between BASH and DOS?](#10-what-is-the-basic-difference-between-bash-and-dos)
- [11) What is the importance of the GNU project?](#11-what-is-the-importance-of-the-gnu-project)
- [12) Describe the root account.](#12-describe-the-root-account)
- [13) What is CLI?](#13-what-is-cli)
- [14) What is GUI?](#14-what-is-gui)
- [15) How do you open a command prompt when issuing a command?](#15-how-do-you-open-a-command-prompt-when-issuing-a-command)
- [16) How can you find out how much memory Linux is using?](#16-how-can-you-find-out-how-much-memory-linux-is-using)
- [17) What is typical size for a swap partition under a Linux system?](#17-what-is-typical-size-for-a-swap-partition-under-a-linux-system)
- [18) What are symbolic links?](#18-what-are-symbolic-links)
- [19) Does the Ctrl+Alt+Del key combination work on Linux?](#19-does-the-ctrlaltdel-key-combination-work-on-linux)
- [20) How do you refer to the parallel port where devices such as printers are connected?](#20-how-do-you-refer-to-the-parallel-port-where-devices-such-as-printers-are-connected)
- [21) Are drives such as harddrive and floppy drives represented with drive letters?](#21-are-drives-such-as-harddrive-and-floppy-drives-represented-with-drive-letters)
- [22) How do you change permissions under Linux?](#22-how-do-you-change-permissions-under-linux)
- [23) In Linux, what names are assigned to the different serial ports?](#23-in-linux-what-names-are-assigned-to-the-different-serial-ports)
- [whatis dmesg](#whatis-dmesg)
- [24) How do you access partitions under Linux?](#24-how-do-you-access-partitions-under-linux)
- [25) What are hard links?](#25-what-are-hard-links)
- [26) What is the maximum length for a filename under Linux?](#26-what-is-the-maximum-length-for-a-filename-under-linux)
- [27)What are filenames that are preceded by a dot?](#27what-are-filenames-that-are-preceded-by-a-dot)
- [28) Explain virtual desktop.](#28-explain-virtual-desktop)
- [29) How do you share a program across different virtual desktops under Linux?](#29-how-do-you-share-a-program-across-different-virtual-desktops-under-linux)
- [30) What does a nameless (empty) directory represent?](#30-what-does-a-nameless-empty-directory-represent)
- [31) What is the pwd command?](#31-what-is-the-pwd-command)
- [32) What are daemons?](#32-what-are-daemons)
- [33) How do you switch from one desktop environment to another, such as switching from KDE to Gnome?](#33-how-do-you-switch-from-one-desktop-environment-to-another-such-as-switching-from-kde-to-gnome)
- [34) What are the kinds of permissions under Linux?](#34-what-are-the-kinds-of-permissions-under-linux)
- [35) How does case sensitivity affect the way you use commands?](#35-how-does-case-sensitivity-affect-the-way-you-use-commands)
- [36) What are environmental variables?](#36-what-are-environmental-variables)
- [37) What are the different modes when using vi editor?](#37-what-are-the-different-modes-when-using-vi-editor)
- [38) Is it possible to use shortcut for a long pathname?](#38-is-it-possible-to-use-shortcut-for-a-long-pathname)
- [39) What is redirection?](#39-what-is-redirection)
- [40) What is grep command?](#40-what-is-grep-command)
- [41) What could possibly be the problem when a command that was issued gave a different result from the last time it was used?](#41-what-could-possibly-be-the-problem-when-a-command-that-was-issued-gave-a-different-result-from-the-last-time-it-was-used)
- [42) What are the contents in /usr/local?](#42-what-are-the-contents-in-usrlocal)
- [43) How do you terminate an ongoing process?](#43-how-do-you-terminate-an-ongoing-process)
- [44) How do you insert comments in the command line prompt?](#44-how-do-you-insert-comments-in-the-command-line-prompt)
- [45) What is command grouping and how does it work?](#45-what-is-command-grouping-and-how-does-it-work)
- [46) How do you execute more than one command or program from a single command line entry?](#46-how-do-you-execute-more-than-one-command-or-program-from-a-single-command-line-entry)
- [47) Write a command that will look for files with an extension “c”, and has the occurrence of the string “apple” in it.](#47-write-a-command-that-will-look-for-files-with-an-extension-%E2%80%9Cc%E2%80%9D-and-has-the-occurrence-of-the-string-%E2%80%9Capple%E2%80%9D-in-it)
- [48) Write a command that will display all .txt files, including its individual permission.](#48-write-a-command-that-will-display-all-txt-files-including-its-individual-permission)
- [49) Write a command that will do the following:](#49-write-a-command-that-will-do-the-following)
- [50) What, if anything, is wrong with each of the following commands?](#50-what-if-anything-is-wrong-with-each-of-the-following-commands)
- [51) commond seq https://www.lifewire.com/uses-of-linux-seq-command-4011324](#51-commond-seq-httpswwwlifewirecomuses-of-linux-seq-command-4011324)
- [52) Linux List The Open Ports And The Process That Owns Them](#52-linux-list-the-open-ports-and-the-process-that-owns-them)
- [53) How to use awk](#53-how-to-use-awk)
- [54) How to find the total number of folders in Linux](#54-how-to-find-the-total-number-of-folders-in-linux)
- [centOS yum install conflicts](#centos-yum-install-conflicts)
- [55) How to rename a file or many files](#55-how-to-rename-a-file-or-many-files)
- [56) Linux common commands](#56-linux-common-commands)
- [57) iptables](#57-iptables)
- [58) How to count words in a file](#58-how-to-count-words-in-a-file)
- [other links](#other-links)


# 1) What is Linux?
Linux is an operating system based on UNIX, and was first introduced by Linus Torvalds. It is based on the Linux Kernel, and can run on different hardware platforms manufactured by Intel, MIPS, HP, IBM, SPARC and Motorola. Another popular element in Linux is its mascot, a penguin figure named Tux.


# 2) What is the difference between UNIX and LINUX?

Unix originally began as a propriety operating system from Bell Laboratories, which later on spawned into different commercial versions. On the other hand, Linux is free, open source and intended as a non-propriety operating system for the masses.

# 3) What is BASH?

BASH is short for Bourne Again SHell. It was written by Steve Bourne as a replacement to the original Bourne Shell (represented by /bin/sh). It combines all the features from the original version of Bourne Shell, plus additional functions to make it easier and more convenient to use. It has since been adapted as the default shell for most systems running Linux.

# 4) What is Linux Kernel?

The Linux Kernel is a low-level systems software whose main role is to manage hardware resources for the user. It is also used to provide an interface for user-level interaction.

# 5) What is LILO?

LILO is a boot loader for Linux. It is used mainly to load the Linux operating system into main memory so that it can begin its operations.

# 6) What is a swap space?

A swap space is a certain amount of space used by Linux to temporarily hold some programs that are running concurrently. This happens when RAM does not have enough memory to hold all programs that are executing.

# 7) What is the advantage of open source?

Open source allows you to distribute your software, including source codes freely to anyone who is interested. People would then be able to add features and even debug and correct errors that are in the source code. They can even make it run better, and then redistribute these enhanced source code freely again. This eventually benefits everyone in the community.


8 ) What are the basic components of Linux?

Just like any other typical operating system, Linux has all of these components: kernel, shells and GUIs, system utilities, and application program. What makes Linux advantageous over other operating system is that every aspect comes with additional features and all codes for these are downloadable for free.

# 9) Does it help for a Linux system to have multiple desktop environments installed?

In general, one desktop environment, like KDE or Gnome, is good enough to operate without issues. It’s all a matter of preference for the user, although the system allows switching from one environment to another. Some programs will work on one environment and not work on the other, so it could also be considered a factor in selecting which environment to use.

# 10) What is the basic difference between BASH and DOS?

The key differences between the BASH and DOS console lies in 3 areas:
– BASH commands are case sensitive while DOS commands are not;
– under BASH, / character is a directory separator and acts as an escape character. Under DOS, / serves as a command argument delimiter and is the directory separator
– DOS follows a convention in naming files, which is 8 character file name followed by a dot and 3 character for the extension. BASH follows no such convention.

# 11) What is the importance of the GNU project?

This so-called Free software movement allows several advantages, such as the freedom to run programs for any purpose and freedom to study and modify a program to your needs. It also allows you to redistribute copies of a software to other people, as well as freedom to improve software and have it released to the public.

# 12) Describe the root account.

The root account is like a systems administrator account, and allows you full control of the system. Here you can create and maintain user accounts, assigning different permissions for each account. It is the default account every time you install Linux.

# 13) What is CLI?

CLI is short for Command Line Interface. This interface allows user to type declarative commands to instruct the computer to perform operations. CLI offers an advantage in that there is greater flexibility. However, other users who are already accustom with using GUI find it difficult to remember commands including attributes that come with it.

# 14) What is GUI?

GUI, or Graphical User Interface, makes use of images and icons that users click and manipulate as a way of communicating with the computer. Instead of having to remember and type commands, the use of graphical elements makes it easier to interact with the system, as well as adding more attraction through images, icons and colors.

# 15) How do you open a command prompt when issuing a command?

To open the default shell (which is where the command prompt can be found), press Ctrl-Alt-F1. This will provide a command line interface (CLI) from which you can run commands as needed.

# 16) How can you find out how much memory Linux is using?

From a command shell, use the “concatenate” command: cat /proc/meminfo for memory usage information. You should see a line starting something like: Mem: 64655360, etc. This is the total memory Linux thinks it has available to use.


http://www.binarytides.com/linux-command-check-memory-usage/


cat /proc/meminfo
free -m

top

gnome-system-monitor Gnome desktop



# 17) What is typical size for a swap partition under a Linux system?

The preferred size for a swap partition is twice the amount of physical memory available on the system. If this is not possible, then the minimum size should be the same as the amount of memory installed.

# 18) What are symbolic links?


Symbolic links act similarly to shortcuts in Windows. Such links point to programs, files or directories. It also allows you instant access to it without having to go directly to the entire pathname.

To create a symbolic link in Unix, at the Unix prompt, enter:

 ln -s source_file myfile
To view the symbolic links in a directory:
Open a terminal and move to that directory.
Type the command: ls -la. This shall long list all the files in the directory even if they are hidden.
The files that start with l are your symbolic link files.
You can use rm to delete the symlink.

Example:

-rw-rw-r-- 1 2014-01-02 09:21 tmo
lrwxrwxrwx 1 2014-01-02 09:21 tmo2 -> tmo
Then ...

 rm tmo2
will remove the symlink


# 19) Does the Ctrl+Alt+Del key combination work on Linux?

Yes, it does. Just like Windows, you can use this key combination to perform a system restart. One difference is that you won’t be getting any confirmation message and therefore, reboot is immediate.

# 20) How do you refer to the parallel port where devices such as printers are connected?

Whereas under Windows you refer to the parallel port as the LPT port, under Linux you refer to it as /dev/lp . LPT1, LPT2 and LPT3 would therefore be referred to as /dev/lp0, /dev/lp1, or /dev/lp2 under Linux.

A parallel port is a type of interface found on computers (personal and otherwise) for connecting peripherals. In computing, a parallel port is a parallel communication physical interface. It is also known as a printer port or Centronics port.



# 21) Are drives such as harddrive and floppy drives represented with drive letters?

No. In Linux, each drive and device has different designations. For example, floppy drives are referred to as /dev/fd0 and /dev/fd1. IDE/EIDE hard drives are referred to as /dev/hda, /dev/hdb, /dev/hdc, and so forth.

# 22) How do you change permissions under Linux?

Assuming you are the system administrator or the owner of a file or directory, you can grant permission using the chmod command. Use + symbol to add permission or – symbol to deny permission, along with any of the following letters: u (user), g (group), o (others), a (all), r (read), w (write) and x (execute). For example the command chmod go+rw FILE1.TXT grants read and write access to the file FILE1.TXT, which is assigned to groups and others.


http://www.computerhope.com/unix/uchmod.htm

equivalent command


chmod u=rwx,g=rx,o=r myfile
chmod 754 myfile


# 23) In Linux, what names are assigned to the different serial ports?

Serial ports are identified as /dev/ttyS0 to /dev/ttyS7. These are the equivalent names of COM1 to COM8 in Windows.    Linux uses ttySx for a serial port device name. 

https://www.cyberciti.biz/faq/find-out-linux-serial-ports-with-setserial/

# whatis dmesg

dmesg (# 1)            - print or control the kernel ring buffer
Display Detected System’s Serial Support

Simple run dmesg command
$ dmesg | grep tty


# 24) How do you access partitions under Linux?

Linux assigns numbers at the end of the drive identifier. For example, if the first IDE hard drive had three primary partitions, they would be named/numbered, /dev/hda1, /dev/hda2 and /dev/hda3.

/dev/hd* – IDE disks. /dev/hda will be first IDE hard disk, /dev/hdb will be second IDE hard disk, and so on.
/dev/sd* – SCSI or SATA disks. /dev/sda will be first SATA/SCSI hard disk, /dev/sdb will be second SATA/SCSI hard disk, and so on.
List Partitions Under Linux
Open a terminal window (select Applications > Accessories > Terminal). Switch to the root user by typing su – and entering the root password, when prompted. Or use sudo command:
$ sudo fdisk -l

To list all block devices, run: `lsblk`

# 25) What are hard links?

Hard links point directly to the physical file on disk, and not on the path name. This means that if you rename or move the original file, the link will not break, since the link is for the file itself, not the path where the file is located.

# 26) What is the maximum length for a filename under Linux?

Any filename can have a maximum of 255 characters. This limit does not include the path name, so therefore the entire pathname and filename could well exceed 255 characters.

# 27)What are filenames that are preceded by a dot?

In general, filenames that are preceded by a dot are hidden files. These files can be configuration files that hold important data or setup info. Setting these files as hidden makes it less likely to be accidentally deleted.

# 28) Explain virtual desktop.

This serves as an alternative to minimizing and maximizing different windows on the current desktop. Using virtual desktops, each desktop is a clean slate where you can open one or more programs. Rather than minimizing/restoring all those programs as needed, you can simply shuffle between virtual desktops with programs intact in each one.

# 29) How do you share a program across different virtual desktops under Linux?

To share a program across different virtual desktops, in the upper left-hand corner of a program window look for an icon that looks like a pushpin. Pressing this button will “pin” that application in place, making it appear in all virtual desktops, in the same position onscreen.

xfce desktop with debian, left click left top incon, and choose Always on Visible Workplace.
# 30) What does a nameless (empty) directory represent?

This empty directory name serves as the nameless base of the Linux file system. This serves as an attachment for all other directories, files, drives and devices.

# 31) What is the pwd command?

The pwd command is short for print working directory command. It’s counterpart in DOS is the cd command, and is used to display the current location in the directory tree.

# 32) What are daemons?

Daemons are services that provide several functions that may not be available under the base operating system. Its main task is to listen for service request and at the same time to act on these requests. After the service is done, it is then disconnected and waits for further requests.

backgroud process.

In multitasking computer operating systems, a daemon (/ˈdiːmən/ or /ˈdeɪmən/)[1] is a computer program that runs as a background process, rather than being under the direct control of an interactive user. Traditionally, the process names of a daemon end with the letter d, for clarification that the process is, in fact, a daemon, and for differentiation between a daemon and a normal computer program. For example,syslogd is the daemon that implements the system logging facility, and sshd is a daemon that services incoming SSH connections.

In a Unix environment, the parent process of a daemon is often, but not always, the init process. A daemon is usually either created by a process forking a child process and then immediately exiting, thus causing init to adopt the child process, or by the init process directly launching the daemon. In addition, a daemon launched by forking and exiting typically must perform other operations, such as dissociating the process from any controlling terminal (tty). Such procedures are often implemented in various convenience routines such as daemon(# 3) in Unix.

Systems often start daemons at boot time and serve the function of responding to network requests, hardware activity, or other programs by performing some task. Daemons can also configure hardware (like udevd on some Linux systems), run scheduled tasks (like cron), and perform a variety of other tasks.


# 33) How do you switch from one desktop environment to another, such as switching from KDE to Gnome?

Assuming you have these two environments installed, just log out from the graphical interface. Then at the Log in screen, type your login ID and password and choose which session type you wish to load. This choice will remain your default until you change it to something else.

# 34) What are the kinds of permissions under Linux?

There are 3 kinds of permissions under Linux:
– Read: users may read the files or list the directory
– Write: users may write to the file of new files to the directory
– Execute: users may run the file or lookup a specific file within a directory

# 35) How does case sensitivity affect the way you use commands?

When we talk about case sensitivity, commands are considered identical only if every character is encoded as is, including lowercase and uppercase letters. This means that CD, cd and Cd are three different commands. Entering a command using uppercase letters, where it should be in lowercase, will produce different outputs.

# 36) What are environmental variables?

Environmental variables are global settings that control the shell’s function as well as that of other Linux programs. Another common term for environmental variables is global shell variables.

# 37) What are the different modes when using vi editor?

There are 3 modes under vi:
– Command mode – this is the mode where you start in
– Edit mode – this is the mode that allows you to do text editing
– Ex mode – this is the mode wherein you interact with vi with instructions to process a file

# 38) Is it possible to use shortcut for a long pathname?

Yes, there is. A feature known as filename expansion allows you do this using the TAB key. For example, if you have a path named /home/iceman/assignments directory, you would type as follows: /ho[tab]/ice[tab]/assi[tab] . This, however, assumes that the path is unique, and that the shell you’re using supports this feature.

# 39) What is redirection?

Redirection is the process of directing data from one output to another. It can also be used to direct an output as an input to another process.

curl urlYMAL | kubeclt apply -f -

# 40) What is grep command?

grep a search command that makes use of pattern-based searching. It makes use of options and parameters that is specified along the command line and applies this pattern into searching the required file output.

https://www.cyberciti.biz/faq/howto-use-grep-command-in-linux-unix/


How To Use grep Command In Linux / UNIX - nixCraft
www.cyberciti.biz
This step-by-step guide explains how to use grep command on Linux or Unix-like operating system with plenty of practical examples to search files.
 you can force grep to display output in --color, or simply output the number of occurance:
$ grep --color <keyword> /etc/passwd
$ grep -c <keyword> /ect/passwd
Use the egrep command as follows:
$ egrep -w 'word1|word2' /path/to/file
Pass the -n option to precede each line of output with the number of the line in the text file from which it was obtained:
$ grep -n 'root' /etc/passwd

grep can be used together with regex, put regex inside single quote.   
https://www.cyberciti.biz/faq/searching-multiple-words-string-using-grep/    

```
grep 'word1\|word2\|word3' /path/to/file
grep '^redis*'
```

# 41) What could possibly be the problem when a command that was issued gave a different result from the last time it was used?

One highly possible reason for getting different results from what seems to be the same command has something to do with case sensitivity issues. Since Linux is case sensitive, a command that was previously used might have been entered in a different format from the present one. For example, to lists all files in the directory, you should type the command ls, and not LS. Typing LS would either result in an error message if there is no program by that exact name exist, or may produce a different output if there is a program named LS that performs another function.

# 42) What are the contents in /usr/local?

It contains locally installed files. This directory actually matters in environments where files are stored on the network. Specifically, locally-installed files go to /usr/local/bin, /usr/local/lib, etc.). Another application of this directory is that it is used for software packages installed from source, or software not officially shipped with the distribution.

# 43) How do you terminate an ongoing process?

Every process in the system is identified by a unique process id or pid. Use the kill command followed by the pid in order to terminate that process. To terminate all process at once, use kill 0.

# 44) How do you insert comments in the command line prompt?

Comments are created by typing the # symbol before the actual comment text. This tells the shell to completely ignore what follows. For example: “# This is just a comment that the shell will ignore.”

# 45) What is command grouping and how does it work?

You can use parentheses to group commands. For example, if you want to send the current date and time along with the contents of a file named OUTPUT to a second file named MYDATES, you can apply command grouping as follows: (date cat OUTPUT) > MYDATES

# 46) How do you execute more than one command or program from a single command line entry?

You can combine several commands by separating each command or program using a semicolon symbol. For example, you can issue such a series of commands in a single entry: 

 A ; B  – Run A and then B, regardless of the success or failure of A
 A && B  – Run B only if A succeeded
 A || B  – Run B only if A failed
# 47) Write a command that will look for files with an extension “c”, and has the occurrence of the string “apple” in it. 

1


Find ./ -name “*.c” | xargs grep –i “apple”

find -name need  " ", returns each row a filename ending .c

Case insensitive:  -i

xargs: get the output from preceding expression and feed into the next command.

# 48) Write a command that will display all .txt files, including its individual permission.
1


ls -a -l *.txt


list directory contents

http://man7.org/linux/man-pages/man1/ls.1.html


-a --all, do no ignore *.txt

-l, using a long listing format. 



# 49) Write a command that will do the following:
-look for all files in the current and subsequent directories with an extension c,v,C,V
-strip(delete) the,v from the result (you can use sed command)
-use the result and use a grep command to search for all occurrences of the word ORANGE in the files.

1


Find ./ -iname “*.c,v” | sed ‘s/,v//g’ | xargs grep “ORANGE”


http://www.computerhope.com/unix/used.htm


sed:


s command 's/Regularexpression/Replacement/Flag'

Flag g: apply replacement to all match, not only the first.


| xargs: get the output from preceding expression and feed into the next command.


https://unix.stackexchange.com/questions/15308/how-to-use-find-command-to-search-for-multiple-extensions 

find ./ -type f \( -iname \*.yml-o -iname \*.yaml\)
find ./ \( -iname "*.yml" -o -iname "*.yaml" \)



Both \*.jpg "*.jpg" work
-o means or
-iname must before search pattern
Very important to have white space before and after \(


use non case sensitive -iregex 

find ./ -iregex '.*\.\(yaml\|yml\)$'


# 50) What, if anything, is wrong with each of the following commands?

a) ls -l-s
b) cat file1, file2
c) ls – s Factdir


Answers:
a) there should be space between the 2 options: ls -l -s
b) do not use commas to separate arguments: cat file1 file2
c) there should be no space between hyphen and option label: ls –s Factdir



# 51) commond seq https://www.lifewire.com/uses-of-linux-seq-command-4011324

seq 10: gives you 1 to 10, ten numbers in 10 rows.

seq -f '%02g/01/2018' 10, ten numbers 01,  02, ..., 10


-f: format to %02g


# 52) Linux List The Open Ports And The Process That Owns Them

https://www.cyberciti.biz/tips/linux-display-open-ports-owner.html

list all

sudo lsof -i 

list for a specific port `sudo lsof -i :<port>`

check a pid source `ls -l /proc/<pid>/exe`

old method `sudo netstat -tulpn`

# 53) How to use awk

awk can be used to filter as well  
https://www.cyberciti.biz/faq/bash-scripting-using-awk/   
```
awk '{ print }' /etc/passwd

awk '{ print $0 }' /etc/passwd
# use ':' to seperate and print the first field
awk -F':' '{ print $1 }' /etc/passwd

# Pattern Matching
# You can only print line of the file if pattern matched. 
For e.g. display all lines from Apache log file if HTTP error code is 500 
(9th field logs status error code for each http request):
awk '$9 == 500 { print $0}' /var/log/httpd/access.log
```

# 54) How to find the total number of folders in Linux
http://mp.weixin.qq.com/s/ltvNiHcyH1_5mljtLPsI4g

# centOS yum install conflicts
[yum update or yum install fails with package conflict:](https://access.redhat.com/solutions/# 158883)
Install the yum-utils package:
`yum install yum-utils`    

The package-cleanup --dupes lists all duplicate packages:
`package-cleanup --dupes`  

The package-cleanup --cleandupes removes the duplicates (it asks for a confirmation to remove all duplicates unless the -y switch is given):
`package-cleanup --cleandupes`   

Edit /etc/yum.conf, set the following line:
`exactarch=1`    

Run yum command:
```
yum clean all
yum update
```  

# 55) How to rename a file or many files
https://www.cyberciti.biz/faq/linux-rename-file/

# 56) Linux common commands
http://mp.weixin.qq.com/s/NKfnIcbNB-k21RorSVlddw

# 57) iptables
https://www.digitalocean.com/community/tutorials/how-to-list-and-delete-iptables-firewall-rules
https://www.howtogeek.com/177621/the-beginners-guide-to-iptables-the-linux-firewall/

# 58) How to count words in a file
https://www.computerhope.com/unix/uwc.htm
```
$ wc myfile.txt
87 157 1505 myfile.txt
# lines words chars

$ ls -1 | wc -l
# count the number of folders and files in current dir
```

# other links
http://mp.weixin.qq.com/s/Lvu8IL6zv9PzDb2oSte3pA
`mount | column –t mount |column –t :`  output as a table


