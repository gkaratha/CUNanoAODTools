import os

samples="HiggsZMET_files.txt"
fltr=None

with open(samples,'r') as txt:
  lines=txt.readlines()
  for line in lines:
    sample=line.split(":")
    if len(sample)!=2:
       continue
    if (fltr != None) and (fltr not in sample[0]):
       continue
    print "name",sample[0],"sample",sample[1]
    os.system("python crab_cfg.py --name "+sample[0]+" --sample "+sample[1])
