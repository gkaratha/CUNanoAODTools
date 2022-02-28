#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.LeptonSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.HTSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.JetSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.JetLepCleaner import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenAnalyzer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenIdenticalMothersDiscriminator import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenRecoMatcher import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles


from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

#import argparse
from os import listdir
from os.path import isfile, join
from signal_files import fsignal

#parser = argparse.ArgumentParser(description='run Higgs to ZMET f/w')
#parser.add_argument('--prod',dest='production',default=False,action='store_true',help='an integer for the accumulator')
#parser.add_argument('--run_signal',dest='run_signal',default=True,action='store_false',help='adds specific branches H->ZZ')
#parser.add_argument('-o',dest='outputFolder',default="test_HtoZZ_2MuMET",type=str,help='an integer for the accumulator')

#args = parser.parse_args()
#cfg in txt because crab helper is not perfect (to be mild)
production=False
outputFolder="signalZtoMuE" #used only for non-production
build_GenSignalDecay=True
load_signal_from_file=False
maxEntries=None #deactivate(use all evts): None


fnames=[
#"root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/NANOAOD/02Apr2020-v1/230000/04C09D40-7E66-D148-8C4E-45422D08E6B8.root"
#"root://cms-xrd-global.cern.ch//store/data/Run2018D/DoubleMuon/NANOAOD/02Apr2020-v1/20000/0CD604C2-BBC0-424D-9531-719F10CF1ED4.root"
#Z->lfv
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2520000/786C58A3-19EB-3942-9FE2-8B6936300FC7.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2520000/8350DE73-D6A4-244C-94D5-C0D56CE561A8.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2520000/9A3B097C-6AD6-1C4C-874E-B9650FF4E06B.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2520000/B41038C2-CD7D-D74C-8371-B1D5325BE2DB.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2520000/BC48C659-7BAA-9F41-930D-07714CEC7B4E.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/2358483A-DD44-C749-BA1F-F0B0F0CED3CC.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/24AD115E-89A7-B44A-8534-894A515B026E.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/28A6C455-9F68-7344-8B69-570BC47C033C.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/3F315781-429E-BE4C-8A32-943ED86EEFEC.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/42AECBE2-9D07-5A48-995E-14414B0706E1.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/4A6123BD-6485-9B46-95E1-07CE3684B23E.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/4BC3B454-3346-704B-A0C0-9109558225C2.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/53CA0D9E-66C2-5648-A665-AA0EB26C842F.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/53CA0D9E-66C2-5648-A665-AA0EB26C842F.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/7CEBF4DA-DDED-7743-8E82-3D4F9C3E2319.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/88B3F307-C7FE-4C48-8CD4-D39480253F6D.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/893C4652-B1E1-004F-8913-208C2EA8BDF6.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/95150E39-239F-B243-9821-0D7F527086F8.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/A5A644A7-AA85-684B-9901-B2999AB4A556.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/B9657C52-392B-CC4B-B500-20BEDAD59876.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/C658AD3B-67BF-D341-A536-9C4F7196BCDD.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/E293824A-AD91-B443-AC9A-0F53E3B38F29.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/E7C2A5AB-C0CA-DE43-BCCE-7DA0AAAF48DE.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/EC972535-EF1D-854D-8AB8-52BDB33594C1.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/260000/F1EB906F-2CAC-9542-83EE-190237EEB9E9.root",
"root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/270000/A1023F4D-F3BE-5849-A672-43081EB1F452.root"
#Z->mumu
#"root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/260000/D00124A5-B512-BB47-90D9-1E02BEC9BB94.root",
#"root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/260000/D4A15E3B-B2AF-0747-83DD-6EEAB40A3728.root",
#"root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/260000/FB03DB80-CA59-D249-8B87-899D822BF069.root"
##Z->ee
#"root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv6/ZToEE_NNPDF31_13TeV-powheg_M_50_120/NANOAODSIM/PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/100000/7C1F6146-1573-2D45-AF44-F5CA9A9BD639.root",
#"root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv6/ZToEE_NNPDF31_13TeV-powheg_M_50_120/NANOAODSIM/PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/100000/9D3E63A9-9DE0-1841-9311-000C9B44F5DD.root",
#"root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv6/ZToEE_NNPDF31_13TeV-powheg_M_50_120/NANOAODSIM/PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/100000/8FE26BC0-6724-894D-94C2-3BFB981533C6.root"

]

