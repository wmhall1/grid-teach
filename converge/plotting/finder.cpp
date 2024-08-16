/*
 * Weston Hall
 * 03/01/22
 * This counts the converging models in calcperiods
  1
   0.0000000000000000
      100000

 */

#include<iostream>
#include<iomanip>
#include<fstream>
#include<string>
#include<sstream>

using namespace std;

int main(){

	ifstream calcperiods;
	ofstream output;
	ofstream outlog;

	string run, nextline;
	double temp, mass, helium, hydrogen, ttemp,tmass,thelium,thydrogen;
		
	cout << "Temp:";
	cin >> temp;
	cout << "Mass (xxx.x):";
	cin >> mass;
	cout << "Helium -log()";
	cin >> helium;
	cout << "Hydrogen -log()";
	cin >> hydrogen;
	
	calcperiods.open("../../calcperiods");
	
	if(!calcperiods){
		cout << "ERR: No calcperiods file" << endl;
		exit(1);
	}
	
	output.open("output");
	//outlog.open("diverging");

	int i = 0;
	while(!calcperiods.eof()){
		getline(calcperiods, run);
		nextline ="";
		/*
		ttemp = stod(run.substr(2,7));
		tmass = stod(run.substr(13,5));
		thelium = stod(run.substr(31,4));
		thydrogen=stod(run.substr(8,4));
		*/

//  12600.0    1000.0    200.0   325.0   950.0 
		if(run.length() > 0 && run.at(2) == '1'){
			ttemp = stod(run.substr(2,7));
                	tmass = stod(run.substr(13,5));
                	thelium = stod(run.substr(31,4));
                	thydrogen=stod(run.substr(39,4));
			//cout << ttemp << " " << tmass << " " << thelium << " " << thydrogen << endl;
			if(ttemp == temp && thelium == helium && thydrogen == thydrogen){

				output << run << endl;
				do{
					getline(calcperiods,nextline);
					output << nextline << endl;
					
				}while(nextline.at(6) != '1');
				//output << endl;
			}
		}

	}


	calcperiods.close();
	output.close();
	outlog.close();

	return 0;
}
