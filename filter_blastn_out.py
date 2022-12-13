#file_name:fliter_blastn_out
#function:filter the result of blastn output

import sys
import getopt

def usage():
	print ('''Usage:Python changeID.py [option] [parameter]
	-i/--input_file   blastn_out_outfmt_6
	-o/--output_file   the output_file
	-h/--help          show possible options''')

##########################inputfile#########################
'''
NC_009094.1:115896-116071       KN010225.1      98.276  174     2       1       1       174     33244   33416   1.01e-80        303
NC_009094.1:706574-706815       KN017494.1      99.582  239     1       0       1       239     36359   36121   1.39e-120       436
NC_009094.1:804083-804250       KN010125.1      96.407  167     5       1       1       167     98209   98374   7.51e-72        274
NC_009094.1:978182-978406       KN008280.1      96.380  221     6       2       1       221     112178  112396  2.20e-98        363
NC_009094.1:978585-978741       KN008280.1      98.077  156     3       0       1       156     112577  112732  2.51e-71        272
NC_009094.1:1052900-1053010     JPTV01111771.1  99.091  110     1       0       1       110     16784   16893   2.78e-49        198
NC_009094.1:1139129-1139248     KN007988.1      97.458  118     3       0       1       118     82631   82748   2.38e-50        202
NC_009094.1:1418049-1418188     KN006502.1      95.745  141     3       2       1       139     164289  164428  6.18e-57        224
NC_009094.1:1427393-1427527     KN006502.1      97.744  133     3       0       1       133     173903  174035  1.27e-58        230
'''
##############################################################

opts, args = getopt.getopt(sys.argv[1:], "hi:o:",["help","input_file=","output_file="])
for op, value in opts:
	if op == "-i" or op == "--input_file":
		input_file = value
	elif op == "-o" or op == "--output_file":
		output_file = value
	elif op == "-h" or op == "--help":
		usage()
		sys.exit(1)
if len(sys.argv) == 1:
    usage()
    sys.exit(1)

f1=open(input_file)
f2=open(output_file,"w")
score = {}
species_loc = {}
dict3={}
iden={}
for l in f1:
    i = l.strip().split('\t')
    x = i[0].split(':')
    z = x[1].split('-')
    length=int(z[1])-int(z[0])+1
    if i[0] in score:
        if float(i[2]) > 70 and (int(i[3])/float(length))> 0.9:
            dict3[i[0]]+=1
            if float(i[2]) >float(iden[i[0]]):
                iden[i[0]] = float(i[2])
            else:
                pass
            if float(i[-1])> float(score[i[0]]):
                score[i[0]] = i[-1]
                species_loc[i[0]]= i[1]+'\t'+i[8]+'\t'+i[9] 
            else:
                pass
        else:
            pass
    else:
        if (int(i[3])/float(length))> 0.9 and float(i[2]) > 70:
            dict3[i[0]] = 1
            iden[i[0]] = i[2]
            score[i[0]] = i[-1]
            species_loc[i[0]]= i[1]+'\t'+i[8]+'\t'+i[9]
        else:
            pass
for key,value in species_loc.items():
        x=value.split('\t')
        if int(x[1])>int(x[2]):
            f2.write(key+'\t'+x[0]+'\t'+x[2]+'\t'+x[1]+'\t'+str(dict3[key])+'\t'+str(iden[key])+'\n')
        else:
            f2.write(key+'\t'+x[0]+'\t'+x[1]+'\t'+x[2]+'\t'+str(dict3[key])+'\t'+str(iden[key])+'\n')
f1.close()
f2.close()