if load_signal_from_file:
   fnames=fsignal()

# only read the branches in this file - for speed deactivate unescairy stuff
branchsel_in ="keep_and_drop_in.txt"

# only write the branches in this file in ADDITION of what is produce by module
branchsel_out ="keep_and_drop_out.txt"
TriggerCuts=""
#TriggerCuts="HLT_IsoMu24"
#TriggerCuts="(HLT_Mu27_Ele37_CaloIdL_MW || HLT_Mu37_Ele27_CaloIdL_MW || HLT_IsoMu24) && nMuon>0 && nElectron>0"
#TriggerCuts=""
MuonSelection = lambda l : l.pt>10 and l.mediumPromptId==True and abs(l.eta)<2.4 and l.pfRelIso03_all<0.3 and  abs(l.dz)<1.0 and abs(l.dxy)<0.5
#TightMuonSelection = lambda l : l.pt>10 and l.mediumPromptId==True and abs(l.eta)<2.4 and l.pfRelIso03_all<0.3 and  abs(l.dz)<1.0 and abs(l.dxy)<0.5
ElectronSelection = lambda l : l.pt>10 and abs(l.eta)<2.4 and l.pfRelIso03_all<0.3 and abs(l.dz)<1.25 and abs(l.dxy)<0.5  
TauSelection = lambda l : l.pt>5 and abs(l.eta)<2.4 and l.idAntiMu>0
JetSelection = lambda l : l.pt>20.0 and abs(l.eta)<4.7 and l.puId>6

 


modules=[]

'''ZmumuBuilder=GenAnalyzer(
                  decay='23->-13,13',
                  motherName='GenZMuMu',
                  daughterNames=['GenMuon','GenAntiMuon'],
                  variables=['pt','eta','phi','pdgId'],
                  conjugate=False,
                  daughter_antipart=[True,True],
                  skip=False,
                  )
if build_GenSignalDecay: modules.append(ZmumuBuilder)
RecoMuonMatcher=GenRecoMatcher(
                  genParticles=['GenMuon'],
                  recoCollections=['Muon'],
                  maxDR=0.1
                  )
if build_GenSignalDecay: modules.append(RecoMuonMatcher)
RecoAntiMuonMatcher=GenRecoMatcher(
                  genParticles=['GenAntiMuon'],
                  recoCollections=['Muon'],
                  maxDR=0.1
                  )
if build_GenSignalDecay: modules.append(RecoAntiMuonMatcher)'''
'''ZeeBuilder=GenAnalyzer(
                  decay='23->-11,11',
                  motherName='GenZEE',
                  daughterNames=['GenElectron','GenAntiElectron'],
                  variables=['pt','eta','phi','pdgId'],
                  conjugate=False,
                  daughter_antipart=[True,True],
                  skip=False,
                  )
if build_GenSignalDecay: modules.append(ZeeBuilder)
RecoElectronMatcher=GenRecoMatcher(
                  genParticles=['GenElectron'],
                  recoCollections=['Electron'],
                  maxDR=0.1
                  )
if build_GenSignalDecay: modules.append(RecoElectronMatcher)
RecoAntiElectronMatcher=GenRecoMatcher(
                  genParticles=['GenAntiElectron'],
                  recoCollections=['Electron'],
                  maxDR=0.1
                  )
if build_GenSignalDecay: modules.append(RecoAntiElectronMatcher)
'''
ZmueBuilder=GenAnalyzer(
                  decay='23->-13,11',
                  motherName='GenZMuE',
                  daughterNames=['GenMuon','GenElectron'],
                  variables=['pt','eta','phi','pdgId'],
                  conjugate=True,
                  mother_has_antipart=False,
                  daughter_has_antipart=[True,True],
                  skip=False,
                  )
