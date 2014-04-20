---
layout: post
title:  Git setup and using under Ubuntu
categories: [notes]
tags: [Git, computer]
---
>This post will be update over time along with my git learning.

##Set up
In Ubuntu, it is super easy to install and set up Git. Bascially, just follow the online [reference](http://git-scm.com/docs).

	sudo apt-get install git
	git config --global user.name "daijiang"
	git config --global user.email "daijianglee@gmail.com"
	git config --global color.ui auto
	git config --global core.editor subl # set default editor

That's it! You can check all of your config information by `git config --list`. If you want to know how to use a commend of git, simply using `man git-commend`, e.g. `man git-add`, `man git-pull`.

##Basic steps

####Initialization
Then I want to create a directory named as "github" and clone my repositories into this directory. If your repository is private, then git will ask you for username and password.

	mkdir github
	cd github
	git clone URL
	# git clone URL path/to/
	cd newProject

If I already have a directory and want to version control that one, `cd` to the directory:
	
	git init
	git add *.txt # to track all txt files
	git commit -m 'initial project version'

####Track files
After then, if you modified a file, you can use the following code to version control files.

	git status # check the status of the project
	git diff # check what has been changed (file not staged yet)
	git add filename # send file to staged
	git diff --staged # file already staged but not committed
	git commit -m 'message' 
	git commit -a # all files, and you can skip the stage step by doing this

You can also rename files by using `git mv namea nameb`. This is equal to: `mv namea nameb; git rm namea; git add nameb`.

####Untrack files
How about files you do not want to track? If you tracked them before, use `git rm filename` to untrack and delete it. If you want just to untrack it and want to keep it in the working directory, use `git rm --cached filename`. If you do not want track them at the beginning, put their names in the `.gitignore` file in the directory. Here is an example of the `.gitignore` file:

	*.a # ignore all .a files
	!lib.a # except this file
	/a.txt # ignore a.txt file in the root, but not subdir/a.txt
	dire/ # ignore all files in dire directory

####History
`git log`: check history of a project. Here are some common options:

	git log -p # show diff of each commit
	git log -2 # the latest two commits
	git log --graph
	git log --stat # only show number of lines changed
	git log --shortstat
	git log --name-only # or --name-status
	git log --abbrev-commit
	git log --relative-date 
	git log --pretty=oneline # oneline for each commit
	git log --pretty=short # other options: full, fuller
	git log --pretty=format:"%h - %an, %ar : %s"
	git log --since=2.weeks # commits of the latest two weeks
	git log --since='2002-01-16' # or = '2 years 1 day 3 minutes ago'
	git log --pretty=oneline -- dire/ # only check history of dire directory

####Undo actions

	git checkout -- file.name # undo the modification
	
	git reset HEAD filename # unstage file
	
	# undo the latest commit
	git commit -m 'bad commit'
	git add forgotten.file
	got commit --amend # use the staged dire to edit the last commit

