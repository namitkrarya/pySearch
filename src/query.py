import pickle, pprint, copy
from parser import getTerms, getTerms1
from okapi_BM25 import score_BM25

mainIndex = pickle.load(open("/home/nk7/spl_pySearch/index_dump/mainIndex.p", "rb"))
docIndex = pickle.load(open("/home/nk7/spl_pySearch/index_dump/docIndex.p", "rb"))
avdl = sum([docIndex[x][1] for x in docIndex])/len(docIndex)


def function(list1, list2):
    list = []
    for value1 in list1:
        for value2 in list2:
            if (value1[0] == value2[0]):
                pos = [pos for pos in value1[1] if pos in value2[1]]
                if (pos != []):
                    list.append([value1[0], pos])
    return list
def intersectLists(lists):
    if len(lists)==0:
        return []
    lists.sort(key=len)
    ilist = lists[0]
    for l in lists:
        ilist = function(ilist, l)
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


def freeTextQuery(q):
    q=getTerms1(q)
    if q == []:
        return [];
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
        doc_score = 0.0
        l = [[i+1, []] for i in range(0, docIndex[doc][0])]
        for word in q:
            if word in mainIndex:
                n = len(mainIndex[word])
                f = 0
                for d in mainIndex[word]:
                    if doc == d[0]:
                        f = sum([len(line[1]) for line in d[1]])
                        for line in d[1]:
                            l[line[0]-1][1] += line[1]
                doc_score += score_BM25(n, f, len(docIndex), docIndex[doc][1], avdl)
        l = [x for x in l if len(x[1]) != 0]
        l = sorted(l, key=lambda x: len(x[1]), reverse=True)
        doc_list.append([doc, l, doc_score])
    doc_list = sorted(doc_list,key=lambda x: x[-1], reverse=True)
    return ([x[0:2] for x in doc_list])

def phraseQuery(q):
    originalQuery=q
    q=getTerms1(q)
    if len(q)==0:
        return [];
    elif len(q)==1:
        return freeTextQuery(originalQuery)

    phraseDocs=pqDocs(q)
    phraseDocs = sorted(phraseDocs,key=lambda x: sum([len(line[1]) for line in x[1]]), reverse=True)
    doc_list = []
    for doc in phraseDocs:
        m = sorted(doc[1], key=lambda x: len(x[1]), reverse=True)
        doc_list.append([doc[0], m])
    return doc_list

def pqDocs(q):
    phraseDocs=[]
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
