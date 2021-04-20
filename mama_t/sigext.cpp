{
   gROOT->Reset();
   gROOT->SetStyle("Plain");
   gStyle->SetOptTitle(0);
   gStyle->SetOptStat(0);
   gStyle->SetFillColor(0);
   gStyle->SetPadBorderMode(0);
   m = (TH1F*)gROOT->FindObject("h");
   if (m) m->Delete();
   TCanvas *c1 = new TCanvas("c1","Normalization of gamma-transmission coefficient",600,600);
   TH2F *h = new TH2F("h"," ",10,-0.887500,   6.561,50,8.851e+00,3.339e+07);
   ifstream sigfile("sigpaw.cnt");
   float sig[28],sigerr[28];
   float energy[81],energyerr[81];
   float extL[82],extH[82];
   int i;
   float a0 = -0.8875;
   float a1 =  0.2480;
   for(i = 0; i < 36; i++){
   	energy[i] = a0 + (a1*i);
   	energyerr[i] = 0.0;
   	extL[i] = 0.0;
   	extH[i] = 0.0;
   }
   float x, y;
   i = 0;
   while(sigfile){
   	sigfile >> x;
   	if(i<27){
   		sig[i]=x;
   	}
   	else{sigerr[i-27]=x;}
   	i++;
   }
   ifstream extendfile("extendLH.cnt");
   i = 0;
   while(extendfile){
   	extendfile >> x >> y ;
   	extL[i]=x;
   	extH[i]=y;
   	i++;
   }
   TGraph *extLgraph = new TGraph(36,energy,extL);
   TGraph *extHgraph = new TGraph(36,energy,extH);
   TGraphErrors *sigexp = new TGraphErrors(27,energy,sig,energyerr,sigerr);
   c1->SetLogy();
   c1->SetLeftMargin(0.14);
   h->GetXaxis()->CenterTitle();
   h->GetXaxis()->SetTitle("#gamma-ray energy E_{#gamma} (MeV)");
   h->GetYaxis()->CenterTitle();
   h->GetYaxis()->SetTitleOffset(1.4);
   h->GetYaxis()->SetTitle("Transmission coeff. (arb. units)");
   h->Draw();
   sigexp->SetMarkerStyle(21);
   sigexp->SetMarkerSize(0.8);
   sigexp->Draw("P");
   extLgraph->SetLineStyle(1);
   extLgraph->DrawGraph(11,&extLgraph->GetX()[0],&extLgraph->GetY()[0],"L");
   extHgraph->SetLineStyle(1);
   extHgraph->DrawGraph(18,&extHgraph->GetX()[18],&extHgraph->GetY()[18],"L");
   TArrow *arrow1 = new TArrow(1.097e+00,5.586e+03,1.097e+00,9.879e+02,0.02,">");
   arrow1->Draw();
   TArrow *arrow2 = new TArrow(1.592e+00,1.732e+04,1.592e+00,3.063e+03,0.02,">");
   arrow2->Draw();
   TArrow *arrow3 = new TArrow(3.576e+00,3.992e+05,3.576e+00,7.061e+04,0.02,">");
   arrow3->Draw();
   TArrow *arrow4 = new TArrow(4.320e+00,1.347e+06,4.320e+00,2.383e+05,0.02,">");
   arrow4->Draw();
   c1->Update();
   c1->Print("sigext.pdf");
   c1->Print("sigext.eps");
   c1->Print("sigext.ps");
}
