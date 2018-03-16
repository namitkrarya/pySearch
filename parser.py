import re, pickle
from nltk import PorterStemmer

stopIndex = pickle.load(open("/home/nk7/spl_pySearch/index_dump/stopIndex.p", "rb"))

# def stopWord(stopwordsFile):
#     f=open(stopwordsFile, 'r')
#     stopwords=[line.rstrip() for line in f]
#     sw=dict.fromkeys(stopwords)
#     f.close()
#     return sw

def getTerms(line):
    line=line.lower()
    line=re.sub(r'[^a-z0-9 ]',' ',line)
    line=line.split()
    # sw = stopWord(stopwordsFile)
    line=[x for x in line if x not in stopIndex]
    line=[PorterStemmer().stem(word) for word in line]
    return line
