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
   TH2F *h = new TH2F("h"," ",10,-0.887500,   7.056,50,2.284e+01,9.057e+07);
   ifstream sigfile("sigpaw.cnt");
   float sig[30],sigerr[30];
   float energy[81],energyerr[81];
   float extL[82],extH[82];
   int i;
   float a0 = -0.8875;
   float a1 =  0.2480;
   for(i = 0; i < 30; i++){
   	energy[i] = a0 + (a1*i);
   	energyerr[i] = 0.0;
   	extL[i] = 0.0;
   	extH[i] = 0.0;
   }
   float x, y;
   i = 0;
   while(sigfile){
   	sigfile >> x;
   	if(i<29){
   		sig[i]=x;
   	}
   	else{sigerr[i-29]=x;}
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
   TGraph *extLgraph = new TGraph(30,energy,extL);
   TGraph *extHgraph = new TGraph(30,energy,extH);
   TGraphErrors *sigexp = new TGraphErrors(29,energy,sig,energyerr,sigerr);
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
   extLgraph->DrawGraph(10,&extLgraph->GetX()[0],&extLgraph->GetY()[0],"L");
   extHgraph->SetLineStyle(1);
   extHgraph->DrawGraph(10,&extHgraph->GetX()[20],&extHgraph->GetY()[20],"L");
   TArrow *arrow1 = new TArrow(8.485e-01,8.913e+03,8.485e-01,1.427e+03,0.02,">");
   arrow1->Draw();
   TArrow *arrow2 = new TArrow(1.344e+00,4.843e+04,1.344e+00,7.751e+03,0.02,">");
   arrow2->Draw();
   TArrow *arrow3 = new TArrow(4.073e+00,6.347e+06,4.073e+00,1.016e+06,0.02,">");
   arrow3->Draw();
   TArrow *arrow4 = new TArrow(4.817e+00,1.716e+07,4.817e+00,2.746e+06,0.02,">");
   arrow4->Draw();
   c1->Update();
   c1->Print("sigext.pdf");
   c1->Print("sigext.eps");
   c1->Print("sigext.ps");
}
