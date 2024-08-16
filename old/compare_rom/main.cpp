#include<iostream>
#include<iomanip>
#include<string>
#include<fstream>

using namespace std;

int main(){
	ifstream input;
	ofstream output;
	string run;

	input.open("weston_ast");
	output.open("weston_ast_adj");
	while(!input.eof()){
		getline(input, run);
		output << run << " & ";
		getline(input, run);
		output << run;
		output << endl;
	}
		

	input.close();
	output.close();
	return 0;
}
