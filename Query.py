# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 20:14:09 2015

@author: user
"""

import urllib2
from xml.dom import minidom

import  AmazonWebServices 

#Login details
AWS_ACCESS_KEY_ID = 'AKIAJCVAZC3LFAMDJNAA'
AWS_SECRET_ACCESS_KEY = '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'  
AWS_AFFILIATE_ID = "35mmpe-20"


url = AmazonWebServices.amazonSearchByKeywords('yoga_mat',AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_AFFILIATE_ID)

feed = urllib2.urlopen(url)
doc = minidom.parse(feed)

#Get all doc elements matching a given tag
brands = doc.getElementsByTagName("Studio")
price = doc.getElementsByTagName("Amount")

data = zip(brands,price)

for awsNode1, awsNode2 in data:
    awsNode1 =  awsNode1.childNodes[5].childNodes[9].childNodes[22].nodeValue
    awsNode2 = awsNode2.childNodes[5].childNodes[9].childNodes[14].childNodes[1].nodeValue
    print "%s:%s"%(awsNode1,awsNode2)