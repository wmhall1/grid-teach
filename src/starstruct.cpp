//starstruct.cpp
#include"header.h"

void Star::add_ell(int ell){
	ells.push_back(ell);
}

void Star::display(){
	cout << filename << endl;
	cout << "Period" << "\t" << "Uncert." << "\t" << "Weight" << "\t" << "Ell" << endl;
	cout << setprecision(2) << fixed;
	for(int i=0; i<np; i++){
		if(!periods.empty()){
			cout << periods.at(i);
		}
		cout << "\t";
		if(!uncertains.empty()){
			cout << uncertains.at(i);
		}
		cout << "\t";
	       	if(!weights.empty()){
			cout << weights.at(i);
		}
		cout << "\t";
		if(!ells.empty()){
			cout << ells.at(i) << endl;
		}
		else{
			cout << endl;
		}
	}
		cout << endl << "np: " << np << endl;
}

void Model::display(){
	cout << header << endl;
	for(int i=0; i < periods.size(); i++){
		cout << ells.at(i) << "\t" << periods.at(i) << endl;
	}
	cout << "ii = " << ii << endl;
}


void Star::build(){
	ifstream input;
	double mode, unc, w;
	int j = 0;
	
	input.open(filename);
	if(!input){
		input.close();
		input.clear();
		filename = "star/"+filename;
		input.open(filename);
	}
	
	if(!input){
		cout << "Period file "<< filename << " did not open." << endl;
	}
	else{
		while(input >> mode >> w){
			periods.push_back(mode);
			weights.push_back(w);
			j++;
		}
		np = j;
		input.close();
		input.clear();
	}

	input.close();
}

void Star::add_modec(double modec){
	modecs.push_back(modec);
}
void Star::add_llcs(int llc){
	llcs.push_back(llc);
}
void Star::add_k(int k){
	ks.push_back(k);
}

void Star::write(string writing, string file){
	ofstream output;
	output.open(starname+"."+file, ios::app);
	output << writing;
	output.close();
	output.clear();
}

void Model::add_ell(int ell){
	ells.push_back(ell);
}
void Model::add_period(double period){
	periods.push_back(period);
}



void Fit::add_ell(int ell){
	ells.push_back(ell);
}
void Fit::add_period(double period){
	periods.push_back(period);
}
void Fit::add_k(int k){
	ks.push_back(k);
}
void Fit::display(){
	cout << S << "\t";
	if(oneto){
		cout << "Is oneto";
	}
	else{
		cout << "NOT oneto";
	}
	cout << endl;
	for(int i =0; i < periods.size(); i++){
		cout << ells.at(i) << "\t" << periods.at(i) << "\t" << ks.at(i) << endl;
	}
}

//endif
