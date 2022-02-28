def transform( heff, kwds):

   for kwd in kwds:
     value = kwd.split("=")
     if value[0]=="LineColor":
        heff.SetLineColor(float(value[1]))
     if value[0]=="LineWidth":
        heff.SetLineWidth(float(value[1]))
     if value[0]=="XLabelSize":
        heff.GetXaxis().SetTitleSize(float(value[1]));
     if value[0]=="YLabelSize":
        heff.GetYaxis().SetTitleSize(float(value[1]));
     if value[0]=="YTitle":
        heff.GetYaxis().SetTitle(value[1]);
     if value[0]=="YMinMax":
        heff.GetYaxis().SetRangeUser(float(value[1]),float(value[2]));
     if value[0]=="Cumulative":
        heff_clone = heff.Clone()
        for i in range(heff.GetNbinsX()):
          heff.SetBinContent(i, heff_clone.Integral(i,heff.GetNbinsX()) )
     if value[0]=="InverseCumulative":
        heff_clone = heff.Clone()
        for i in range(heff.GetNbinsX()):
          heff.SetBinContent(i, heff_clone.Integral(0,i) )
     if value[0]=="Rate":
        heff_clone = heff.Clone()
        for i in range(heff.GetNbinsX()):
          heff.SetBinContent(i, heff_clone.Integral(i,heff.GetNbinsX())/heff_clone.Integral(0,heff.GetNbinsX())*int(value[1])*11246 )
   return heff

def legPos( options):
  default= (0.75,0.7,0.95,0.9)
  newpos=0
  for option in options:
    if not "LegPos" in option :
       continue;
    pos = (option.split("=") )[1]
    if pos =="BL":
      newpos=(0.15,0.15,0.3,0.3)
    elif pos  =="BR":
      newpos=(0.7,0.15,0.95,0.3) 
    elif pos =="TL":
      newpos= (0.1,0.7,0.3,0.9)
    elif pos  =="TR":
      newpos= (0.7,0.7,0.9,0.9)

  if newpos ==0:
     return default; 
  else:
     return newpos

def legName( options,default):
  name=default
  for option in options:
    if "LegName" in option:
      name = (option.split("="))[1]
  return name
    

def AddOverflow(h1):
  nx=h1.GetNbinsX()
  value=h1.GetBinContent(nx)+ h1.GetBinContent(nx+1);
  h1.SetBinContent(nx,value);
  return h1

def defalut_canvas(c1):
  c1.SetBorderSize(0)
  c1.SetTopMargin(0.08)
  c1.SetLeftMargin(0.12)
  c1.SetRightMargin(0.04)
  c1.SetBottomMargin(0.12)

def default_plot(histo,xaxis="",yaxis=""):
  if xaxis!="": histo.GetXaxis().SetTitle(xaxis)
  if yaxis!="": histo.GetYaxis().SetTitle(yaxis)
  histo.SetLineWidth(2)
  #histo.SetMarkerStyle(20)
  #histo.SetMarkerSize(1.0)
  histo.GetXaxis().SetTitleSize(0.08) #0.06
  histo.GetYaxis().SetTitleSize(0.07) #0.06
  histo.GetXaxis().SetTitleFont(42)
  histo.GetYaxis().SetTitleFont(42)
  histo.GetXaxis().SetTitleOffset(0.7)
  histo.GetYaxis().SetTitleOffset(0.8)
  histo.GetXaxis().SetLabelOffset(0.007)
  histo.GetYaxis().SetLabelOffset(0.007)
  histo.GetYaxis().SetLabelSize(0.040)
  histo.GetXaxis().SetLabelSize(0.045)
  return histo