if build_GenSignalDecay: modules.append(ZmueBuilder)
RecoElectronMatcher=GenRecoMatcher(
                  genParticles=['GenElectron'],
                  recoCollections=['Electron'],
                  maxDR=0.1
                  )
if build_GenSignalDecay: modules.append(RecoElectronMatcher)
RecoMuonMatcher=GenRecoMatcher(
                  genParticles=['GenMuon'],
                  recoCollections=['Muon'],
                  maxDR=0.1
                  )
if build_GenSignalDecay: modules.append(RecoMuonMatcher)

MuonSelector= LeptonSkimmer(
                  LepFlavour='Muon',
                  Selection=MuonSelection,
                  Veto=None,
                  minNlep=-1
                  )
modules.append(MuonSelector)
ElectronSelector= LeptonSkimmer(
                  LepFlavour='Electron',
                  Selection=ElectronSelection,
                  Veto=None,
                  minNlep=-1
                  )
modules.append(ElectronSelector)
TauSelector= LeptonSkimmer(
                  LepFlavour='Tau',
                  Selection=TauSelection,
                  Veto=None,
                  minNlep=-1
                  )
modules.append(TauSelector)
HTCalculator= HTSkimmer(
                  minJetPt=25,
                  minJetEta=4.7,
                  minJetPUid=-1,
                  minHT=-1,
                  collection="Jet",
                  HTname="HT"
                  )
modules.append(HTCalculator)
LooseHTCalculator= HTSkimmer(
                  minJetPt=25,
                  minJetEta=4.7,
                  minJetPUid=3,
                  minHT=-1,
                  collection="Jet",
                  HTname="looseHT"
                  )
modules.append(LooseHTCalculator)
MediumHTCalculator= HTSkimmer(
                  minJetPt=25,
                  minJetEta=4.7,
                  minJetPUid=5,
                  minHT=-1,
                  collection="Jet",
                  HTname="mediumHT"
                  )
modules.append(MediumHTCalculator)
TightHTCalculator= HTSkimmer(
                  minJetPt=25,
                  minJetEta=4.7,
                  minJetPUid=6,
                  minHT=-1,
                  collection="Jet",
                  HTname="tightHT"
                  )
modules.append(TightHTCalculator)

JetSelector=JetSkimmer( 
                  BtagWPs=[0.1274, 0.4229, 0.7813 ], 
                  nGoodJetMin=-1, 
                  nBJetMax=20 , 
                  Selection=JetSelection,
                  Veto=None
                  )
modules.append(JetSelector)
JetMuonCleaner=JetLepCleaner( 
                  Lepton='Muon',
                  Jet='Jet',
                  BJet='BJet',
                  dRBJet=0.3,
                  dRJet=0.3,
                  RemoveFailingObjects=False)
modules.append(JetMuonCleaner)   



if not production:
   p = PostProcessor(outputFolder, fnames, cut=TriggerCuts,  modules=modules,branchsel = branchsel_in, outputbranchsel = branchsel_out, prefetch = True, longTermCache = True, provenance=True, maxEntries=maxEntries)
else:
   p = PostProcessor(".", inputFiles(), cut=TriggerCuts,  modules=modules,branchsel = branchsel_in, outputbranchsel = branchsel_out, provenance=True, fwkJobReport=True)  

p.run() ###############RUN here######################
################################# options #############################
#class PostProcessor:
# outputDir, inputFiles, cut=None, branchsel=None, modules=[],compression="LZMA:9", friend=False, postfix=None, jsonInput=None,noOut=False, justcount=False, provenance=False, haddFileName=None,fwkJobReport=False, histFileName=None, histDirName=None, outputbranchsel=None, maxEntries=None, firstEntry=0, prefetch=False, longTermCache=False
print "done"
