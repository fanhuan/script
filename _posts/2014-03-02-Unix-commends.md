---
layout: post
title:  Unix commends
categories: [notes]
tags: [computer]
---
I tried a couple of times to switch from Windows to Ubuntu, but failed, mainly because that I do not have enough time and patient
to teach myself. 

Last week, I heared [a great class](http://kbroman.github.io/Tools4RR/) is giving this semester at UW-Madison. After look at
its website, I felt that it may be a good time to pick the Ubuntu up, again. And try to learn the commend line. 

Here is a list of the most basic commends in Unix from what I learned today.

+ `cd Documents` to change to the Documents sub-folder.
+ `cd ..` to change to the parent directory.
+ `cd` to change to your home directory.
+ `pwd` to print the path of the current working directory.
+ `ln -s` creates symbolic links. `ln -s Documents Docs`.
+ `ls -l` reveal where a symlink points. e.g. Docs -> Documents in the above example.
+ `cat day1.R` have a look at a text file in within the current directory, e.g. day1.R.
+ `less day1.R` only read a few part of day1.R. Press `q` to quit the reading.
+ `man command` to check what a command does. e.g. `man ls`. Press `q` to quit.
+ `command > file` dump the standard output into a file. e.g. `pwd > pwd.txt`, then you can use `cat pwd.txt` to have a look at the file.
+  `Ctrl+d` will send "end of file' and will often terminate the shell.
+  `ls /bin/*sh` will list all shells available.
+  `df -h` to get the disk of file system used, `-h` means return human readable numbers, e.g. 100Mb. 100Gb.
+  `du -hs /path/to/directory` get the total size of the directory. `du` means disk usage, `-h` as above, `-s` means summary.
+  `env` to view the current values of environment variables.





More later.
