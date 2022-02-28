float Dphi(float phi1, float phi2){
  float Dphi= phi1-phi2;
  if (Dphi>3.14) Dphi -= 6.28;
  if (Dphi<-3.14) Dphi += 6.28;
  return Dphi;

}
