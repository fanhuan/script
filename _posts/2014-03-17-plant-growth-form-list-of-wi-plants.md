---
layout: post
title:  Lists of plant growth forms of Wisconsin plants
categories: [notes]
tags: [research, plants]
---

When I analyze the vegetation data, there is a good chance that I want to split plants into different growth forms, e.g. trees, shrubs. However, I do not have a list of them to do the match in R. I searched online and did not find any list available for analysis. The only thing I found is from the University of Wisconsin - Steve point' s herbarium [website](http://wisplants.uwsp.edu/VascularPlants.html). They have an Identification guides. But when I click on, say, Trees link, they do not have a txt file ready to download, and a txt file table is all what I want!

As a result, I decide to create the txt table according to their website, with the help of [Sublime text](http://www.sublimetext.com/3). Here is the procedure:

1. Open the website, right click, choose `view page source`.
2. Copy the page source into Sublime text, then we can see the species names are wrapped by `SpCode=` and `</A>`.
3. In sublime text, `Ctrl+I`, turn on regular expression search (`Alt+R`), type `SpCode=.+</A`, then press `Alt+Enter`. All matches were selected! Cool! Then copy `Ctrl+C` all of them into a new file (`Ctrl+N`) in Sublime text! 
4. Not done yet. In the new file, `Ctrl+I`, then type `SpCo.+>` first, then press `Alt+Enter`, then press `Delete`. We are half way there, we search `</A`, `Alt+Enter`, then press `Delete`. Awesome! We got the list of that page!
5. Repeat this for each page... Fortunately, they are not too many for trees and shrubs!

I put the list of [tree](http://daijiang.name/pdf/tree.txt), [shrub](http://daijiang.name/pdf/shrub.txt), [vine](http://daijiang.name/pdf/vine.txt), [fern/fern allies](http://daijiang.name/pdf/fern_fern_allies.txt), and [graminoids](http://daijiang.name/pdf/graminoids.txt) online. Downlaod them if you need.

For each species, if you just want the genus and sp, not including the subsp/var info. You can read them in R and then using regular expression to extract them. Or you can do this in Sublime text. Here is my way doing in R:

{% highlight r%}
library(stringr)
tree=read.table("data/tree.txt", sep="\n", stringsAsFactors=F, quote="")$V1
tree=unlist(str_extract_all(tree, "^[A-Za-z]+\\s{1,1}X?\\s?[a-z]+"))
tree=unique(tree)
{% endhighlight %}

In the regular expression part, `^` means at the begining of the string; `[A-Za-z]` means any letters; `+` means more than one times; `\\s` means any space, `{1,1}` means exactly one time; `?` means one time or not present. If you do this in Sublime text, replace `\\s` with `\s`.

I hope this will be helpful if you are doing community ecological analysis.
