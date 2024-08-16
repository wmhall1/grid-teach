/* 
 * Weston Hall
 * Grid comparison code
 * 06/18/2021
 *
 * The majority of this code was taken from the ajusteh comparison code written
 * in FORTRAN by Dr. Endl. I have rewritten it in hopefully the same manner and
 * added some of my own touches. Should be able to read grids that have been
 * concatenated in the same file, instead of hard coding individual file names
 *
 */

#include<iostream>
#include<iomanip>
#include<string>
#include<fstream>
#include<cmath>
#include<chrono>

using namespace std;

int main(int argc, char *argv[]){
	// First lets declare variables
	
	//Heres the variables for file names and streams
	string calcpname, perfilename, ofilename;
	ifstream calcperiods, periodlist;
	ofstream output, outputper, doutput;
	
	//Here is user input data and counts to hold:
	int l, np = 0, ii, num, iil1, iil2;
	string run;

	//Here is the arrays declared:
	double modec[100]={0},dif[200]={0},modecs[200]={1},llcs[200]={0},prob=0, ll[100]={0}, smin=1000000.0;
	
	//Variables to count num stars in concatenated file.
	double doubrun;
	int starcount = 0;

	//Debug mode: add any argument when executing to enter debug mode ex: "./a.out -d"
	bool debug = false;
	if(argc > 1){debug=true;cout << "debug" << endl; doutput.open("debug");}
	
	//Declare the probability variables
	double sigma3, sigma2, wt;
	
	//Declare matching variable
	bool goto9000 = false;

	//Now lets get user data we will need
	//Get grid, and star file name from terminal
	calcperiods.open("calcperiods");

	if(!calcperiods){
		cout << "Grid model filename: ";
		cin >> calcpname;
		calcperiods.open(calcpname);
	}

	cout << endl << "File with periods (lowest -> highest): ";
	cin >> perfilename;
	cout << endl;

	//check opening those files for errors, quit program if they dont exist
	if(!calcperiods){
		cout << "Grid model file did not open." << endl;
		exit(1);
	}
	periodlist.open(perfilename);
	if(!periodlist){
		cout << "Period file did not open." << endl;
		exit(1);
	}
	
	//This part counts num stars in grid
	while(calcperiods >> doubrun){
		if(doubrun == 0){
			calcperiods >> doubrun;
			if(doubrun == 100000){
				starcount++;
			}
		}
	}
	calcperiods.close();
	calcperiods.clear();
	calcperiods.open(calcpname);
	if(debug){cout << "num of stars in grid = " << starcount << endl;}
	
	//Lets get the np (number of periods) from the file by reading the lines and then closing and reopening
	while(getline(periodlist,run)){
		np++;
	}
	periodlist.close();
	periodlist.clear();
	periodlist.open(perfilename);
	if(debug){cout <<"np detected = " <<  np << endl << "debug mode: manually set np = "; cin >> np;}
	
	//Declare observed sizes
	double modeo[np] = {0};
	double sigmao[np] = {0};
	double w[np] = {0};
	double limposed[np] = {0};


	//Read in modeo and sigmao from period file
	for(int i = 0; i < np; i++){
		periodlist >> modeo[i] >> sigmao[i];
		w[i] = 1/(sigmao[i]*sigmao[i]);
	}

	//Now lets prompt more user info on naming output
	cout << "Output file name will be: ";
	cin >> ofilename;
	output.open(ofilename);

	//fill the limposed, let user pick which l to use
	for(int i = 0; i < np; i++){
		cout << "Period = " << modeo[i] << "   ";
		cout << "What is the l? 1 or 2(whatever)?";
		cin >> limposed[i];
	}
	
	bool d9000 = false;
	char answer;
	if(debug){
		cout << "debug mode: Disable matching (Y/N)? "; 
		cin >> answer;
		if(answer == 'Y' || answer == 'y'){
			d9000 = true;
			cout << "disabled    " << answer << endl;
			//sleep_for(1000);
		}
	}
	
	outputper.open("outputper");

	/*
	 * This next part she starts reading individual files. Not what Im gonna do
	 * So instead I will write it to read just the first star in the grid.
	 * If it works I will loop for the rest.
	 */

	//ifi loops for number of stars in grid
	for(int ifi=0; ifi<starcount; ifi++){
		getline(calcperiods,run);	//Read all of label to the /n character
		
		int i = 0;
		do{				//Read in ll and modec for particular model
			calcperiods >> ll[i] >> modec[i];
			i++;
		}while(ll[i-1] != 0);

		ii = i-1;			//Get total number of periods
		
		i = 0;	//just in case
		//Need to find number of l=1 and l=2
		for(int i=0;i<ii;i++){
			if(ll[i] == 1 && ll[i+1] == 2){
				num = i;
			}
		}
		iil1=num+1;		//num l=1
		iil2= ii -iil1;		//num l=2
		

		/* Matching observed modes to calculated modes*/	
		for(int i =0; i< np; i++){
			smin = 1000000.0;			//Set min very high
			outputper << run.substr(2,45);

		        if(debug){outputper << " pmode=" << modeo[i] << "  g";}
			
			for(int j=0; j<ii;j++){

				dif[j] = abs(modeo[i]-modec[j]);	//Calcualte difference

				if(limposed[i] == 2){
					if(dif[j] < smin){		//If difference is <smin
						smin = dif[j];	
						modecs[i] = modec[j];	//add to array
						llcs[i] = ll[j];
									//add to array
					}
				}
				else if(limposed[i] == 1){
					if(dif[j] < smin && ll[j] == 1){	//Same here
						smin = dif[j];
						modecs[i] = modec[j];
						llcs[i] = ll[j];	
					}
				}		
			}
		
			//Write chosen periods and modes in another file
			outputper <<  "mode=" << modecs[i] << " l=" << llcs[i] << endl;
		}

		/*Insures one-to-one matching*/
		
		goto9000 = false;
		if(!d9000){
			for(int i=0;i<np;i++){
				if(modecs[i] == modecs[i+1]){
					//goto 9000
					goto9000 = true;
				}
				if(modecs[i] == modecs[i+1]){
					goto9000 = true;
				}
				//If any of the modecs are the same, set goto9000
			}
		}

		//As long as its one-to-one
		if(!goto9000){
			//calculate sigma**2
			//Initialize wt, sigma2, prob
			wt = 0.0;
			sigma2 = 0.0;
			prob = 0.0;
	
			//Increment the variables
			for(int i = 0; i < np ; i++){
				wt = wt + w[i];
				sigma2 = sigma2 + pow((modeo[i]-modecs[i]),2)*w[i];
				//This part is the calculation of probability from sigma2
				if(llcs[i] == 1){
					prob = prob + 1/(pow((modeo[i]-modecs[i]),2)*w[i]*iil1/ii);
				}
				if(llcs[i] == 2){
					prob = prob + 1/(pow((modeo[i]-modecs[i]),2)*w[i]*iil2*2.258/ii);
				}
			}
	
			//Adjust prob
			prob=prob*86.39696/ii;
			//thats the value I have to apply my cut in seconds(?)
			
			//Calculate sigma3
			sigma3=sqrt(sigma2/wt);
	
			//Write to output
			if(run.length() < 30){
				output << run << setw(25-run.length());
			}
			else{
				output << run.substr(2,45);
			}
			output << " S(sec)= " << setprecision(4) << fixed <<  sigma3 << "\tProb= " << prob << endl;
			
		}

		//DEBUG OUTPUT
		if(debug){
			doutput << run << endl
				<<"modeo   modecs  w  \t    iil1="
			        << iil1 << " iil2 =" << iil2 << " ii =" << ii << endl;
			for(int i=0;i<np;i++){
				doutput << modeo[i] << " " << modecs[i] << " " <<  w[i] << "\t " 
					<< 1/(pow((modeo[i]-modecs[i]),2)*w[i]*iil1/ii)<< endl;
			}
			doutput << "Prob unweighted (sum of last column) = " << prob/86.39696*ii << endl;
		}

		getline(calcperiods,run);	//finish reading line to go to next	
	}
	
	//Close out files
	calcperiods.close();
	periodlist.close();
	output.close();
	outputper.close();
	
	if(debug){for(int i=0;i<300;i++){cout << modecs[i] << endl;}}
	if(debug){cout << endl << "np is " << np << endl << endl;}
	if(debug){cout << "Files closed." << endl << run << endl;doutput.close();}
	if(debug && d9000){cout << "disabled" << endl;}

	return 0;
}
