# -*- coding: utf-8 -*-
"""
CS481 Fall 2019 Homework 2
Burrows-Wheeler Transform source code file
Created on Thu Oct  24 11:00:07 2019
@author: İlayda Beyreli 201801130
"""

import sys
import time
from itertools import chain

def readfa(file_name):
    # Reading .FA files into lists
    with open(file_name, "r") as fin:
        data =fin.read().splitlines()
    data = list(chain.from_iterable(data[1:])) 
    return data

def readbwt(file_name):
    with open(file_name, "r") as fin:
        data =fin.read().splitlines()
    data = list(chain.from_iterable(data)) 
    return data


def readfm(file_name):
    with open(file_name, "r") as fin:
        data =fin.read().splitlines()
    s = data.index("SA")
    r = data.index("Rnk")
    o = data.index("Occ")
    Rank = [int(x) for x in data[r+1].split() if x.isdigit()]
    sa = [int(x) for x in data[s+1].split() if x.isdigit()]
    Occ = []
    for i in range(o+1,len(data)):
        line = [int(s) for s in data[i].split() if s.isdigit()]
        Occ.append(line)
    Cnt = Occ[-1]
    return Occ,Cnt,Rank,sa

def writebwt(file_name,data):
    with open(file_name, "w+") as fout:
        for item in data:
            fout.write(item)
    return True

def writefm(file_name,alphabet,Occ,Rank,sa):
    with open(file_name, "w+") as fout:
        fout.write("SA\n")
        for item in sa:
            fout.write(str(item)+" ")
        fout.write("\n")
    with open(file_name, "a+") as fout:
        for item in alphabet:
            fout.write(str(item)+" ")
        fout.write("\n")
    with open(file_name, "a+") as fout:
        fout.write("Rnk\n")
        for item in Rank:
            fout.write(str(item)+" ")
        fout.write("\n")
    with open(file_name, "a+") as fout:
        fout.write("Occ")
        for l in Occ:
            fout.write("\n")
            for item in l:
                fout.write(str(item)+" ")                
    return True

def suffix_array(ori):
    x = ori.copy()
    # Add 1 to rank due to index transformation
    x =  [rank+1 for suffix, rank in sorted((x[i:], i) for i in range(len(x)))]
    return x

# Burrows-Wheeler Transform
def bwtf(data,alphabet):
    """Apply Burrows-Wheeler transform to input string."""
    sa =  suffix_array(data)
    spec  = '#'
    # Adding special char to the array
    data.append(spec)
    # Generating all rotations
    m = []
    Rank = [0 for i in range(len(alphabet))] 
    for i in range(0, len(data)):
        m.append(data)
        # Keep track of rank
        ind = alphabet.index(data[0])   
        temp = data[1:].copy()
        temp.append(data[0])
        data = temp
    m.sort()
    Cnt = [0 for i in range(len(alphabet))] 
    out = []
    temp =[]
    Occ = []
    for j in range(0,len(m)):
        item =m[j][-1]
        out.append(item)
        temp.append(m[j][0])
        # Fill Occ table
        ind = alphabet.index(item)
        Cnt[ind] = Cnt[ind]+1
        Occ.append(Cnt.copy())
    for i in range(len(alphabet)):
        j = alphabet[i]
        ind = temp.index(j)
        Rank[i] = ind 
    return out, Occ, Cnt, Rank, sa
   
# Inverse Burrows-Wheeler Transform
def ibwtf(data):
    """Apply inverse Burrows-Wheeler transform."""
    spec  = '#'
    out = ["" for i in range(len(data))]
    for i in range(len(data)):
        out = sorted(data[i] + out[i] for i in range(len(data)))
    out = [i for i in out if i[-1]==spec][0]
    out = [i for i in out]  
    return out[:-1]

# Search With Burrows Wheeler Transform & Ferragini-Marzini Index
def bwfm_search(bwt,pattern,alphabet,Occ,Rank,sa):
    t = time.time()
    l = pattern[-1]
    frm = int(Rank[alphabet.index(l)] )# Next block starts from "frm"
    to = int(Occ[-1][alphabet.index(l)]) # Next block finishes at "to"
    # print(frm,to)
    for i in range(len(pattern)-2,-1,-1): #Starting from the right most position
        l = pattern[i]
        if l in bwt[frm:(to+1)]:                
            frm = Rank[alphabet.index(l)]+max(Occ[frm][alphabet.index(l)]-1,0)
            to = Rank[alphabet.index(l)]+Occ[to][alphabet.index(l)]-1
            print(frm,to)
            if i == 0:
                print("Pattern P found in T ", to+1-frm, "times at positions:")
                for j in range (to+1-frm):
                    print("Pos ",j+1,": ",str(sa[frm+j-1]))
                print("Search completed in %.2f seconds." % (time.time()-t))
        else:
            print("Pattern P NOT found in T.")
            print("Search completed in %.2f seconds." % (time.time()-t))
            return False
    return True

## Main Function
try:
    mode =  sys.argv[1] # "--search"
    text_file =  sys.argv[2] #"hw2example.fa"
except IndexError:
    print("Insufficient number of arguments!")

spec = '#'
text = readfa(text_file)
alphabet=list(set(text))
alphabet.append(spec)
alphabet.sort()


if mode == "--index":
    bwt, Occ, _, Rank,sa = bwtf(text, alphabet)
    done = writebwt(text_file+'.bwt',bwt)
    done = writefm(text_file+'.fm',alphabet,Occ,Rank,sa)
    print("Indexing has been done. -> "+text_file+'.bwt'+" , "+text_file+'.fm')
elif mode == "--search":
    try:
        pattern_file =  sys.argv[4] #  "hw2pattern.fa" #
        pattern = readfa(pattern_file)
        fm_file = text_file+".fm"
        bwt_file = text_file+".bwt"
    except IndexError:
        print("Insufficient number of arguments! Expected: 4 Passed:",len(sys.argv)-1)
    try:
        Occ,Cnt,Rank,sa = readfm(fm_file)
        bwt = readbwt(bwt_file)
        done = bwfm_search(bwt,pattern,alphabet,Occ,Rank,sa)
    except OSError:
        print(".bwt and/or .fm file not found in the working directory!\nTry --index command first.")
elif mode == "--inverse":
    bwt_file = text_file+".bwt"
    bwt = readbwt(bwt_file)
    ori = ibwtf(bwt)
    done = writebwt(text_file+'.ibwt',ori)
    print("The data has been recovered. -> "+text_file+'.ibwt')
else:
    try:    
        raise KeyError
    except KeyError:
        print("Invalid command!\nTry either --index, --search or --inverse.")