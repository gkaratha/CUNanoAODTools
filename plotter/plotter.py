import os, subprocess 
from optparse import OptionParser
import multiprocessing as mp
from ROOT import *
import time;
import sys
import getpass


sys.path.insert(1, 'PlottingCore/')
from SingleEfficiency import SingleEfficiency
from SinglePlot import SinglePlot
from PerSampleEfficiency import PerSampleEfficiency
from PerSamplePlot import PerSamplePlot

def handle_cache(path):
  path=path.split("*")[0]
  sample=path.split("/")[-4]
  print "copy",path,"locally"
  local_path="/tmp/"+getpass.getuser()+"/"
  if os.path.exists(local_path+sample):
     print sample,"exists"
     return local_path+sample+"/*.root"
  else:
     os.system("mkdir "+local_path+sample)
     os.system("cp "+path+"*.root"+"  "+local_path+sample)
     print sample,"copied" 
     return local_path+sample+"/*.root"
  #os.syste 
    


def get_nano_evts(path):
  cc=TChain("Runs")
  
  cc.Add(path.split()[0]+"*.root")  
  #cc.SetMakeClass(1)
  #cc.SetBranchStatus("*",1)
  var=0
#  cc.SetBranchStatus("Runs.genEventCount",1)
  #cc.SetBranchAddress("genEventCount",var)
  nevts=0
  #print path.split()[0]
  for c in cc:
#    for tree in c:
      #print getattr(tree,"genEventCount")
      try:
        nevts+=c.genEventCount
      except AttributeError:
        try:
          nevts+=c.genEventCount_
        except AttributeError:
          try:
            nevts+=c.genEventCount_TChiWZ
          except AttributeError:
            print "Error no genEvtcount found"
            c.Print()
            exit()
            nevts+=-1
 
  return nevts

def f(x):
  args = x.split(";")
  #print x
  qt= "\",\""
  os.system(  "root -l -b -q 'PlottingCore/"+args[0]+"(\""+args[1]+qt+args[2]+qt+args[3]+qt+args[4]+qt+args[5]+qt+args[6]+"\")'"   )
  print "core",(args[2].split("_"))[2],"done"



