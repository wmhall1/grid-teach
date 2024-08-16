/*
 *
 * Weston Hall
 * 01-30-22
 * THis code will get the minimums from the old output
 * And also calculate sigmas
 *
 *
 10650.0    900.0    300.0    350.0    600.0    5.9147   0.9354
 */

#include<iostream>
#include<iomanip>
#include<fstream>
#include<string>
#include<cmath>

using namespace std;

int main(){

	ifstream input;
	ofstream output;
	string filename = "../output";
	string title;
	string trash;
	double sigma;
	double S;
	string mintitle;
	double min = 100;

	input.open(filename);
	output.open("minoutput1");
	cout << "How small of S looking for? ";
	cin >> S;

	while(!input.eof()){
		getline(input,title,'S');
		input >> trash >> sigma;
		if(sigma < S){
			output << title;
			//output << "S= " << sigma;
			output << " " << sigma;
			getline(input, trash);

			output << "\t" << trash.substr(7,20) << endl;

			if(sigma < min){
				min = sigma;
				mintitle = title;
			}
		}
		else{
			getline(input,trash);	
	
		}
	}
	cout << "minimum is " << mintitle << " S= " << min << endl;
	input.close();
	output.close();

	input.clear();
	output.clear();
	input.open("minoutput1");
	output.open("minoutput");

	while(!input.eof()){
		getline(input, trash);
		output << trash.substr(0,52) << endl;
	}

	input.close();
	output.close();
	
	/* STARTS HERE */

	double temp, mass, mhe, mh, sigma_t, sigma_m, sigma_he, sigma_h;
	double runtemp, runmass, runhe, runh;
	temp = stod(mintitle.substr(0,7));
	mass = stod(mintitle.substr(11,5));
	mhe = stod(mintitle.substr(28,5));
	mh = stod(mintitle.substr(37,5));
	cout << mintitle << endl;
	cout << temp << " " << mass << " " << mhe << " " << mh << endl;

	input.clear();
	input.open(filename);
	
	while(!input.eof()){
		getline(input, title,'S');

		if(title.substr(0,1) == "1"){

			runtemp = stod(title.substr(0,7));
			runmass = stod(title.substr(11,5));
			runhe = stod(title.substr(28,5));
			runh = stod(title.substr(37,5));
			input >> trash >> sigma;


			if(stod(title.substr(0,7)) == temp &&
				stod(title.substr(11,5)) == mass &&
				stod(title.substr(28,5)) == mhe &&
				stod(title.substr(37,5)) == mh){
			
				sigma_t = sqrt(stod(title.substr(0,7)))
			}
		}
		getline(input,trash);
	}


	return 0;
}
