/*
 *
 * Weston Hall
 * Original:08-19-21
 * Final: 03-30-22
 *
 * This code will get minimums from output file below S cutoff
 *
 * Input:
 *  -"output" file, generally one directory back, "../output"
 *  -user input S cutoff
 *
 * Output:
 *  -"minoutput1" file containing all matches below S cutoff
 *   from output with S's and Probs
 *  -"minoutput" file containing all matches below S cutoff
 *   in proper format.
 *
 *
 */

#include<iostream>
#include<iomanip>
#include<fstream>
#include<string>
#include<cmath>

using namespace std;

int main(){
    
    //Declare variables
    ifstream input;
    ifstream modecs;
    ofstream output, output2;
    //Name output:
    string filename = "../output";
    string title;
    string trash;
    double sigma;
    double S;
    string mintitle;
    bool mincatch = true;
    double min = 1000000;
    input.open(filename);
    modecs.open("../modecs");
    output.open("minoutput1");
    double temp, mass, hy, he;

    //Input S cutoff
    cout << "How small of S looking for? ";
    cin >> S;
    
    //Read through matches
    do{
    while(!input.eof()){
        //Read line up to 'S'
        getline(input,title,'S');
        //Get the S
        input >> trash >> sigma;
         
        //If less than cutoff write to "minoutput"

	//cout << sigma << endl;
	if(sigma < S){
	    output << title;
	    //cout << title << endl;
	    //output << "S= " << sigma;
	    output << " " << sigma;
	    getline(input, trash);

	    output << "\t" << trash.substr(7,15) << endl;

	    if(sigma < min){
		min = sigma;
		mincatch = false;
		mintitle = title;
	    }
	}
	//If not, trash it
	else{
	    getline(input,trash);    
    
	}
    }
    input.close();
    input.clear();
    input.open(filename);
    S = S+10;
    //cout << min << " " << S << endl;
    }while(mincatch);

    //Output to screen overall minimum
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
    //modecs.close();
//cout << "here" << endl;
    input.open("minoutput");
    output.open("minoutput2");
    double mtemp, mmass, mhe, mhy;
    string modes;
    while(input >> temp >> mass >> trash >> he >> hy >> S){
	    do{
	    modecs >> mtemp >> mmass >> trash >> mhe >> mhy;
	    getline(modecs, modes);
	    }while(!(mtemp == temp && mmass == mass && mhe == he && mhy == hy));
	    getline(input, trash);
	    output << temp << ";" << mass << ";" << he << ";" << hy << ";" << S << ";" << modes << endl;
    }
    input.close();
    output.close();
    modecs.close();
    return 0;
}
