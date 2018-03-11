import sys
import re
# from porterStemmer import PorterStemmer
# from collections import defaultdict
import copy
import pickle
from functools import reduce

stopwordsFile = "/home/nk7/spl_pySearch/stopwords.dat"
mainIndex = pickle.load(open("/home/nk7/spl_pySearch/dict.p", "rb"))
# print (mainIndex)
q = input("Enter your search query :")

def intersectLists(lists):
    if len(lists)==0:
        return []
    #start intersecting from the smaller list
    lists.sort(key=len)
    return list(reduce(lambda x,y: set(x)&set(y),lists))


def stopWord(stopwordsFile):
    f=open(stopwordsFile, 'r')
    stopwords=[line.rstrip() for line in f]
    sw=dict.fromkeys(stopwords)
    f.close()
    return sw

def getTerms(line):
    line=line.lower()
    # print("\n" + line)
    line=re.sub(r'[^a-z0-9 ]',' ',line) #put spaces instead of non-alphanumeric characters
    # line=re.sub(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*",' ', line)
    # print("\n" + line)
    line=line.split()
    # print (line)
    sw = stopWord(stopwordsFile)
    line=[x for x in line if x not in sw]  #eliminate the stopwords
    # line=[ porter.stem(word, 0, len(word)-1) for word in line]
    return line

def getPostings(words):
    #all terms in the list are guaranteed to be in the index
    return [mainIndex[word] for word in words]


def getDocsFromPostings(postings):
    #no empty list in postings
    return [ [x[0] for x in p] for p in postings ]

def queryType(q):
    if '"' in q:
        return pq(q)
    else:
        return ftq(q)

def ftq(q):
    q=getTerms(q)
    if len(q)==0:
        print ('')
        return

    li=set()
    for word in q:
        if word in mainIndex:
            postings=mainIndex[word]
            docs=[ x[0] for x in postings]
            li=li.union(set(docs))
        else:
            #term not in index
            continue

    li=list(li)
    return li
    # rankDocuments(q, li)

def pq(q):
    originalQuery=q
    q=getTerms(q)
    if len(q)==0:
        print ('')
        return
    elif len(q)==1:
        ftq(originalQuery)
        return

    phraseDocs=pqDocs(q)
    return phraseDocs
    # rankDocuments(q, phraseDocs)

def pqDocs(q):
    phraseDocs=[]
    length=len(q)
    #first find matching docs
    for word in q:
        if word not in mainIndex:
            #if a term doesn't appear in the index
            #there can't be any document maching it
            return []

    postings=getPostings(q)    #all the terms in q are in the index
    docs=getDocsFromPostings(postings)
    #docs are the documents that contain every term in the query
    docs=intersectLists(docs)
    #postings are the postings list of the terms in the documents docs only
    for i in range(len(postings)):
        postings[i]=[x for x in postings[i] if x[0] in docs]

    #check whether the term ordering in the docs is like in the phrase query

    #subtract i from the ith terms location in the docs
    postings=copy.deepcopy(postings)    #this is important since we are going to modify the postings list

    for i in range(len(postings)):
        for j in range(len(postings[i])):
            postings[i][j][1]=[x-i for x in postings[i][j][1][0]]

    #intersect the locations
    result=[]
    for i in range(len(postings[0])):
        li=intersectLists( [x[i][1] for x in postings] )
        if li==[]:
            continue
        else:
            result.append(postings[0][i][0])    #append the docid to the result

    return result

print(queryType(q))
