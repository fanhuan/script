---
layout: post
title:  Git setup and using under Ubuntu
categories: [notes]
tags: [Git, computer]
---
>This post will be update over time along with my git learning.

In Ubuntu, it is super easy to install and set up Git. Bascially, just follow the online [reference](http://git-scm.com/docs).

	sudo apt-get install git
	git config --global user.name "daijiang"
	git config --global user.email "daijianglee@gmail.com"
	git config --global color.ui auto

That's it!

Then I want to create a directory named as "github" and clone my repositories into this directory. If your repository is private, then git will ask you for username and password.

	mkdir github
	cd github
	git clone URL
	cd newProject