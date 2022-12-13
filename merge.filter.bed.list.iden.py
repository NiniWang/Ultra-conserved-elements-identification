#!/usr/bin/env python3.4
import sys
import getopt
def usage():
    print('''Useage: python script.py [option] [parameter]
    -l/--list            input the filter bed list
    -o/--results             the  results
    -h/--help                show possible options''')
#######################
opts, args = getopt.getopt(sys.argv[1:], "hl:o:",["help","list=","results="])
for op, value in opts:
    if op == "-l" or op == "--list":
        list = value
    elif op == "-o" or op == "--results":
        results = value
    elif op == "-h" or op == "--help":
        usage()
        sys.exit(1)
if len(sys.argv) < 3:
    usage()
    sys.exit(1)

f1=open(list)
f2=open(results,'w')
title='seq'
wy=''
name=[]
dict={}
for file in f1:
    file=file.strip()
    a=file.split('/')
    b=a[-1].split('.')
    c=b[0]
    name.append(c)
    wy+=c+'\t'
    locals()[c]={}
    file=open(file)
    for reads in file:
        reads=reads.split()
        dict[reads[0]]=''
        locals()[c][reads[0]]=reads[5]
f2.write(title+'\t'+wy+'\n')
for key,value in dict.items():
    x=''
    for i in name:
        x+='\t'+locals()[i].get(key,'0')
    f2.write(key+x+'\n')
f1.close()
f2.close()
