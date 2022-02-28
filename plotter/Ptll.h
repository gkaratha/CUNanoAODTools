float Ptll(float pT1, float eta1, float phi1, float mass1, float pT2, float eta2, float phi2, float mass2){
  TLorentzVector vmu1,vmu2;
  vmu1.SetPtEtaPhiM( pT1, eta1, phi1, mass1); 
  vmu2.SetPtEtaPhiM( pT2, eta2, phi2, mass2);
  return (vmu1+vmu2).Pt();
}
