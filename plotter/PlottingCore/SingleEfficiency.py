from histo_tool import *
from ROOT import *
from cms_lumi import CMS_lumi
from math import sqrt
import os

def SingleEfficiency(threaded_roots,workdir,outputDir):

  merge="hadd -f "+workdir+"/hsum.root "
  for root in threaded_roots:
    merge+=" "+workdir+"/"+root
  os.system(merge)
  froot = TFile(workdir+'/hsum.root')
  fout = TFile(workdir+'/heff.root',"RECREATE")
  yld = open(outputDir+"/Efficiencies.txt","w")
  yld.write("HistoName  |    Total Efficiency(including under/overflow)\n")
  with open(workdir+"/_histo_0.txt","r") as res:
    lines=[]
    lines=res.readlines()
    plotted_alrd=[]
    for iline,line in enumerate(lines):
      if line=="\n": continue
      if iline in plotted_alrd:
        continue
      wline=(line.rstrip()).split(":")
      histName=wline[0]
      canvasName=wline[1]
      plot_options=(wline[2]).split(";")
      hnum= froot.Get("hnum<>"+histName)
      hden= froot.Get("hden<>"+histName)
      nnum = float(hnum.Integral(0,hnum.GetNbinsX()+1))
      nden= float(hden.Integral(0,hden.GetNbinsX()+1))
      yld.write(histName+"   |   "+str(nnum/nden)+" +/- "+str(sqrt( nnum/(nden**2)+(nnum**2)/(nden**3)))+"\n")
      heff = TGraphAsymmErrors(hnum,hden)
      heff=default_plot(heff)
      heff.SetLineWidth(3)
      c1 = TCanvas( canvasName,canvasName, 1000,700)
      defalut_canvas(c1)
      heff=transform(heff,plot_options)
      if "LogX" in plot_options: c1.SetLogx()
      if "LogY" in plot_options: c1.SetLogy()
      x1,y1,x2,y2= legPos(plot_options)
      leg = TLegend(x1,y1,x2,y2)
      leg.AddEntry(heff,legName(plot_options,histName))
      heff.SetTitle("")
      heff.Draw("A P")
      heff.Write()
      multhisto=False
      for jline in range(iline+1,len(lines)-1):
        line2=lines[jline]
        if line2=="\n": continue;
        wline2=(line2.rstrip()).split(":")
        canvasName2=wline2[1]
        if canvasName != canvasName2:  break;
        multhisto=True
        plotted_alrd.append(jline);
        histName2=wline2[0]
        plot_options2=wline2[2].split(";")
        hnum2=froot.Get("hnum<>"+histName2)
        hden2=froot.Get("hden<>"+histName2)
        nnum2 = float(hnum2.Integral(0,hnum2.GetNbinsX()+1))
        nden2 = float(hden2.Integral(0,hden2.GetNbinsX()+1))
        yld.write(histName2+"   |   "+str(nnum2/nden2)+" +/- "+str(sqrt( nnum2/(nden2**2)+(nnum2**2)/(nden2**3)))+"\n")
        heff2 = TGraphAsymmErrors(hnum2,hden2)
        
        heff2=default_plot(heff2)
        heff2.SetLineWidth(3)
        heff2.SetLineColor(jline-iline)
        heff2.SetMarkerColor(jline-iline)
        heff2=transform(heff2,plot_options2)
        leg.AddEntry(heff2,legName(plot_options2,histName2))
        heff2.Draw("P sames")
        heff2.Write()
      heff.GetXaxis().SetTitle(hnum.GetXaxis().GetTitle())
      heff.GetYaxis().SetTitle(hnum.GetYaxis().GetTitle())
      leg.SetLineColor(0)
      if multhisto: leg.Draw("sames")
      CMS_lumi(c1, 4,  0 , aLittleExtra=0.07)
      c1.SaveAs(outputDir+"/"+canvasName+".png");
      c1.SaveAs(outputDir+"/"+canvasName+".pdf");
  yld.close()
  fout.Close()
