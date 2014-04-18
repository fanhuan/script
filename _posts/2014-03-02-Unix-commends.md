---
layout: post
title:  Unix shell commends
categories: [notes]
tags: [computer]
---
I tried a couple of times to switch from Windows to Ubuntu, but failed, mainly because that I do not have enough time and patient
to teach myself. 

Last week, I heared [a great class](http://kbroman.github.io/Tools4RR/) is giving this semester at UW-Madison. After look at
its website, I felt that it may be a good time to pick the Ubuntu up, again. And try to learn the commend line. 

Here is a list of the most basic commends in Unix from what I learned today.

### Basic system commends
+ `cd Documents` to change to the Documents sub-folder.
+ `cd` to change to your home directory.
+ `cd ..` to change to the parent directory.
+ `.` means current directory.
+ `..` means one level up of current directory, i.e. parent directory.
+ `~` is the shortcut of the home directory. e.g. `cd ~`, same effect as `cd`.
+ `tab` to autocomplete, e.g. `cd b<tab>` will autocomplete the directory name begin with `b` (if it exits).
+ `pwd` to print the path of the current working directory.
+ `ln -s` creates symbolic links. `ln -s Documents Docs`. Then Docs -> Documents.
+ `ls -l` reveal where a symlink points and permission info. e.g. Docs -> Documents in the above example. `-S` sort files by size.
+ `ls /bin/*a* /bin/*b*` list all files in /bin that contain the letter a or b.
+ `man command` to check what a command does. e.g. `man ls`. Press `q` to quit. `man` use `less` internal, so you can use `/` to search for something.
+ `history` to check all commend used.
+ `!220` to rerun the 220th commend from history
+ `|` is used for piping, i.e. use output of one commend as input of another. 
+ `Ctrl+d` will send "end of file' and will often terminate the shell.
+ `ls /bin/*sh` will list all shells available.
+ `df -h` to get the disk of file system used (short of disk free?), `-h` means return human readable numbers, e.g. 100Mb. 100Gb.
+ `du -hs /path/to/directory` get the total size of the directory. `du` means disk usage, `-h` as above, `-s` means summary.
+ `env` to view the current values of environment variables.
+ `PATH` the environment path of a program. e.g. `echo $PATH` will print a list of places the shell will ONLY look for a program to run.
+ `which` print the location of a program. e.g. `which ls`.
+ `uname -a` print the system information.
+ `lsb_release -a` print Linux standard base distribution-specific information.


### File related
+ `command > file` dump the standard output into a file. e.g. `pwd > pwd.txt`, then you can use `cat pwd.txt` to have a look at the file. `>` will rewrite a file if it already exits. `>>` will append to an exist file instead of rewrite it.
+ `mkdir /tmp/user` will create a new directory named as user. All files in `/tmp` will be deleted after computer shutdown.
+ `cat day1.R` have a look at a text file in within the current directory, e.g. day1.R. You can also use `cat day1.R day2.R` to print two files. `cat day*` will print all files begin with day. You can also use `cat day* > all.R` to save all files into one file.
+ `cat filefolder/*` print the contents of all of the files in the filefolder directory.
+ `less day1.R` only read a few part of day1.R. Press `q` to quit the reading, `space` to go forward, `b` to go backward, `g` to go to the begining, `G` to go to the end, `/` to search a word, but only forwardly.
+ `cp file file_backup` copy a file.
+ `mv file_backup /tmp/user` move the file into the /tmp/user directory.
+ `mv file_backup file_backup_important` to rename a file.
+ `mv */* dire` move all files in each directory into one directory ('dire' here).
+ `rm file` to delete a file. By default, `rm` cannot delete a directory. In order to delete a directory and its conten, use `rm -r foo` where foo is a directory.
+ `find` find files based on arbitrary criteria.
	* `find . -print` prints all file and directory in current directory.
	* `find . -type f -print` only prints files, no directory.
	* `find . -type f -name "*1*"` find files whose names have 1.
	* `find . -type f -name "*1*" -or -name "*2*" -print` names have 1 or 2.
	* `find . -type f -name "*1*" -and -name "*2*" -print` names have 1 and 2.
	* `find . -type f -print | xargs grep Volume` print volume line of each file.
	* `find . -name "*NOTES*" | xargs rm` delete files whose names are NOTES.
	* `find . -type f -exec mv {} {}.txt \;` add all files with .txt at the end.
	* `find . -type f -not -name "*.txt" -exec mv {} {}.txt \;` match all files do not end with .txt and then add .txt to their names.
+ `fdupes -d -r path/to/dire` to find and deal with duplicated files within a directory. You may need to `sudo apt-get install fdupes`.
+ `fdupes -r path/to/dire > dup.txt` to save all results in a txt file.




### Misc
+ `sudo apt-get install --only-upgrade r-base-dev` to upgrade (only) R to the latest version.


More later. 2014-04-14.
