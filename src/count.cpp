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

using namespace std;

int main(){

	ifstream calcperiods;
	ofstream output;
	ofstream outlog;

	string run, nextline;


	calcperiods.open("../calcperiods");
	
	if(!calcperiods){
		cout << "ERR: No calcperiods file" << endl;
		exit(1);
	}
	
	output.open("converging");
	outlog.open("diverging");

	int i = 0;
	while(!calcperiods.eof()){
		getline(calcperiods, run);
		
		if(run.length() > 0 && run.at(2) == '1'){
			getline(calcperiods,nextline);
			if(nextline.at(3) != '0'){
				output << run << endl;
			}
			else{
				outlog << run << endl;
			}
		}

	}


	calcperiods.close();
	output.close();
	outlog.close();

	return 0;
}
