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
    final = []
    if '"' in q:
        final = (pq(q))
    else:
        final = (ftq(q))
    for rank, hit in enumerate(final, 1):
        print (str(rank), "-", hit[0], "at line", hit[1], ",", hit[2], "time(s).")

def function(list1, list2):
    list = []
    for value1 in list1:
        for value2 in list2:
            if (value1[0] == value2[0]):
                list.append([value1[0], [pos for pos in value1[1] if pos in value2[1]]])
    return list
def intersectLists(lists):
    if len(lists)==0:
        return []
    # pprint.pprint(lists)
    lists.sort(key=len)
    ilist = lists[0]
    for l in lists:
        ilist = function(ilist, l)
    # pprint.pprint(ilist)
    return ilist

def intersectList(lists):
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
        l = []
        for word in q:
            if word in mainIndex:
                n = len(mainIndex[word])
                for d in mainIndex[word]:
                    f = 0
                    if doc == d[0]:
                        f = sum([len(line[1]) for line in d[1]])
                        for line in d[1]:
                            flag = 0
                            for line2 in l:
                                if line[0] == line2[0]:
                                    line2[1] += len(line[1])
                                    flag = 1
                            if (flag == 0):
                                l.append([line[0], len(line[1])])
                        # f = len(d[1])
                doc_score += score_BM25(n, f, len(docIndex), docIndex[doc], avdl)
        l = sorted(l, key=lambda x: x[1], reverse=True)
        doc_list.append([doc, l[0][0], l[0][1], doc_score])
    doc_list = sorted(doc_list,key=lambda x: x[3], reverse=True)
    return ([x[0:3] for x in doc_list])

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
    # phraseDocs = sorted(phraseDocs,key=lambda x: len(x[1]), reverse=True)
    phraseDocs = sorted(phraseDocs,key=lambda x: sum([len(line[1]) for line in x[1]]), reverse=True)
    doc_list = []
    for doc in phraseDocs:
        m = sorted(doc[1], key=lambda x: len(x[1]), reverse=True)[0]
        doc_list.append([doc[0], m[0], len(m[1])])
    return doc_list

def pqDocs(q):
    phraseDocs=[]
    length=len(q)
    for word in q:
        if word not in mainIndex:
            return []

    postings=getPostings(q)
    docs=getDocsFromPostings(postings)
    docs=intersectList(docs)
    # print(docs)
    for i in range(len(postings)):
        postings[i]=[x for x in postings[i] if x[0] in docs]
    postings=copy.deepcopy(postings)
    # pprint.pprint(postings)
    for i in range(len(postings)):
        for j in range(len(postings[i])):
            postings[i][j][1]=[[x[0], [y-i for y in x[1]]] for x in postings[i][j][1]]
    # pprint.pprint(postings)
    doc_rank = []
    for j in range(len(postings[0])):
        li=intersectLists( [x[j][1] for x in postings] )
        if li==[]:
            continue
        else:
            doc_rank.append([postings[0][j][0], li])
    return doc_rank

queryInstance()
