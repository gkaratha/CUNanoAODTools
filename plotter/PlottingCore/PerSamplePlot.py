from histo_tool import *
from ROOT import *
from cms_lumi import CMS_lumi
import os

def PerSamplePlot(sample_names,sample_roots,sample_normalization,sample_category,sample_colors,workdir,outputDir):
  fout = TFile(outputDir+"/histos.root","RECREATE")
  yld = open(outputDir+"/Yields.txt","w")
  yld.write("HistoName    |    Total Yields(intgr)\n")
  with open(workdir+"/_histo_core_0.txt","r") as res:
    lines=[]
    lines=res.readlines()
    for iline,line in enumerate(lines):
      if line=="\n": continue
      wline=(line.rstrip()).split(":")
      histName=wline[0]
      canvasName=wline[1]
      plot_options=(wline[2]).split(";")
      c1 = TCanvas( canvasName,canvasName, 700,700)
      defalut_canvas(c1)
      if "LogX" in plot_options: c1.SetLogx()
      if "LogY" in plot_options: c1.SetLogy()
      x1,y1,x2,y2= legPos(plot_options)
      leg = TLegend(x1,y1,x2,y2)
      finternal = TFile(workdir+"/temp.root","RECREATE")
      final_colors=[]
      names=[]
      categories=[]
      sample_names_sorted=[]
      ichunk=0
      while ichunk<len(sample_names):
        sample_nm,sample_norm  = sample_names[ichunk],sample_normalization[ichunk]
        if ichunk>len(sample_roots) or ichunk==len(sample_roots):
           sample_root=sample_roots[ichunk % len(sample_roots)]
        else:
           sample_root=sample_roots[ichunk]
        sample_cat = sample_category[ichunk]
        froot = TFile(workdir+"/"+sample_root)
        h1 = (froot.Get(histName)).Clone(histName+str(ichunk))
        real_stats=h1.Integral(0,h1.GetNbinsX()+1)
        if sample_norm!=None:
           h1.Scale(float(sample_norm))
        inext_chunk=ichunk+1
      
        while inext_chunk<len(sample_names) and sample_nm==sample_names[inext_chunk]:
           if inext_chunk>len(sample_roots) or inext_chunk==len(sample_roots):
             sample_root2=sample_roots[inext_chunk % len(sample_roots)]
           else:
             sample_root2=sample_roots[inext_chunk]
           froot2 = TFile(workdir+"/"+sample_root2)
           h2 = (froot2.Get(histName)).Clone(histName+str(inext_chunk))
           if sample_normalization[inext_chunk]!=None:
              h2.Scale(float(sample_normalization[inext_chunk]))
           h1.Add(h2)
           ichunk=inext_chunk
           inext_chunk+=1
        h1.SetName(histName+str(ichunk))
        names.append(histName+str(ichunk))
        if sample_colors[ichunk]!="None":
          final_colors.append(int(sample_colors[ichunk]))
        else:
          final_colors.append(ichunk)
        categories.append(sample_cat)
        sample_names_sorted.append(sample_nm)
        if "Over" in plot_options: h1=AddOverflow(h1)
        yld.write(histName+"  "+sample_nm+" real stats "+str(real_stats)+"  "+str(sample_norm)+"\n")
        h1=default_plot(h1)
        h1.SetLineWidth(3)
        h1=transform(h1,plot_options)
        if "Norm" in plot_options:
           h1.Scale(1.0/h1.Integral())
        fout.cd()
        h1.Write()
        finternal.cd()
        h1.Write()
        ichunk+=1

      finternal.Close()
      finternal_read= TFile(workdir+"/temp.root","READ")
      hstack= THStack("hs","")
      for iplot,name in enumerate(names):
        htemp  = finternal_read.Get(name)
        xaxe= str(htemp.GetXaxis().GetTitle())
        yaxe= str(htemp.GetYaxis().GetTitle())
        hstack.SetTitle(";"+xaxe+";"+yaxe) 
        htemp.SetLineColor(final_colors[iplot])
        htemp.SetFillColor(final_colors[iplot])
        #htemp.SetFillStyle(3001)
        leg.AddEntry(htemp,legName(plot_options,sample_names_sorted[iplot]))
        if categories[iplot]=="Bkg":
          hstack.Add(htemp);
      hstack.Draw("HIST")      
      for opt in plot_options:
         if "YMinMax" in opt:
           minmax=opt.split("=")
           hstack.SetMinimum(float(minmax[1]))
           hstack.SetMaximum(float(minmax[2]))

      for iplot,name in enumerate(names):
        if categories[iplot]=="Sgn":
           htemp=finternal_read.Get(name)
           htemp.SetFillColor(0);
           if iplot>0:
             htemp.Draw("sames")
           else:
             htemp.Draw("HIST")
        if categories[iplot]=="Data":
           htemp=finternal_read.Get(name)
           htemp.SetFillColor(0);
           if iplot>0:
             htemp.Draw("sames PE0")
           else:
             htemp.Draw("PE0")
          
        
      CMS_lumi(c1, 4,  0 , aLittleExtra=0.07)
      if len(sample_names)>1:
        leg.Draw("sames")
      c1.SaveAs(outputDir+"/"+canvasName+".png");
      c1.SaveAs(outputDir+"/"+canvasName+".pdf");
  yld.close()
  fout.Close()
