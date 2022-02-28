float DphillMET(float pt1, float eta1, float phi1, float pt2, float eta2, float phi2,float metphi){
  TLorentzVector mu1,mu2;
  mu1.SetPtEtaPhiM(pt1, eta1, phi1, 0.105);
  mu2.SetPtEtaPhiM(pt2, eta2, phi2, 0.105);

  float Dphi= metphi-(mu1+mu2).Phi();
  if (Dphi>3.14) Dphi -= 6.28;
  if (Dphi<-3.14) Dphi += 6.28;
  return Dphi;

}
