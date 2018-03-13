import os, sys, re
import pickle, pprint
from parser import stopWord, getTerms
from timeit import default_timer as timer
# mainIndex = pickle.load(open("/home/nk7/spl_pySearch/dict.p", "rb"))
mainIndex = {}
docIndex = {}
start = timer()
for filename in os.listdir("/home/nk7/spl_pySearch/corpus/split/"):
    if filename.endswith(".txt"):
        fileIndex = {}
        wordCount = 0
        lineCount = 0
        with open("corpus/split/" + filename) as f:
            for num, line in enumerate(f, 1):
                lineCount += 1
                line = getTerms(line)
                lineIndex = {}
                for position, word in enumerate(line, 1):
                    wordCount += 1
                    if word in lineIndex:
                        lineIndex[word][1].append(position)
                    else:
                        lineIndex[word] = [num, [position]]
                # pprint.pprint(lineIndex)
                for word in lineIndex:
                    if word in fileIndex:
                        fileIndex[word][1].append(lineIndex[word])
                    else:
                        fileIndex[word] = [filename, [lineIndex[word]]]
            # pprint.pprint(fileIndex)
            for word in fileIndex:
                if word in mainIndex:
                    mainIndex[word].append(fileIndex[word])
                else:
                    mainIndex[word] = [fileIndex[word]]
        docIndex[filename] = [lineCount, wordCount]

# pprint.pprint(mainIndex)
# pprint.pprint(docIndex)
end = timer()
print(end - start)
pickle.dump(mainIndex, open("/home/nk7/spl_pySearch/index_dump/mainIndex.p", "wb"))
pickle.dump(docIndex, open("/home/nk7/spl_pySearch/index_dump/docIndex.p", "wb"))
