---
layout: post
title:  Unix shell commends
categories: [notes]
tags: [computer]
---
I tried a couple of times to switch from Windows to Ubuntu, but failed, mainly because that I do not have enough time and patience
to teach myself. 

Last week, I heared [a great class](http://kbroman.github.io/Tools4RR/) is giving this semester at UW-Madison. After look at
its website, I felt that it may be a good time to pick the Ubuntu up, again. And try to learn the commend line. 

Here is a list of the most basic commends in Unix from my learning notes.

## Basic system commends

+ `/` is the root directory if at the beginning.
+ `.` means current directory.
+ `..` means one level up of current directory, i.e. parent directory.
+ `~` is the shortcut of the home directory. e.g. `cd ~`, same effect as `cd`; `~/data` equals with `/home/user/data`
+ `$` the commend line is ready.
+ `#` comments, things after this will be ignored.
+ `cd Documents` to change to the Documents sub-folder.
+ `cd` to change to your home directory.
+ `cd ..` to change to the parent directory.
+ `tab` to autocomplete, e.g. `cd b<tab>` will autocomplete the directory name begin with `b` (if it exits).
+ `pwd` to print the path of the current working directory.
+ `ln -s` creates symbolic links. `ln -s Documents Docs`. Then Docs -> Documents.
+ `ls -l` reveal where a symlink points and permission info. e.g. Docs -> Documents in the above example. `-S` sort files by size, `-F` means flag, add / at the end of directories. `-R` lists the contents of directories recursively.
+ `ls /bin/*a* /bin/*b*` list all files in /bin that contain the letter a or b.
+ `man command` to check what a command does. e.g. `man ls`. Press `q` to quit. `man` use `less` internal, so you can use `/` to search for something.
+ `history` to check all commend used.
+ `!220` to rerun the 220th commend from history
+ `|` is used for piping, i.e. use output of one commend as input of another. e.g. `wc -l file1 file2 | sort | head -1` counts lines of file, then sorts the lines then print the first line of the result.
+ `Ctrl+d` will send "end of file' and will often terminate the shell.
+ `ls /bin/*sh` will list all shells available.
+ `df -h` to get the disk of file system used (short of disk free?), `-h` means return human readable numbers, e.g. 100Mb. 100Gb.
+ `du -hs /path/to/directory` get the total size of the directory. `du` means disk usage, `-h` as above, `-s` means summary.
+ `env` to view the current values of environment variables.
+ `PATH` the environment path of a program. e.g. `echo $PATH` will print a list of places the shell will ONLY look for a program to run.
+ `which` print the location of a program. e.g. `which ls`.
+ `uname -a` print the system information.
+ `lsb_release -a` print Linux standard base distribution-specific information.
+ `finger` to check users inthe system.


## File related commends

+ `command > file` dump the standard output into a file. e.g. `pwd > pwd.txt`, then you can use `cat pwd.txt` to have a look at the file. `>` will create a file if it does not exit or rewrites a file if it already exits. `>>` will append to an exist file instead of rewrite it.
+ `commend < input` e.g. `wc < file1`. This tells the computer that the input of `wc` is `file1`. This actually equals to `wc file1`.
+ `mkdir /tmp/user` will create a new directory named as user. All files in `/tmp` will be deleted after computer shutdown.
+ `rmdir /tmp/user` to remove a directory. If the directory is not empty, this will not work. Instead use `-r` option, which means "recursive", if you are sure that you want to remove all files inside the directory.
+ `cat day1.R` have a look at a text file in within the current directory, e.g. day1.R. You can also use `cat day1.R day2.R` to print two files. `cat day*` will print all files begin with day. You can also use `cat day* > all.R` to save all files into one file.
+ `cat filefolder/*` print the contents of all of the files in the filefolder directory.
+ `wc file1 file2` counts the number of lines (`-l`), words (`-w`) and characters (`-m`) in files.
+ `sort file` to sort a file.
+ `uniq file` to delete replicated *neighbor* lines.
+ `head -5 file` print the first 5 lines of file.
+ `tail -5 file` print the last 5 lines of file.
+ `less day1.R` only read a few part of day1.R. Press `q` to quit the reading, `space` to go forward, `b` to go backward, `g` to go to the begining, `G` to go to the end, `/` to search a word, but only forwardly.
+ `cp file file_backup` copy a file.
+ `mv file_backup /tmp/user` move the file into the /tmp/user directory.
+ `mv file_backup file_backup_important` to rename a file.
+ `mv */* dire` move all files in each directory into one directory ('dire' here).
+ `rm file` to delete a file. By default, `rm` cannot delete a directory. In order to delete a directory and its conten, use `rm -r foo` where foo is a directory.
+ `colrm start end` remove columns of file. A column is a character.
+ `grep` stands for *global/regular expression/print*. It finds lines in a file.
	* `grep -n pattern file` `-n` will number lines found.
	* `man grep` for more options. e.g. `-i` matching case-insensive, `-V` inverts the match.
+ `find` find files based on arbitrary criteria.
	* `find . -print` prints all file and directory in current directory (`.`).
	* `find . -type f -print` only prints files, no directory.
	* `find . -type d -print` only prints directories, not files.
	* `find . -type f -name "*1*"` find files whose names have 1.
	* `find . -type f -name "*1*" -or -name "*2*" -print` names have 1 or 2.
	* `find . -type f -name "*1*" -and -name "*2*" -print` names have 1 and 2.
	* `find . -type f -print | xargs grep Volume` print volume line of each file. `grep Volume $(find . -type f -print)` is another way.
	* `find . -name "*NOTES*" | xargs rm` delete files whose names are NOTES. `rm $(find . -name "*NOTES*" )` is another way.
	* `find . -type f -exec mv {} {}.txt \;` add all files with .txt at the end.
	* `find . -type f -not -name "*.txt" -exec mv {} {}.txt \;` match all files do not end with .txt and then add .txt to their names.
+ `fdupes -d -r path/to/dire` to find and deal with duplicated files within a directory. You may need to `sudo apt-get install fdupes`.
+ `fdupes -r path/to/dire > dup.txt` to save all results in a txt file.


## Loops

	for filename in *.txt
	do 
		# examples:
		echo $filename                   # print file names
		head -3 $filename 
	    head -100 $filename | tail -20   # print 81-100 lines for each file
		echo mv $filename prefix-$filename
		mv $filename prefix-$filename    # rename each file
		bash programname  $filename out-$filename
										 # run programname on each file
	done

If file names have space in some of them, put `$filename` in quote to avoid problems. But the best way is to avoid putting space in any file names. If you are not sure about the commends you are using, put `echo mv $filename prefix-$filename` between `do` and `done` to check it.

##Moving cursor inside bash
+ `^` means `Ctrl` key, e.g. `^A` means `Ctrl+A`.
+ `^A` move to the beginning of a line in the shell.
+ `^E` move to the end of a line.
+ `^C` cancel what you are doing.
+ `^L` clean the screen of your shell.
 

##Shell scripts

Example: put `head -20 file.txt | tail -5` in a file *commend.sh*; put `head $2 $1 | tail $3` in a file *commend2.sh*; put `wc -l $* | sort -n` in a file *commend3.sh*;
+ `shell scripts` a bunch of commends saved in a file.
+ `bash commend.sh` will run the commends saved in file *commend.sh*.
+ `bash commend2.sh filename.txt -20 -5` can specify filenames and lines. `$1` means the first parameter on the commend line, etc.
+ `bash commend3.sh *.txt backup/*.txt` will sort and list all files specified. `$*` means all parameters on the commend line.
+ `bash commend3.sh` will use stdin (i.e input from the commend line) as input.
+ `history | tail -4 | colrm 1 7 > useful.sh` will save your last 4 commends into *useful.sh* so you can recycle them later.

## Remote

+ `scp filename user@server:filenameYouWant` on your local terminal to send local file to remote server. `scp filename user@server:.` if you do not want  to rename the file.youwant
+ `ssh -Y user@server` to connect a remote server.



## Misc

+ `sudo apt-get install --only-upgrade r-base-dev` to upgrade (only) R to the latest version.
+ `echo $GDMSESSION` check the OS info. In my machine, it returns *Lubuntu*.
+ `echo $XDG_CURRENT_DESKTOP` check the desktop window manager. My is *LXDE*.


More later. 2014-04-21.

##Reference

+ [Software carpentry](http://software-carpentry.org/v5/novice/shell/)
+ [Software carpentry UW-Madison](https://github.com/UW-Madison-ACI/boot-camps/blob/2014-01-uwmadison/shell/Readme.md)
