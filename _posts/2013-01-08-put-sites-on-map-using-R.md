---
layout: post
title:  Put your sites on map using R
categories: [Tips]
tags: [R]
---
Last summer, I resampled about 34 used-be Pine Barrens sites.  Here is the distribution map:

{% highlight r %}
data=read.csv("lat.csv")
library(ggplot2);library(ggmap)
p=ggmap(get_map(c(-89.725,44.9), zoom = 7, source = "google", maptype = "terrain")) #get the WI map
cbPalette <- c("blue", "red")
p+geom_point(data=data,aes(long,lat,colour = type, shape=type),alpha=0.8,size=4)+theme(legend.position="top")+scale_colour_manual(values=cbPalette)
{% endhighlight %}

![ggmap-site](http://i.imgur.com/nYFKywM.png)

Or, another version:

{% highlight r %}
library(maps)
ggplot(data, aes(long, lat))+borders("county","wisconsin", colour="grey70")+geom_point(colour="red",alpha= 0.5)
{% endhighlight %}

![map-site](http://i.imgur.com/n7nuFKq.png)

