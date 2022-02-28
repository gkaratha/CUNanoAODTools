float MTH(float pT1, float eta1, float phi1, float pT2, float eta2, float phi2,float met_pt, float met_phi){
  TLorentzVector vmu1,vmu2;
  vmu1.SetPtEtaPhiM(pT1, eta1, phi1, 0.105);
  vmu2.SetPtEtaPhiM(pT2, eta2, phi2, 0.105);
  float phill=(vmu1+vmu2).Phi(); 
  float Dphi= phill-met_phi;
  if (Dphi>3.14) Dphi -= 6.28;
  if (Dphi<-3.14) Dphi += 6.28;
  return TMath::Sqrt(2*(vmu1+vmu2).Pt()*met_pt*(1- TMath::Cos(Dphi)));
 
}
