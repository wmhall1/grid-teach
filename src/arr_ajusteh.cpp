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
 *  Limitations:
 *   -Proper formatting of input required.
 *   -Maximum of 100 periods per star
 *
 */

#include"header.h"

int main(int argc, char *argv[]){
    // First lets declare variables
    
    //Heres the variables for file names and streams
    string calcpname, perfilename, ofilename;
    ifstream calcperiods;
    ofstream doutput;
    
    //Here is user input data and counts to hold:
    int l;
    string run;

    //Variables to count num stars in concatenated file.
    int starcount = 0;

    //Debug mode: add any argument when executing to enter debug mode ex: "./a.out -d"
    bool debug = false;
    if(argc > 1){debug=true;cout << "debug" << endl; doutput.open("debug");}
    
    //Now lets get user data we will need:

    //grid filename hardcoded in as "calcperiods"
    //cout << "Grid model filename: ";
    //cin >> calcpname;
    calcpname = "calcperiods";
    
    //Read in star file names
    vector<Star> stars;
    int ie = 0;
    
    while(perfilename != "stop" && perfilename !="Stop"){
	    cout << "Star file name (\'stop\' to stop)";
	    cin >> perfilename;
	    cout << endl;
	    if(perfilename !="stop" && perfilename!="Stop"){
		stars.push_back(Star(perfilename));
		stars.at(ie).build();
		//stars.at(ie).display();
		for(int k=0; k < stars.at(ie).np; k++){
			cout << "Period = " << stars.at(ie).periods.at(k) << "   ";
			cout << "What is the l? 1 or 2(whatever)?";
			cin >> l;
			cout << endl;
			stars.at(ie).add_ell(l);
		}//k
		string comm = "rm " + perfilename + ".*";
		system(comm.c_str());
	    }
	    ie++;
    }
    stars.at(0).display();
    

    //check opening file for errors, quit program if they dont exist
    calcperiods.open(calcpname);
    if(!calcperiods){
        cout << "Grid model file did not open." << endl;
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
    
    /////LOGIC STARTS HERE////
    //
    //For each grid model
    for(int ifi = 0; ifi < starcount; ifi++){
	    /////MAKING THE MODEL///////////
	    //Get header
	    getline(calcperiods, run);
	    Model model = Model(run);
	    
	    int ll = 1;
	    double period;
	    
	    //Make model
	    while(ll != 0){
		calcperiods >> ll >> period;
		//IF calcperiods not formatted correctly, quit.
		if(ll!= 1 && ll != 2 && ll != 0){
			cout << "Model smashing at:" << endl << run << endl;
			exit(1);
		}
		model.add_ell(ll);
		model.add_period(period);
	    }

	    model.ii = model.periods.size();
	    getline(calcperiods,run);
	    getline(calcperiods,run);

	    //Get fit
	    for(int j = 0; j < stars.size(); j++){
	    	Fit fit = get_fit(stars.at(j), model);
		stars.at(j).write(model.header.substr(2,45), "out");
            	stars.at(j).write(" S(sec)= " + to_string(fit.S).substr(0,7) + "\tProb="+to_string(fit.prob).substr(0,6)+"\n", "out");
	        
		//Write mode output
		if(fit.oneto){
			stars.at(j).write(model.header.substr(2,45) + "  ", "mode");
			for(int i =0; i < stars.at(j).np; i++){
				stars.at(j).write(to_string(fit.periods.at(i)).substr(0,6) + "(" + 
						to_string(fit.ells.at(i)) + "," + to_string(fit.ks.at(i)) + ")", "mode");
				if(i != stars.at(j).np - 1){
					stars.at(j).write(", ", "mode");
				}
			}
			stars.at(j).write("\n","mode");
		}

		//Write min output
		if(fit.oneto && fit.S < stars.at(j).np){
			stars.at(j).write(model.header.substr(2,45), "min");
			stars.at(j).write("  " + to_string(fit.S).substr(0,7)+"\n", "min");
		}


	    }//j
	    

	    //LOGGING
	    if(ifi == starcount / 10){
		    cout << "10\% done" << endl;
	    }
	    if(ifi == starcount *2/10){
		    cout << "20\% done" << endl;
	    }
	    if(ifi == starcount *3 /10){
                    cout << "30\% done" << endl;
            }
	    if(ifi == starcount *4 /10){
                    cout << "40\% done" << endl;
            }
	    if(ifi == starcount *5 /10){
                    cout << "50\% done" << endl;
            }
	    if(ifi == starcount *6 /10){
                    cout << "60\% done" << endl;
            }
	    if(ifi == starcount *7 /10){
                    cout << "70\% done" << endl;
            }
	    if(ifi == starcount *8 /10){
                    cout << "80\% done" << endl;
            }
	    if(ifi == starcount *9 /10){
                    cout << "90\% done" << endl;
            }
    }//ifi

    //Closing files
    calcperiods.close();
    
    return 0;
}
