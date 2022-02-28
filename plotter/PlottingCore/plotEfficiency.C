/* L1T Analysis plotting script
 * module: Efficiency plotter
 * Author: George Karathanasis georgios.karathanasis@cern.ch
 *
 */

#include <sstream>
#include <string>
#include <algorithm>
#include <iterator>
#include <boost/algorithm/string.hpp>
#include "plot_tool.h"
#include "TLatex.h"
#include "../ExtFunctions.h"



int plotEfficiency(TString path, TString name, TString mca, std::string plots, TString tree){

 //read data
 TChain * cc=new TChain(tree);
 std::ifstream inmca(path+"/"+mca);

 std::string ntuple;
 if (inmca.is_open()){
   while (std::getline(inmca, ntuple)){
      if (ntuple=="") continue;
      cc->Add(TString(ntuple));
   }
 }

 gStyle->SetOptStat(0);
 std::string line;

 cout<<"Running on "<<cc->GetEntries()<<" evts "<<endl;

 //plot containers
 std::ifstream infile(plots);

 //single thread output
 TFile * fout=new TFile(path+"/"+name+".root","RECREATE");
 ofstream tout;
 tout.open(path+"/_"+name+".txt");

 //create numerator/denominator
 while (std::getline(infile, line)){
   vector<string> tokens;
   boost::split(tokens,line,boost::is_any_of(":"));
       
   //skip empty lines
   if (tokens.size()==1) continue;
   //pass lines starting with #
   if (tokens[0]=="#") continue;
   
   // protection
   if (tokens.size()<9) {
      cout<<"ERROR requested plot: "<<tokens[0]<<" less options that mandatory- SKIPPING "<<endl;
      continue;
   }

   // initialize cuts
   if (tokens[2]=="None") tokens[2]="1>0";
   if (tokens[3]=="None") tokens[3]="1>0";

   cout<<"plotting... "<<tokens[0]<<" histo "<<endl;
   cout<<tokens[6]<<endl;
   //create efficiencies
   TH1F *temp_den=gethisto(cc,tokens[1],tokens[2],"hden<>"+tokens[0],std::stoi(tokens[5]),std::stof(tokens[6]),std::stof(tokens[7]));
   TH1F *temp_num=gethisto(cc,tokens[1],tokens[2]+" && "+tokens[3],"hnum<>"+tokens[0],std::stoi(tokens[5]),std::stof(tokens[6]),std::stof(tokens[7]));
   
   
   TString titleX(tokens[4]);
   temp_num->GetXaxis()->SetTitle(titleX);
   temp_den->GetXaxis()->SetTitle(titleX);

   std::string options=tokens[0]+":"+tokens[8]+":";
       // save optional arguments
   for(unsigned int itoken=9; itoken<tokens.size(); ++itoken){
      if (options=="")
        options=tokens[itoken];
      else
        options+=";"+tokens[itoken];
      if (tokens[itoken]=="Over"){
        AddOverFlow(temp_den);
        AddOverFlow(temp_num);     
      }
      if (tokens[itoken]=="Under"){
        AddUnderFlow(temp_den);
        AddUnderFlow(temp_num);
      }
   }
   options+="\n";
   temp_den->Write();
   temp_num->Write();
   tout<<options<<"\n";

 }
 fout->Close();
 tout.close();

 return 0;
 }
