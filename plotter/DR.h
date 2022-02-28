float DR(float eta1, float phi1, float eta2, float phi2){
  float Dphi= phi1-phi2;
  if (Dphi>3.14) Dphi -= 6.28;
  if (Dphi<-3.14) Dphi += 6.28;
  return TMath::Sqrt((eta1-eta2)*(eta1-eta2)+Dphi*Dphi);

}
