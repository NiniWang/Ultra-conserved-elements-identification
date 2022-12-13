#!/usr/bin/env python3.4
import sys
import getopt
def usage():
    print('''Useage: python script.py [option] [parameter]
    -l/--list            input the full pathway list of filtered blast result
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
title='Candidate UCEs'
wy=''
name=[]
CUCEs={}
for file in f1:
    file=file.strip()
    a=file.split('/')
    b=a[-1].split('.')
    species=b[0]
    name.append(species)
    wy+=species+'\t'
    locals()[species]={}
    file=open(file)
    for element in file:
        element=element.split()
        CUCEs[element[0]]=''
        locals()[species][element[0]]=element[5]
f2.write(title+'\t'+wy+'\n')
for key,value in CUCEs.items():
    x=''
    for i in name:
        x+='\t'+locals()[i].get(key,'0')
    f2.write(key+'\t'+x+'\n')
f1.close()
f2.close()
