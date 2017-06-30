
# coding: utf-8

# In[ ]:

import pandas as pd
import os
import sys
import re
from pyspark import SparkConf, SparkContext
from operator import add


# In[ ]:

conf = SparkConf().setAppName("Top_Langauges_App").setMaster("local[2]")
sc = SparkContext(conf=conf)


# In[ ]:

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

def occurenceOfLanguages(s):
    try:
        if s in ["JavaScript", "Java", "PHP",                 "Python", "C#", "C++", "Ruby",                 "CSS","Objective-C", "Perl","Scala",                  "Haskell", "MATLAB","Clojure", "Groovy"]:
            return s
    except ValueError:
        return ""
    
def find_word(doc):
    try:
        docWords = doc.split(" ")
        for word in ["JavaScript", "Java", "PHP","Python", "C#", "C++", "Ruby","CSS","Objective-C", "Perl","Scala","Haskell","MATLAB","Clojure","Groovy"]:
            for w in docWords:
                if word.lower() in docWords:
                    return word
    except ValueError:
        return ""
    
# class Complex:
#     def __init__(self,real,imag):
#         self.r=real
#         self.i=imag

# class WikipediaArticle:
#     def __init__(self,doc):
#         self.ti = find_between(doc,'<title>','</title>')
#         self.tex= find_between(doc,'<text>','</text>')


# cn = ['3,4','3,8']
# complex_numbers = [Complex(real.split(',')[0],real.split(',')[1]) for real in cn]


# In[ ]:

wikidata =  sc.textFile('./data/wikipedia.dat')


# In[ ]:

titles = wikidata.map(lambda x: find_between(x,'<title>','</title>'))
text = wikidata.map(lambda x :find_between(x,'<text>','</text>'))
text.persist()


# # Normal Solution 

# In[ ]:

languagePopularity = text.flatMap(lambda x : x.split(' ') )                         .filter(lambda x : occurenceOfLanguages(x)))                         .map(lambda x : (x,1))                         .reduceByKey(lambda x,y : x+y)                         .sortBy((lambda x:x[1]),ascending=False)


# # Solution using inverted Index Way

# In[ ]:

def make_inverted_index(doc):
    try:
        article = find_between(doc,"<text>","</text>")
        article = article.lower()
        docWords = article.split(" ")
        for word in ["JavaScript", "Java", "PHP","Python", "C#", "C++", "Ruby","CSS","Objective-C", "Perl","Scala","Haskell","MATLAB","Clojure","Groovy"]:
            if word.lower() in docWords:
                return (word,article)
    except ValueError:
        return ""

def f(x): return len(x)


# In[ ]:

wikidata.map(make_inverted_index).groupByKey().mapValues(f).sortBy(lambda x :x[1],ascending=False).count()


# In[ ]:

testDat = sc.textFile("./data/test.txt")


# In[ ]:

testDat.map(make_inverted_index).groupByKey().mapValues(f).sortBy(lambda x :x[1],ascending=False).take(1)

