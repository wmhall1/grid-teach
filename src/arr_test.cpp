/* 
 * Weston Hall
 * Grid comparison code
 * Original: 06/18/2021
 * Final: 03/30/2022
 * Updated: 06/13/2022
 *
 * The majority of this code's logic was taken from the ajusteh comparison code written
 * in FORTRAN by Dr. Barbara Castanheira Endl. I have rewritten it to be a bit more
 * streamlined, have more readable output, and work for my format of grid. Should be 
 * able to read grids that have been concatenated in the same file, instead of hard 
 * coding individual file names as previous grids have been.
 *
 * Dependencies:
 *  -written to be used with GNU g++ compiler
 *  -iostream
 *  -iomanip
 *  -string
 *  -fstream
 *  -cmath
 *  -chrono
 *
 *  Input:
 *   -WDEC grid file, labelled "calcperiods" usually
 *   -file containing star periods and weights in format:
 *           212.20 0.00331
 *           270.46 0.02652
 *           304.05 0.017873
 *   -user input for giving ell's for the periods
 *
 *  Output:
 *   -"output" containing all matching 1-1 models with calculated S's
 *   -"outputper" listing the matching model period for each inputted
 *    period. Mainly for debugging purposes
 *   -"modecs" listing the matching periods with (ell,k) for each for
 *    each model.
 *   -"debug" if run with command line arguments, creates file containing
 *    metadata used during process  
 *
 *  Limitations:
 *   -Proper formatting of input required.
 *   -Maximum of 100 periods per star
 *
 *  Bash usage:
 *   -Can be used in bash scripts with format:
 *        ./ajusteh <<< "$STAR 1 1 1"
 *   -Where $STAR is the period filename and the numbers are the ell's
 */

#include<iostream>
#include<iomanip>
#include<string>
#include<fstream>
#include<cmath>
#include<chrono>
#include<vector>

using namespace std;

struct Star{
	public:
		int np;
		string filename;
		vector<double> periods;
		vector<double> uncertains;
		vector<double> weights;
		vector<double> ells;
	Star(string filename){
			this->filename = filename;
			np = 0;
                }
	//Star() : Star(0,0) {}
	void add_ell(int ell);
	void display();
	void build();
};


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
		cout << endl;
	}
}


void Star::build(){
	ifstream input;
	double mode, unc, w;
	string run;
	int j = 0;
	input.open(filename);
	if(!input){
		filename = "star/"+filename;
	}
	input.close();
	input.clear();
	input.open(filename);
	if(!input){
		cout << "Period file "<< filename << " did not open." << endl;
	}
	else{
		while(!input.eof()){
			getline(input, run);
			j++;
		}
		np = j;
		input.close();
		input.clear();
		input.open(filename);
		for(int i = 0; i < np; i++){
			input >> mode >> w;
			periods.push_back(mode);
			weights.push_back(w);
		}
	}

	input.close();
}
/*
int main(){
	Star test = Star("KIC4357037");
	test.build();
	test.display();	
	return 0;
}*/
