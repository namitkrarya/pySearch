from query import phraseQuery, freeTextQuery
from parser import getTerms

PATH = "/home/nk7/spl_pySearch/corpus/split/"
FILES = 10
LINES = 1

def display_line(fileName, lineNum, ql):
    wordpos = []
    for i in range(ql):
        wordpos += [x+i for x in lineNum[1]]
    with open(PATH + fileName) as doc:
        for i, line in enumerate(doc, 1):
            if lineNum[0] == i:
                line = line.split()
                print ("Line", i, ":")
                for num, word in enumerate(line, 1):
                    if num in wordpos:
                        print ('\x1b[2;30;43m' + word + '\x1b[0m', end=" ")
                    else:
                        print (word, end=" ")

def print_matches(matchedDocs, ql):
    if matchedDocs != []:
        for rank in range(min(FILES, len(matchedDocs))):
            print ('\x1b[1;32;40m' , str(rank+1),".", matchedDocs[rank][0], "at line(s)", [x[0] for x in matchedDocs[rank][1]] , '\x1b[0m')
            for line in range(min(LINES, len(matchedDocs[rank][1]))):
                display_line(matchedDocs[rank][0], matchedDocs[rank][1][line], ql)
                print()
            print ("-"*189)


def queryInstance(query):
    matchedDocs = []
    if '"' in query:
        matchedDocs = phraseQuery(query)
        print_matches(matchedDocs, len(getTerms(query)))
    else:
        matchedDocs = freeTextQuery(query)
        print_matches(matchedDocs, 1)

while(1):
    query = input('\x1b[3;34;40m' + "Enter search query: " + '\x1b[0m')
    if query == '':
        break
    else:
        queryInstance(query)
