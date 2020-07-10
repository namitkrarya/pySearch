import os, gc
import pickle, pprint
from nltk import PorterStemmer
from parser import getTerms
from timeit import default_timer as timer


stopIndex = pickle.load(open("/home/nk7/spl_pySearch/index_dump/stopIndex.p", "rb"))

mainIndex = {}
docIndex = {}
# stopIndex = {}
start = timer()
gc.disable()
for filename in os.listdir("/home/nk7/spl_pySearch/corpus/split/"):
    if filename.endswith(".txt"):
        fileIndex = {}
        wordCount = -1
        lineCount = 0
        with open("corpus/split/" + filename) as f:
            for num, line in enumerate(f, 1):
                lineCount += 1
                line = getTerms(line)
                lineIndex = {}
                for position, word in enumerate(line, 1):
                    wordCount += 1
                    if word not in stopIndex:
                        word = PorterStemmer().stem(word)
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

# stopWordsFile=open("/home/nk7/spl_pySearch/stopwords.txt", 'r')
# stopWords=[line[:-1] for line in stopWordsFile]
# stopIndex=dict.fromkeys(stopWords)
# stopWordsFile.close()

end = timer()
print(end - start)
gc.enable()
# pprint.pprint(mainIndex)
# pprint.pprint(docIndex)
# pprint.pprint(stopIndex)
pickle.dump(mainIndex, open("/home/nk7/spl_pySearch/index_dump/mainIndex.p", "wb"))
pickle.dump(docIndex, open("/home/nk7/spl_pySearch/index_dump/docIndex.p", "wb"))
pickle.dump(stopIndex, open("/home/nk7/spl_pySearch/index_dump/stopIndex.p", "wb"))
