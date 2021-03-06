from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import numpy as np
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {
    'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i', 'Int_t': 'I', 'Float_t': 'F',
    'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class LeptonSkimmer(Module):
    def __init__(self, LepFlavour, Selection=None, Veto=None, minNlep=-1):
        self.LepFlavour=LepFlavour,
        self.LepSelection=Selection,
        self.LepVeto=Veto,
        self.minNlep = minNlep,
        self.branchType = {}
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        _brlist_out = wrappedOutputTree._tree.GetListOfBranches()
        branches_out = set(
            [_brlist_out.At(i) for i in range(_brlist_out.GetEntries())])
        branches_out = [
            x for x in branches_out
            if wrappedOutputTree._tree.GetBranchStatus(x.GetName())
        ]
        # Only keep branches with right collection name
        self.brlist_sep = [
            self.filterBranchNames(branches_out,self.LepFlavour[0])
        ]
        self.brlist_all = set(itertools.chain(*(self.brlist_sep)))

        # Create output branches
        self.out = wrappedOutputTree
        for br in self.brlist_all:
            self.out.branch("%s_%s" % (self.LepFlavour[0], br),
                            _rootLeafType2rootBranchType[self.branchType[br]],
                            lenVar="n%s" % self.LepFlavour[0])

        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def filterBranchNames(self, branches, collection):
        out = []
        for br in branches:
            name = br.GetName()
            if not name.startswith(collection + '_'):
                continue
            out.append(name.replace(collection + '_', ''))
            self.branchType[out[-1]] = br.FindLeaf(br.GetName()).GetTypeName()
        return out


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        if self.LepFlavour[0] !="Muon" and self.LepFlavour[0] !="Electron" and self.LepFlavour[0] !="Tau":
           print "LeptonSkimmer:  Invalid or empty Lepton name",self.LepFlavour[0],"skipping evt"
           return False
        leptons = Collection(event, self.LepFlavour[0])
        if len(leptons)< self.minNlep[0]:
           print "LeptonSkimmer: smaller lepton number wrt threshold Nlep=",len(leptons)," thresh.=",self.minNlep[0]," - Skip evt"
           return False
        if self.LepSelection[0]!=None:
          leptons = filter( self.LepSelection[0], leptons)       
        if len(leptons)< self.minNlep[0]: 
           print "LeptonSkimmer: lower lepton (",self.LepFlavour[0],") number that pass selection wrt threshold Nlep=",len(leptons)," thresh.=",self.minNlep[0]," - Skip evt"
           return False

        veto=[]
        if self.LepVeto[0]!=None:
          veto = filter( self.LepVeto[0], leptons)
        if len(veto)>0:
           print "LeptonSkimmer: failed veto - Skip evt"
           return False

        for bridx, br in enumerate(self.brlist_all):
            out = []
            for obj in leptons:
                out.append(getattr(obj, br))
            self.out.fillBranch("%s_%s" % (self.LepFlavour[0], br), out) 
        return True


