#include<iostream>
#include<iomanip>
#include<fstream>
#include<string>

using namespace std;

int main(){
	
	ifstream input;
	ofstream output;
	int i = 0;
	string run;
	
	input.open("weston_ast_adj");
	
	
	while(!input.eof()){
		getline(input,run);
		i++;
	}
	input.close();
	input.clear();
	input.open("weston_ast_adj");

	string star_names[i];
	double ast_temp[i], ast_mass[i];
	
	
	i=0;
	while(!input.eof()){
		input >> star_names[i];
		i++;
		getline(input,run);
	}
	

	i = i-1;	
	for(int j=0; j<i;j++){
		cout << star_names[j] << endl;
		cout << "Temp: ";
		cin >> ast_temp[j];
		cout << "Mass: ";
		cin >> ast_mass[j];
	}


	output.open("casta_ast");
	for(int j=0; j<i;j++){
		output << star_names[j] << " & " << ast_temp[j] << " & "  << ast_mass[j] << endl;
	}

	input.close();

	return 0;
}
