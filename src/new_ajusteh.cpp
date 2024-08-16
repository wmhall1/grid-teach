/* 
 * Weston Hall
 * Grid comparison code
 * Original: 06/18/2021
 * Final: 03/30/2022
 * Updated: 08/16/2024
 *
 * The majority of this code's logic was taken from the ajusteh comparison code written
 * in FORTRAN by Dr. Barbara Castanheira Endl. I have rewritten it to be a bit more
 * streamlined, have more readable output, and work for my format of grid. Should be 
 * able to read grids that have been concatenated in the same file, instead of hard 
 * coding individual file names as previous grids have been.
 *
 * Differences from ajusteh.cpp: This includes the N/100 factor in calculating sigma
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

using namespace std;

int main(int argc, char *argv[]){
    // First lets declare variables
    
    //Heres the variables for file names and streams
    string calcpname, perfilename, ofilename;
    ifstream calcperiods, periodlist;
    ofstream output, outputper, doutput, modeput, minoutput;//, newcalcp;
    
    //Here is user input data and counts to hold:
    int l, np = 0, ii, num, iil1, iil2;
    string run;

    //Here is the arrays declared:
    double modec[100]={0},dif[200]={0},modecs[200]={1},llcs[200]={0},prob=0, ll[100]={0}, smin=1000000.0;
    int ks[100] = {0};

    //Variables to count num stars in concatenated file.
    double doubrun;
    int starcount = 0;

    //Debug mode: add any argument when executing to enter debug mode ex: "./a.out -d"
    bool debug = false;
    if(argc > 1){debug=true;cout << "debug" << endl; doutput.open("debug");}
    
    //Declare the probability variables
    double sigma3, sigma2, wt;
    
    //Declare matching variable, triggers if not one-to-one
    bool goto9000 = false;

    //Now lets get user data we will need:

    //grid filename hardcoded in as "calcperiods"
    /*
    cout << "Grid model filename: ";
    cin >> calcpname;
    */
    calcpname = "calcperiods";
    
    //Read in star file name
    cout << endl << "File with periods (lowest -> highest): ";
    cin >> perfilename;
    cout << endl;
    
    //Star file can be inside directory named "star"
    //This checks if star is in main ajusteh directory or
    //star directory, and calls appropriately.
    periodlist.open(perfilename);
    if(!periodlist){
        perfilename = "star/"+perfilename;
    }
    periodlist.close();
    periodlist.clear();

    //check opening those files for errors, quit program if they dont exist
    calcperiods.open(calcpname);
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
    while(!calcperiods.eof()){
        getline(calcperiods,run);
        if(run.substr(0,3) == "  1"){
            starcount++;
        }
    }
    calcperiods.close();
    calcperiods.clear();
    calcperiods.open(calcpname);
    if(debug){cout << "num of stars in grid = " << starcount << endl;}
    
    //Lets get the np (number of periods) from the file by reading 
    //the lines and then closing and reopening
    while(getline(periodlist,run)){
        np++;
    }
    periodlist.close();
    periodlist.clear();
    periodlist.open(perfilename);
    if(debug){cout <<"np detected = " <<  np << endl << "debug mode: manually set np = "; cin >> np;}
    
    //Declare arrays with observed sizes
    double modeo[np] = {0};     //Observed Modes
    double sigmao[np] = {0};    //Observed sigmas
    double w[np] = {0};         //weights for modes
    double limposed[np] = {0};  //ell's given by user

    //Read in modeo and sigmao from period file
    for(int i = 0; i < np; i++){
        periodlist >> modeo[i] >> sigmao[i];
        w[i] = 1/(sigmao[i]*sigmao[i]);
    }

    //Now lets prompt more user info on naming output
    //Output file name hardcoded in as "output"
    /*
    cout << "Output file name will be: ";
    cin >> ofilename;
    */

    ofilename = "output";
    output.open(ofilename);

    modeput.open("modecs");

    //fill the limposed, let user pick which l to use
    for(int i = 0; i < np; i++){
        cout << "Period = " << modeo[i] << "   ";
        cout << "What is the l? 1 or 2(whatever)?";
        cin >> limposed[i];
    }
    
    bool d9000 = false;
    
    //Check some debugging, can disable matching
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
    minoutput.open("mincode/minoutput");
    //newcalcp.open("calcperiods_n");

    /*
     * This next part is the main process of reading in the grid
     */

    //ifi loops for number of stars in grid
    for(int ifi=0; ifi<starcount; ifi++){
        getline(calcperiods,run);    //Read all of label to the /n character
        
        int i = 0;
        do{                //Read in ll and modec for particular model
            calcperiods >> ll[i] >> modec[i];
            i++;
        }while(ll[i-1] != 0 && i < 100);			///8/16/24 Sanity Check

        ii = i-1;            //Get total number of periods
        
        i = 0;    //just in case

        //Need to find number of l=1 and l=2
        for(int i=0;i<ii;i++){
            if(ll[i] == 1 && ll[i+1] == 2){
                num = i;
            }
        }
        iil1=num+1;        //num l=1
        iil2= ii -iil1;        //num l=2
        //cout << "first: " << ii << endl; 

        /* Matching observed modes to calculated modes*/    
        for(int i =0; i< np; i++){
            smin = 1000000.0;            //Set min very high
            outputper << run.substr(2,45);          //write label to outputper

                if(debug){outputper << " pmode=" << modeo[i] << "  g";}
            
            for(int j=0; j<ii;j++){

                dif[j] = abs(modeo[i]-modec[j]);    //Calculate difference

                if(limposed[i] == 2){
                    if(dif[j] < smin){        //If difference is <smin
                        smin = dif[j];    
                        modecs[i] = modec[j];    //add to array
                        llcs[i] = ll[j];
                        ks[i] = j+1;            //add to array
                    }
                }
                else if(limposed[i] == 1){
                    if(dif[j] < smin && ll[j] == 1){    //Same here
                        smin = dif[j];
                        modecs[i] = modec[j];
                        llcs[i] = ll[j];
                        ks[i] = j+1;    
                    }
                }        
            }
        
            //Write chosen periods and modes in outputper
            outputper <<  "mode=" << modecs[i] << " l=" << llcs[i] << endl;
        }

        /*Insures one-to-one matching*/        
        goto9000 = false;    //Named after old FORTRAN convention
        if(!d9000){
            for(int i=0;i<np;i++){
                if(modecs[i] == modecs[i+1]){
                    goto9000 = true;
                }
                if(modecs[i] == modecs[i+1]){
                    goto9000 = true;
                }
                //If any of the modecs are the same, triggers goto9000
            }
        }

        //As long as its one-to-one:
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
            //thats the value I have to apply my cut in seconds
            //prob is not actually used beyond being numerical artifact
            
            //Calculate sigma3
	    sigma3=sqrt(sigma2/wt);
	    
	    //Add factor of N/100
	    if(abs(ii) < 0.00000001){
		    //cout << "ii is 0" << run.substr(2,45) << endl << endl;
		    sigma3=1000000.0;
	    }
	    else{
		    sigma3 = sigma3 * static_cast<double>(ii) / 100;
	    }
          
	    //sigma3=sqrt(sigma2/wt);
	    //CHANGED HERE
	    //
	    //
	    //
	    //
	    //
	    //
	    //Write to output
            if(run.length() < 30){
                    output << run << setw(25-run.length());
            }
            else{
                    output << run.substr(2,45);
            }
            output << " S(sec)= " << setprecision(4) << fixed <<  sigma3 << "\tProb= " << prob << endl;
	    /*if(sigma3 < np){
            	//Write to output
            	if(run.length() < 30){
                	minoutput << run << setw(25-run.length());
			//newcalcp << run << setw(25-run.length());
            	}
            	else{
                	minoutput << run.substr(2,45);
			//newcalcp << run.substr(2,45);
            	}
		newcalcp << run << endl;
            	minoutput << " S(sec)= " << setprecision(4) << fixed <<  sigma3 << "\tProb= " << prob << endl;
		for(int i=0; i<ii; i++){
			for(int j=0; j <np; j++){
				if(abs(modecs[j]-modec[i]) > 0.00000001){
					newcalcp << "           " << ll[i] << "   " << modec[i] << endl;
				}
			}
		}
		newcalcp << "   0.0000000000000000     \n      100000\n"; 
	    }*/

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

        //Print matching modes for later identification
        if(!goto9000){
            modeput << run.substr(2,45) << "    ";
            for(int i = 0; i < np; i++){
                modeput << setprecision(2) << fixed << modecs[i] << "("  << setprecision(0) << fixed << limposed[i] << ",";
	       	if(ks[i] < 10){
			modeput << " ";
		}
		modeput	<< ks[i] <<")";
                if(i != np -1){
                    modeput << ",  ";
                }
            }
            modeput << endl;
        }

        getline(calcperiods,run);    //finish reading line to go to next    
    }
    
    //Close out files
    calcperiods.close();
    periodlist.close();
    output.close();
    outputper.close();
    modeput.close();
    minoutput.close();
	//newcalcp.close();
    
    //more debug output
    if(debug){for(int i=0;i<300;i++){cout << modecs[i] << endl;}}
    if(debug){cout << endl << "np is " << np << endl << endl;}
    if(debug){cout << "Files closed." << endl << run << endl;doutput.close();}
    if(debug && d9000){cout << "disabled" << endl;}

    return 0;
}