if __name__ == "__main__":
    # availiable plotting options
    parser = OptionParser()

    parser.add_option("-p","--plotsTxtFile", dest="plotfile",   default="plots.txt", type="string", help="txt with selected plots and cuts")
    parser.add_option("-s","--script", dest="script", default="Plots", type="choice",choices= ['Efficiency','Plots'], help="plotter type choices: EfficiencyPlots or SimplePlots")
    parser.add_option("-i","--inputData" ,dest="inputData",  default="mca.txt", type="string", help="txt with root files to run on. By default running on mca.txt")
    parser.add_option("-o","--outputDir",dest="outputDir",  default="Plots_Date", type="string", help="folder name to save plots. Default=Plots_Date")
    parser.add_option("-n","--ncore",dest="ncore",type="int",  default=-1, help="number of cores to use. -1 uses all")
    parser.add_option("--tree",dest="tree",  default="Events", type="string", help="tree name. Default Events")
    parser.add_option("-l","--lumi",dest="lumi",  default=140.8, type="float", help="Lumi for MC normalization. default 140.8")
    parser.add_option("-v","--verbosity",dest="verb",  default=0, type="float", help="verbosity level:0 (no printouts), 1(only from plotter), 2(from all parts). default 0 (2 still in devolopment)")
    parser.add_option("--cache-samples",dest="cachesmp",  default=False,action="store_true", help="transfers samples in temporary local file. will be bit slower the 1st time it runs due to cp  but faster in subsequent. sample path must have the usual crab structure ie .../crab_Nano_WJetsToLNuHT100to200/210716_174314/0000/")
    parser.add_option("--ftree",dest="ftree",  default="None",type="str", help="extra friend tree path (relative to main sample path ie /main_sample_path_process/friend/)")
    parser.add_option("-f",dest="force_rewrite",  default=False,action="store_true", help="if output file exits it rewrites without asking")   
    (options, args) = parser.parse_args()

     #  create output folder to save plots
    if options.outputDir=="Plots_Date":
      localtime = time.asctime( time.localtime(time.time()) )
      options.outputDir = "Plots_{0}".format(localtime.replace(" ","_"))
      options.outputDir = options.outputDir.replace(":","_")
      os.system(  "mkdir -p "+options.outputDir )
      print "plots will be saved at "+options.outputDir
      
    else:
      print "plots will be saved at "+options.outputDir
      if os.path.exists(options.outputDir):    
         print "Directory "+options.outputDir+" exists"
         if not options.force_rewrite:
            os.system("rm -r -I "+options.outputDir)
         else:
            os.system("rm -r "+options.outputDir)
         if os.path.exists(options.outputDir):
            print "exiting - need output directory"
            exit()
         print "directory "+options.outputDir+" emptied"
      os.makedirs(options.outputDir)

         
    os.system("cp "+options.plotfile+" "+options.outputDir)
    os.system("cp "+options.inputData+" "+options.outputDir)

    script="plotEfficiency.C"
    if options.script=="Plots":
       script="plotSimple.C"
      
    #create tmp folder inside the output directory - will be erased at the end
    workdir =  options.outputDir+"/temp"
    os.makedirs(workdir)
    
    nlines=0
    with open(options.inputData,"r") as inf:
      lines=inf.readlines()
      for line in lines:
        if line.startswith("#"): continue;
        if not line.strip(): continue;
        if line=="\n": continue;
        if not "/" in line: continue;
        nlines+=1


    ncores=mp.cpu_count()
    if nlines<mp.cpu_count(): ncores=nlines
    if options.ncore!=-1: ncores=options.ncore
    files = [open(workdir+'/mca_core_%d.txt' % i, 'w') for i in range(nlines)]

    print "job distributed in",ncores,"cores"

    legs=[]
    xsec=[]
    category=[]
    total_mc_evts=[]
    colors=[]
    plot_type=1
    iline=0
    for line in lines:
      if line.startswith("#"): continue;
      if not line.strip(): continue;
      if line=="\n": continue;
      if not "/" in line: continue;
      if ":" in line:
        if options.verb>0:
          print "mca type2 detected line",iline,":",line
        words= line.split(":")
        category.append(words[0])
        legs.append(words[1])
        xsec.append(words[2])
        if options.cachesmp:
          words[3] = handle_cache(words[3])
        files[iline].write(words[3]+"\n")
        colors.append(words[4])
        if len(words)==6:
           total_mc_evts.append(float(words[5]))
        else:
           if words[0]!="Data":
             print"here", words[1],words[3],get_nano_evts(words[3])
             total_mc_evts.append(get_nano_evts(words[3]))
           else:
             total_mc_evts.append(1.)
        plot_type=2
      else:
         if options.verb>0:
            print "mca type1 detected line",iline,":",line
         files[iline].write(line) 
      iline+=1
      
    for fi in files:
      fi.close() 

    for xs in range(len(xsec)):
      if options.verb>0:
         print "xsec=",xsec[xs],"lumi=",options.lumi,"mc events=",total_mc_evts[xs]
      if category[xs] != "Data" and float(xsec[xs])!=0:
         xsec[xs]=float(xsec[xs])*options.lumi/(1.0*total_mc_evts[xs])
      else:
         xsec[xs]=None 

    chunk_names=[]
    jobs=[]
    for i in range(0,nlines):
       temp=script+";"+workdir+";"+str('histo_core_%d' % i)+";"+str('mca_core_%d.txt' % i)+";"+options.plotfile+";"+options.tree+";"+options.ftree
       chunk_names.append(str('/histo_core_%d.root  ' % i))
       jobs.append(temp)


    p = mp.Pool(ncores)
    p.map(f,jobs)

    print "stage 2... "
    gROOT.SetBatch(True)
    
    if options.script=="Plots":
      if plot_type==1:
        if options.verb>0:
          print "running PlottingCore/SinglePlot"
        SinglePlot(chunk_names,workdir,options.outputDir)   
      else:
        if options.verb>0:
          print "running PlottingCore/PerSamplePlot"
        print xsec
        PerSamplePlot(legs,chunk_names,xsec,category,colors,workdir,options.outputDir)
    else:
      print "uknown plot option (efficiency not supported in v1). exiting.."
      exit()
    
    os.system( "mv "+workdir+"/hsum.root   "+options.outputDir+"/histos.root" )
    if options.verb==0:
      print "clean up"
      os.system( "rm -r "+workdir )
    print "finished !"
  
