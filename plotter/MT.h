float MT(float pT1, float phi1, float pT2, float phi2){
  float Dphi= phi1-phi2;
  if (Dphi>3.14) Dphi -= 6.28;
  if (Dphi<-3.14) Dphi += 6.28;
  return TMath::Sqrt(2*pT1*pT2*(1- TMath::Cos(Dphi)));
 
}
