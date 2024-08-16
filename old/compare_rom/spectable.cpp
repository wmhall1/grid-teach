#include<iostream>
#include<iomanip>
#include<string>
#include<fstream>

using namespace std;

int main(){
	ifstream input;
	char run;
	string runstring;

	input.open("spectral");
	
	while(!input.eof()){
		input >> runstring;
		cout << runstring << " & ";
		input >> runstring;
		cout << runstring;
		input >> runstring;
		cout << runstring;
		input >> runstring;
		input >> runstring;
		cout << "$\\pm$" << runstring << " & ";
		input >> runstring;
		cout << runstring << "$\\pm$";
		input >> runstring;
		input >> runstring;
		cout << runstring << " & ";
		input >> runstring;
		cout << runstring << "$\\pm$";
		input >> runstring;
		cout << runstring;
	        input >> runstring;
		cout << runstring<< "\\\\" << endl;
		getline(input,runstring);
	}	


	input.close();
	return 0;
}
