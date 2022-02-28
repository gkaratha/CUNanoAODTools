from histo_tool import *
from ROOT import *
from cms_lumi import CMS_lumi
from math import sqrt
import os

def PerSampleEfficiency(sample_names,sample_roots,workdir,outputDir):

  fout = TFile(workdir+'/heff.root',"RECREATE")
  yld = open(outputDir+"/Efficiencies.txt","w")
  yld.write("HistoName  |    Total Efficiency(including under/overflow)\n")
  with open(workdir+"/_histo_0.txt","r") as res:
    lines=[]
    lines=res.readlines()
    
    for iline,line in enumerate(lines):
      if line=="\n": continue
      wline=(line.rstrip()).split(":")
      histName=wline[0]
      canvasName=wline[1]
      plot_options=(wline[2]).split(";")
      c1 = TCanvas( canvasName,canvasName, 1000,700)
      defalut_canvas(c1)
      if "LogX" in plot_options: c1.SetLogx()
      if "LogY" in plot_options: c1.SetLogy()
      x1,y1,x2,y2= legPos(plot_options)
      leg = TLegend(x1,y1,x2,y2)
      finternal = TFile(workdir+"/temp.root","RECREATE")
      names=[]
      ichunk=-1;
      for sample_nm, sample in zip(sample_names,sample_roots):
        ichunk+=1
        froot = TFile(workdir+"/"+sample)
        hnum= (froot.Get("hnum<>"+histName)).Clone("hnum<>"+histName+str(ichunk))
        hden= (froot.Get("hden<>"+histName)).Clone("hden<>"+histName+str(ichunk))
        nnum = float(hnum.Integral(0,hnum.GetNbinsX()+1))
        nden= float(hden.Integral(0,hden.GetNbinsX()+1))
        yld.write(histName+"  "+sample_nm+"   |   "+str(nnum/nden)+" +/- "+str(sqrt( nnum/(nden**2)+(nnum**2)/(nden**3)))+"\n")
        heff = TGraphAsymmErrors(hnum,hden)
        heff.SetName(histName+str(ichunk))
        heff.SetTitle(";"+hnum.GetXaxis().GetTitle()+";")
        names.append(str(histName+str(ichunk)))
        heff=default_plot(heff)
        heff.SetLineWidth(3)
        heff=transform(heff,plot_options)
        fout.cd()
        heff.Write()
        finternal.cd()
        heff.Write()
      
      finternal.Close()
      finternal_read= TFile(workdir+"/temp.root","READ")
     
      for iplot,name in enumerate(names):
        htemp=finternal_read.Get(name)
        htemp.SetLineColor(1+iplot)
        htemp.SetMarkerColor(1+iplot)
        leg.AddEntry(htemp,legName(plot_options,sample_names[iplot]))
        if iplot==0: htemp.Draw("A P")
        else: htemp.Draw("P sames")

      CMS_lumi(c1, 4,  0 , aLittleExtra=0.07)
      leg.SetLineColor(0);
      leg.Draw("sames")
      c1.SaveAs(outputDir+"/"+canvasName+".png");
      c1.SaveAs(outputDir+"/"+canvasName+".pdf");
  yld.close()
  fout.Close()
