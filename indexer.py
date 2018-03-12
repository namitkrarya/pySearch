import os, sys, re
import pickle, pprint
from parser import stopWord, getTerms

# mainIndex = pickle.load(open("/home/nk7/spl_pySearch/dict.p", "rb"))
mainIndex = {}
docIndex = {}
for filename in os.listdir("/home/nk7/spl_pySearch/corpus/"):
    if filename.endswith(".txt"):
        fileIndex = {}
        count = 0
        with open("corpus/" + filename) as f:
            for num, line in enumerate(f, 1):
                line = getTerms(line)
                for word in line:
                    count += 1
                    if word in fileIndex:
                        fileIndex[word][1].append([count, num])
                    else:
                        fileIndex[word] = [filename, [[count, num]]]
            pprint.pprint(fileIndex)
            for word in fileIndex:
                if word in mainIndex:
                    mainIndex[word].append(fileIndex[word])
                else:
                    mainIndex[word] = [fileIndex[word]]
        docIndex[filename] = count

pprint.pprint(mainIndex)
pprint.pprint(docIndex)
pickle.dump(mainIndex, open("/home/nk7/spl_pySearch/index_dump/mainIndex.p", "wb"))
pickle.dump(docIndex, open("/home/nk7/spl_pySearch/index_dump/docIndex.p", "wb"))
