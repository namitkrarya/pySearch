import re
import copy
import pickle, pprint
from functools import reduce
from parser import stopWord, getTerms
from okapi_BM25 import score_BM25

mainIndex = pickle.load(open("/home/nk7/spl_pySearch/index_dump/mainIndex.p", "rb"))
docIndex = pickle.load(open("/home/nk7/spl_pySearch/index_dump/docIndex.p", "rb"))
avdl = sum([docIndex[x] for x in docIndex])/len(docIndex)

def queryInstance():
    q = input("Enter your search query: ")
    if '"' in q:
        pprint.pprint (pq(q))
    else:
        pprint.pprint (ftq(q))

def intersectLists(lists):
    if len(lists)==0:
        return []
    lists.sort(key=len)
    ilist = lists[0]
    for l in lists:
        ilist = [value for value in ilist if value in l]
    return ilist

def getPostings(words):
    return [mainIndex[word] for word in words]

def getDocsFromPostings(postings):
    return [ [x[0] for x in p] for p in postings ]


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
            continue

    li=list(li)
    return rankDocuments(q, li)

def rankDocuments(q, li):
    doc_list = []
    for doc in li:
        doc_score = 0
        for word in q:
            if word in mainIndex:
                n = len(mainIndex[word])
                for d in mainIndex[word]:
                    if doc == d[0]:
                        f = len(d[1])
                doc_score += score_BM25(n, f, len(docIndex), docIndex[doc], avdl)
        doc_list.append([doc, doc_score])
    return sorted(doc_list,key=lambda x: x[1], reverse=True)

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
    phraseDocs = sorted(phraseDocs,key=lambda x: len(x[1]), reverse=True)
    doc_list = []
    for doc in phraseDocs:
        cline = doc[1][1][1]
        mline = doc[1][1][1]
        cfreq = 1
        mfreq = 1
        for occ in doc[1]:
            if occ[1] == cline:
                cfreq+=1
            else:
                if (cfreq > mfreq):
                    mline = cline
                    mfreq = cfreq
                cfreq = 0
                cline = occ[1]
        doc_list.append([doc[0], mline, mfreq])
    return doc_list

def pqDocs(q):
    phraseDocs=[]
    length=len(q)
    for word in q:
        if word not in mainIndex:
            return []

    postings=getPostings(q)
    docs=getDocsFromPostings(postings)
    docs=intersectLists(docs)
    for i in range(len(postings)):
        postings[i]=[x for x in postings[i] if x[0] in docs]
    postings=copy.deepcopy(postings)
    for i in range(len(postings)):
        for j in range(len(postings[i])):
            postings[i][j][1]=[[x[0]-i, x[1]] for x in postings[i][j][1]]
    doc_rank = []
    for j in range(len(postings[0])):
        li=intersectLists( [x[j][1] for x in postings] )
        if li==[]:
            continue
        else:
            doc_rank.append([postings[0][j][0], li])
    return doc_rank

queryInstance()
