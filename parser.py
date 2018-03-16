import re, pickle
from nltk import PorterStemmer

stopIndex = pickle.load(open("/home/nk7/spl_pySearch/index_dump/stopIndex.p", "rb"))

def getTerms(line):
    line=line.lower()
    line=re.sub(r'[^a-z0-9 ]','',line)
    line=line.split()
    return line

def getTerms1(line):
    line=line.lower()
    line=re.sub(r'[^a-z0-9 ]','',line)
    line=line.split()
    line=[x for x in line if x not in stopIndex]
    line=[PorterStemmer().stem(word) for word in line]
    return line
