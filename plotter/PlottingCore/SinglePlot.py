from histo_tool import *
from ROOT import *
from cms_lumi import CMS_lumi
import os

def SinglePlot(threaded_roots,workdir,outputDir):
   
  merge="hadd -f "+workdir+"/hsum.root "
  for root in threaded_roots:
    merge+=" "+workdir+"/"+root
  os.system(merge)
  froot = TFile(workdir+'/hsum.root')
  yld = open(outputDir+"/Yields.txt","w")
  yld.write("HistoName        Total Yields(intgr)\n")
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
      h1= froot.Get(histName)
      if "Over" in plot_options:
        h1=AddOverflow(h1)
      yld.write(histName+"  "+str(h1.Integral(0,h1.GetNbinsX()+1))+"\n")
      h1=default_plot(h1)
      h1.SetTitle("")
      h1.SetLineWidth(3)
      c1 = TCanvas( canvasName,canvasName, 1000,700)
      defalut_canvas(c1)
      hstack= THStack("hs","")
      h1=transform(h1,plot_options)
      if "LogX" in plot_options: c1.SetLogx()
      if "LogY" in plot_options: c1.SetLogy()
      if "Norm" in plot_options and h1.Integral()>0:
         h1.Scale(1.0/h1.Integral())
      hstack.Add(h1)
      x1,y1,x2,y2= legPos(plot_options)
      leg = TLegend(x1,y1,x2,y2)
      leg.AddEntry(h1,legName(plot_options,histName))
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
        h2=froot.Get(histName2)
        if "Over" in plot_options2:
           h2= AddOverflow(h2)
        yld.write(histName2+"  "+str(h2.Integral())+"\n")
        h2=default_plot(h2)
        h2.SetLineWidth(3)
        h2.SetLineColor(jline-iline)
        h2.SetMarkerColor(jline-iline)
        hstack.Add(h2)
        if "Norm" in plot_options2 and h2.Integral()>0:
           h2.Scale(1.0/h2.Integral())
        h2=transform(h2,plot_options2)
        leg.AddEntry(h2,legName(plot_options2,histName2))
      if "PlotLine" in plot_options:
          hstack.Draw("nostack,hist")
      else:
          hstack.Draw("nostack,e1p")
      hstack.GetXaxis().SetTitle(h1.GetXaxis().GetTitle())
      hstack.GetYaxis().SetTitle(h1.GetYaxis().GetTitle())
      hstack.GetXaxis().SetTitleSize(0.08)
      hstack.GetYaxis().SetTitleSize(0.07)
      hstack.GetXaxis().SetTitleOffset(0.7)
      hstack.GetYaxis().SetTitleOffset(0.85)
      leg.SetLineColor(0)
      if multhisto: leg.Draw("sames")
      CMS_lumi(c1, 4,  0 , aLittleExtra=0.07)
      c1.SaveAs(outputDir+"/"+canvasName+".png");
      c1.SaveAs(outputDir+"/"+canvasName+".pdf");
  yld.close()
