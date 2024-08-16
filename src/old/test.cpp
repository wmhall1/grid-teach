#include<iostream>
#include<iomanip>
#include<fstream>
#include<string>
#include<cmath>
#include<vector>
#include<algorithm>

using namespace std;

struct Star{
	public:
		double period;
		double amplitude;
		Star(double period, double amplitude){
			this->period = period;
			this->amplitude = amplitude;
		}
		Star() : Star(0,0) {}
};

bool compareStars(Star one, Star two);


int main(){
	// Declarations
	ofstream output;
	string filename;
	int num;
	double period, amplitude, weight;
	
	//Get output file name
	cout << "star name: ";
	cin >> filename;
	
	//Read length of array, # of stars
	cout << "how many periods? ";
	cin >> num;

	//Declare array	
	Star* stars = new Star[num];
	
	//Create output file
	output.open(filename);
	
	// Read in data
	for(int i = 0; i < num; i++){

		//Ask for data
		cout << "Period " << i+1 << ": ";
		cin >> period;
		cout << "Amplitude " << i+1 << ": ";
		cin >> amplitude;
		
		//Save data in array
		stars[i].period = period;
		stars[i].amplitude = amplitude;
		
	}
	

	//Display data to screen- debugging purposes
	/*
	cout << "Old" << endl;
	for(int i = 0; i < num; i++){
		cout << stars[i].period << " " << 1/pow(stars[i].amplitude,2) << endl;
	}
	*/

	/* SOMEWHERE HERE IT SORTS */
	
	sort(stars, stars + num, compareStars);
	
	//Display again? 

	//Write output
	for(int i = 0; i < num; i++){
                
		//Only go to next line when not first line
                if(i != 0){
                        output << endl;
                }

                //Write period/weight to output
                output << stars[i].period << " " << 1 / (pow(stars[i].amplitude,2));	
	}

	return 0;
}

bool compareStars(Star one, Star two){
	return one.period < two.period;
}
