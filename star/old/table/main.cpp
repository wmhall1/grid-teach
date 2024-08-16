#include<iostream>
#include<iomanip>
#include<string>
#include<fstream>
#include<cmath>
using namespace std;


int main(){
	ifstream star;
	ofstream output;

	string inputfname;
	string outputfname,starname;
	double periods[100], weights[100], amplitudes[100], min;
	int i =0, min_idx;

	cout << "Name:";
	cin >> inputfname;
	starname = inputfname;
	outputfname = inputfname+".out";
	
	cout << "min amp:";
	cin >> min;

	star.open(inputfname);
	if(!star){
		inputfname = "../" + inputfname;
		star.close();
		star.clear();
		star.open(inputfname);
		if(!star){
			cout << "didn't open." << endl;
			exit(1);
		}
	}

	output.open(outputfname);

	while(star >> periods[i] >> weights[i]){
		//cout << periods[i] << " " << weights[i] << endl;
		i++;
	}
	min_idx = -1;
	for(int j = 0; j < i; j++){
		//weights[i] = pow(amplitudes[min_amp_idx],0.5) / pow(amplitudes[i],0.5);
		if(fabs(weights[j] - 1.0) < 0.0000001){
			amplitudes[j] = min;
			min_idx = j;
		}
	}

	if(min_idx >= 0){
		for(int j =0; j < i; j++){
			amplitudes[j] = pow(pow(amplitudes[min_idx],2) / weights[j],0.5);
			if(j==0){
				output << starname;
			}
			output <<" & " << periods[j] << " & " << setprecision(2) << fixed << amplitudes[j] << "\\\\" <<endl;
		}
	}

	else{
		for(int j=0;j <i;j++){
			amplitudes[j] = 1/(pow(weights[j],0.5));
			if(j==0){
				output << starname;
			}
			output << " & "<< periods[j] << " & " << setprecision(2) << fixed << amplitudes[j] << "\\\\" << endl;
		}
	}




	star.close();
	output.close();
	star.clear();
	output.clear();

	return 0;
}
