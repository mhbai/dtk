#!/usr/bin/python
#-*- encoding: UTF-8 -*-

from collections import defaultdict
import math,json

# 將各別的詞頻表合併成單一詞頻表
def MergeTopicFreq(TopicFreq):
	T=defaultdict(int)
	for category, freqDict in TopicFreq.iteritems():
		for word, freq in freqDict.iteritems():
			T[word]+=freq
	return T


def NormTopicFreq(TopicFreq):
	NTopicFreq={}
	for topic, freqDict in TopicFreq.iteritems():
		# 計算區塊總詞頻
		total=sum(freqDict.values())
		# 計算百萬次詞頻 
		NFreqDict={}
		for word, freq in freqDict.iteritems():
			NFreqDict[word]=float(freq*1000000)/total
		NTopicFreq[topic]=NFreqDict
	return NTopicFreq


def TopicFreq2FreqDist(TopicFreq):
	freqDistribution=defaultdict(list)
	for category, freqDict in TopicFreq.iteritems():
		for word, freq in freqDict.iteritems():
			freqDistribution[word].append(freq)
	return freqDistribution

def Entropy(TopicFreq):
	FreqDist=TopicFreq2FreqDist(TopicFreq)
	entropyT={}
	for word, dist in FreqDist.iteritems():
		totalcnt = sum(dist)
		pL=[float(x)/totalcnt for x in dist]
		entropyT[word]=-sum([p*math.log(p,2) for p in pL])
	return entropyT


def DC(TopicFreq):
	# Number of Topics
	N=len(TopicFreq.keys())
	FreqDist=TopicFreq2FreqDist(TopicFreq)
	dcT={}
	for word, dist in FreqDist.iteritems():
		smr=(float(sum([math.sqrt(x) for x in dist]))/N)**2
		mean=float(sum(dist))/N
		dcT[word]=smr/mean
	return dcT

# 計算標準差
def SD(TopicFreq):
	N=len(TopicFreq.keys())
	FreqDist=TopicFreq2FreqDist(TopicFreq)
	sdT={}
	for word, dist in FreqDist.iteritems():
		mean=float(sum(dist))/N
		sdT[word]=math.sqrt(float(sum([(x-mean)**2 for x in dist]))/(N-1))
	return sdT

# 計算變異數
def VC(TopicFreq):
	N=len(TopicFreq.keys())
	FreqDist=TopicFreq2FreqDist(TopicFreq)
	vcT={}
	for word, dist in FreqDist.iteritems():
		mean=float(sum(dist))/N
		vcT[word]=math.sqrt(float(sum([(x-mean)**2 for x in dist]))/(N-1))/mean
	return vcT

# 計算 Juilland's D 及 U
def JD(TopicFreq):
	n=len(TopicFreq.keys())
	vcT=VC(TopicFreq)
	jdT={}
	for word, vc in vcT.items():
		jdT[word]=1-(vc/(math.sqrt(n-1)))
	return jdT

def JU(TopicFreq):
	freqT=MergeTopicFreq(TopicFreq)
	n=len(TopicFreq.keys())
	vcT=VC(TopicFreq)
	juT={}
	for word, vc in vcT.items():
		juT[word]=(1-(vc/(math.sqrt(n-1))))*freqT[word]
	return juT

# 計算 chi-square
def CS(TopicFreq):
	freqT=MergeTopicFreq(TopicFreq)
	# 計算每一分割相對於語料庫的百分比
	sT=defaultdict(float)
	total=0
	for category, T in TopicFreq.iteritems():
		for word, freq in T.iteritems():
			total+=freq
			sT[category]+=freq

	for category in sT.keys():
		sT[category]=float(sT[category])/total

	#print "sT",sT
	# 計算每一個詞在每一類別下的期望值
	expT={}
	for category, T in TopicFreq.iteritems():
		expT[category]={}
		for word, freq in T.iteritems():
			expT[category][word]=sT[category]*freqT[word]

	# 計算 chi-square
	csT=defaultdict(float)
	for category, T in TopicFreq.iteritems():
		for word, freq in T.iteritems():
			csT[word]+=float((freq-expT[category][word])**2)/expT[category][word]
	return csT
			
# 計算 Carroll's D2
def CD(TopicFreq):
	n=len(TopicFreq.keys())
	freqT=MergeTopicFreq(TopicFreq)
	FreqDist=TopicFreq2FreqDist(TopicFreq)
	entropyT={}
	for word, dist in FreqDist.iteritems():
		totalcnt = sum(dist)
		entropyT[word]=(math.log(freqT[word],2)-(float(sum([x*math.log(x,2) for x in dist]))/freqT[word]))/math.log(n,2)
	return entropyT

def CU(TopicFreq):
	n=len(TopicFreq.keys())
	freqT=MergeTopicFreq(TopicFreq)
	FreqDist=TopicFreq2FreqDist(TopicFreq)
	entropyT={}
	for word, dist in FreqDist.iteritems():
		totalcnt = sum(dist)
		D=(math.log(freqT[word],2)-(float(sum([x*math.log(x,2) for x in dist]))/freqT[word]))/math.log(n,2)
		entropyT[word]=freqT[word]*D+(1-D)*freqT[word]/n
	return entropyT

# 計算 IDF
def IDF(TopicFreq):
	n=len(TopicFreq.keys())
	FreqDist=TopicFreq2FreqDist(TopicFreq)
	idfT={}
	for word, dist in FreqDist.iteritems():
		idfT[word]=math.log(float(n)/len(dist),2)
	return idfT

# 計算 Lyne's D3
def LD(TopicFreq):
	freqT=MergeTopicFreq(TopicFreq)
	csT=CS(TopicFreq)
	ldT={}
	for word, cs in csT.items():
		ldT[word]=1-(cs/(4*freqT[word]))
	return ldT

# 計算 Rosengrens Adjusted Freq
def RAF(TopicFreq):
	freqT=MergeTopicFreq(TopicFreq)
	dcT=DC(TopicFreq)
	RAF={}
	for word, dc in dcT.items():
		RAF[word]=dc*freqT[word]
	return RAF
	


if __name__=="__main__":

	T={
	    'f1':{'b': 2, 'a': 1, 'e': 1, 'i': 1, 'k': 1, 'm': 1, 'n': 1, 'p': 1, 'u': 1}, 
		'f2':{'a': 2, 'b': 2, 'e': 1, 'n': 1, 'q': 1, 's': 1, 't': 1, 'w': 1}, 
		'f3':{'a': 3, 'b': 2, 'c': 1, 'e': 1, 'g': 1, 's': 1, 't': 1}, 
		'f4':{'a': 4, 'b': 2, 'e': 1, 'g': 1, 'h': 1, 't': 1}, 
		'f5':{'a': 5, 'b': 2, 'h': 1, 'e': 1, 'x': 1}
	}

	L=DC(T)
	#L=Entropy(T)
	#L=SD(T)
	#L=VC(T)
	#L=CS(T)
	#L=JD(T)
	#L=CD(T)
	#L=IDF(T)
	#L=LD(T)
	#L=LD(T)
	#L=JU(T)
	#L=RAF(T)
	L=CU(T)
	print json.dumps(L,indent=4)
