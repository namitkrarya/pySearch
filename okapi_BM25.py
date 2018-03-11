from math import log

k1 = 1.2
b = 0.75

def score_BM25(n, f, N, dl, avdl):
    K = compute_K(dl, avdl)
    first = log((N  + 0.5)/(n + 0.5))
    second = ((k1 + 1) * f) / (K + f)
    return first * second

def compute_K(dl, avdl):
	return k1 * ((1-b) + b * (float(dl)/float(avdl)) )
