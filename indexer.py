import os, sys, re
import io, fileinput, string
# from numpy import *
import pickle
import os.path
import pprint
stopwordsFile = "/home/nk7/spl_pySearch/stopwords.dat"
# def stopWord(stopwordsFile)
f=open(stopwordsFile, 'r')
stopwords=[line.rstrip() for line in f]
sw=dict.fromkeys(stopwords)
f.close()

def getTerms(line):
    line=line.lower()
    # print("\n" + line)
    line=re.sub(r'[^a-z0-9 ]',' ',line) #put spaces instead of non-alphanumeric characters
    # line=re.sub(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*",' ', line)
    # print("\n" + line)
    line=line.split()
    # print (line)
    line=[x for x in line if x not in sw]  #eliminate the stopwords
    # line=[ porter.stem(word, 0, len(word)-1) for word in line]
    return line



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
            # print (fileIndex)
            for word in fileIndex:
                if word in mainIndex:
                    mainIndex[word].append(fileIndex[word])
                else:
                    mainIndex[word] = [fileIndex[word]]
        docIndex[filename] = count
        # print(mainIndex)
# pprint.pprint(mainIndex)
# pprint.pprint(docIndex)
pickle.dump(mainIndex, open("/home/nk7/spl_pySearch/dict.p", "wb"))
pickle.dump(docIndex, open("/home/nk7/spl_pySearch/docdict.p", "wb"))

        # print (f)
        # count=0
        # split = f.split()
        # for word in split:
        #     word = re.sub(r'[^\w\s]','',word)
        #     word = word.lower()
        #     flag = 0
        #     c=-1
        #     for i in l:
        #         c+=1
        #         if ( word == i[0] ):
        #             flag = 1
        #             i[1]+=1
        #     if flag == 0:
        #         l.append([word, 1])
        #         count+=1
        # l.sort()
        # # l = sorted(l,key=lambda x: x[0])
        # print (l)
        # # print (count)
        # x = range(count*count)
        # x = reshape(x, (count,count))
        # for row in range(0,count):
        #     for col in range(0, count):
        #         x[row][col] = 0
        #
        # prev = ""
        # co = 0
        # for word in split:
        #     word = re.sub(r'[^\w\s]','',word)
        #     word = word.lower()
        #     if co == 0:
        #         co+=1
        #         prev = word
        #         continue
        #     w = 0
        #     p = 0
        #     q = 0
        #     for i in l:
        #         if( i[0] == word ):
        #             w = q
        #             break
        #         else:
        #             q+=1
        #     q = 0
        #     for i in l:
        #         if( i[0] == prev ):
        #             p = q
        #             break
        #         else:
        #             q+=1
        #     x[p][w]+=1
        #     prev = word
        # # print (x)
        # save_path = "/home/namit/spl/indexes"
        # completeName1 = os.path.join(save_path, filename[:-4]+"1.p")
        # completeName2 = os.path.join(save_path, filename[:-4]+"2.p")
        # pickle.dump(l, open(completeName1, "wb"))
        # pickle.dump(x, open(completeName2, "wb"))
