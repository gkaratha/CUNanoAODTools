float PtllMETratio(float pT1, float eta1, float phi1,float pT2, float eta2, float phi2, float met_pt){
  TLorentzVector vmu1,vmu2;
  vmu1.SetPtEtaPhiM( pT1, eta1, phi1, 0.105); 
  vmu2.SetPtEtaPhiM( pT2, eta2, phi2, 0.105);
  return (vmu1+vmu2).Pt()/met_pt;
}
