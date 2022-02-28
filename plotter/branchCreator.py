import os, subprocess
from optparse import OptionParser
import multiprocessing as mp
from ROOT import *
import time;
import sys


def f(x):
  args = x.split(";")
  print x
  name, mca_fl, branches, tree_name=args[0],args[1],args[2],args[3],args[4]
  
  froot = TFile(mca_fl,"update")
  tree = froot.Get(tree_name) 
  for branch in branches:
    branch_name,branch_size, branch_var = branch.split(":")
    values = array('f',[0])
    tree.Branch(branch_name, branch_var,branch_name+"["+branch_size+"]/F")
    for ievt in range(tree.GetEntries()):
      tree.GetEntry(ievt)
      
  os.system(  "root -l -b -q 'PlottingCore/"+args[0]+"(\""+args[1]+qt+args[2]+qt+args[3]+qt+args[4]+qt+args[5]+"\")'"   )
  print "core",(args[2].split("_"))[1],"done"





if __name__ == "__main__":
    # availiable plotting options
    parser = OptionParser()

    parser.add_option("-b","--branchesTxtFile", dest="branchfile",   default="branches.txt", type="string", help="txt with selected plots and cuts")
    parser.add_option("-i","--inputData" ,dest="inputData",  default="mca.txt", type="string", help="txt with root files to run on. By default running on mca.txt")
    parser.add_option("-c","--copyRootBeforeUpdate",dest="copyRootBeforeUpdate",  default=False,action='store_true', help="if the outputDir exists, this rewrites it (previous deleted)")
    (options, args) = parser.parse_args()


    
    clean_mca=[]
    with open(options.inputData,"r") as inf:
      lines=inf.readlines()
      for ln in lines:
        if ":" in ln:
           clean_ln=ln.split(":")[1]
        else:
           clean_ln=ln
  
      clean_mca.append(clean_ln)

    clean_mca_fls=[]
    for mca in clean_mca:
      if "*" in mca:
         mca=mca.split("*")[0]
         for (dirpath, dirnames, filenames) in walk(mca):
           for filename in filenames:
             clean_mca_fls.append(mca+filename)
      else: clean_mca_fls.append(mca)
   
    ncores=mp.cpu_count()
    if nlines<mp.cpu_count(): ncores=nlines
    jobs=[]
    for i, mca_fl in enumerate(clean_mca_fls):
       temp=str('file_%d' % i)+";"+mca_fl+";"+options.branchfile+";"+options.tree
       chunk_names.append(str('/file_%d.root  ' % i))
       jobs.append(temp)


    p = mp.Pool(ncores)
    p.map(f,jobs)




