float MTllMET(float pT1, float eta1, float phi1, float pT2, float eta2, float phi2,float met_pt, float met_phi){
  TLorentzVector mu1,mu2;
  mu1.SetPtEtaPhiM(pT1,eta1,phi1,0.105);
  mu2.SetPtEtaPhiM(pT2,eta2,phi2,0.105);
  float Dphi= (mu1+mu2).Phi()-met_phi;
  if (Dphi>3.14) Dphi -= 6.28;
  if (Dphi<-3.14) Dphi += 6.28;
  return TMath::Sqrt(2*(mu1+mu2).Pt()*met_pt*(1- TMath::Cos(Dphi)));
 
}
