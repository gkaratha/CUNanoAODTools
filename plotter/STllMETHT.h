float MTllMET2(float pT1, float eta1, float phi1, float pT2, float eta2, float phi2,float met_pt, float met_phi){
  TLorentzVector mu1,mu2;
  mu1.SetPtEtaPhiM(pT1,eta1,phi1,0.105);
  mu2.SetPtEtaPhiM(pT2,eta2,phi2,0.105);
  float met_energy=TMath::Sqrt(met_pt*met_pt+91*91);
  float ll_energy=(mu1+mu2).E();
  TVector3 vll,vmet;
  vll.SetPtEtaPhi((mu1+mu2).Pt(),(mu1+mu2).Eta(),(mu1+mu2).Phi());
  vmet.SetPtEtaPhi(met_pt,0,met_phi);
  return TMath::Sqrt( TMath::Power((met_energy+ll_energy),2)-(vmet+vll).Mag2() );
 
}
