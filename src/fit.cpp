//fit.cpp
#include"header.h"

Fit get_fit(Star star, Model model){
	Fit fit;
	fit.oneto = true;
	double wt = 0.0;
	double sigma2 = 0.0;
	double prob = 0.0;
	double sigma3;
	for(int i = 0; i < star.np; i++){
		fit.add_period(1.0);
		fit.add_ell(1);
		fit.add_k(0);
		double smin = 1000000.0;
		double dif;
		//Fill periods, ells, and ks
		for(int j=0; j < model.ii; j++){
			if(star.ells.at(i) == model.ells.at(j)){
				dif = abs(star.periods.at(i) - model.periods.at(j));
				if(dif < smin){
					smin = dif;
					fit.periods.at(i) = model.periods.at(j);
					fit.ells.at(i) = model.ells.at(j);
					fit.ks.at(i) = j+1;
				}
			}
		}
		//Check oneto
		if(i > 0 && fit.ks.at(i) == fit.ks.at(i-1)){
			fit.oneto = false;
		}

		//Calculate S
		//wt = wt + star.weights.at(i);
		//sigma2 = sigma2 + pow(star.periods.at(i) - fit.periods.at(i), 2) * star.weights.at(i);

		//Calculate prob
		/*
		if(model.ells.at(i) == 1){
			prob += 1/(pow(smin,2)*star.weights.at(i));
		}
		if(model.ells.at(i) == 2){
			prob += 1/(pow(smin,2)*star.weights.at(i));
		}*/

	}//i

	for(int i = 0; i < star.np; i++){
		wt = wt+star.weights.at(i);
		sigma2 = sigma2 + pow((star.periods.at(i) - fit.periods.at(i)),2) * star.weights.at(i);
	}

	sigma3=sqrt(sigma2/wt);
	//Sanity check
	if(model.ii < 0.00001){
		sigma3 = 1000000;
	}
	
	fit.S = sigma3;
	
	fit.prob = prob * 86.39696 / model.ii;
	
	return fit;
}       





