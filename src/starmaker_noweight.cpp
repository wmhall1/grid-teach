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
                double uncertain;
		double weight;
                Star(double period, double uncertain, double weight){
                        this->period = period;
                        this->uncertain = uncertain;
			this->weight = weight;
                }
                Star() : Star(0,0,0) {}
};

bool compareStars(Star one, Star two);


int findSmallestElement(double arr[], int n){
   /* We are assigning the first array element to
    * the temp variable and then we are comparing
    * all the array elements with the temp inside
    * loop and if the element is smaller than temp
    * then the temp value is replaced by that. This
    * way we always have the smallest value in temp.
    * Finally we are returning temp.
    */
   double temp = arr[0];
   int idx = 0;
   for(int i=0; i<n; i++) {
      if(temp>arr[i] && arr[i] != 0) {
         temp=arr[i];
	 idx = i;
      }
   }
   return idx;
}

int main(){
	// Declarations
	ofstream output, noweight;
	string filename;
	int num, min_amp_idx;
	double period, uncertain, weight;
	
	//Get output file name
	cout << "star name: ";
	cin >> filename;
	
	//Read length of array, # of stars
	cout << "how many periods? ";
	cin >> num;

	//Declare array	
	double periods[num];
	double uncertains[num];
	double weights[num];
	//Declare array 
        Star* stars = new Star[num];


	//Create output file
	output.open(filename);
	noweight.open(filename+ "_un");

	// Read in data
	for(int i = 0; i < num; i++){

		//Ask for data
		cout << "Period " << i+1 << ": ";
		cin >> period;
                cout << "Uncertainties " << i+1 << ": ";
		cin >> uncertain;

		//Save data in array
		periods[i] = period;
		uncertains[i] = uncertain;
		
	}
	
	//Calcualte weights
	min_amp_idx = findSmallestElement(uncertains,num);
	cout << min_amp_idx << endl;
	weights[min_amp_idx] = 1.0;
	for(int i=0; i < num; i++){
		if(i != min_amp_idx && uncertains[i] > 0){
			weights[i] = uncertains[min_amp_idx] / uncertains[i];
		}
		else{
			weights[i] = 1;
		}
	}

	//Assign to stars
	for(int i=0; i < num; i++){
		stars[i].period = periods[i];
		stars[i].uncertain = uncertains[i];
		if(abs(weights[i]) > 0.000000001){
			stars[i].weight = weights[i];
		}
		else{
			stars[i].weight = 0.000001;
		}
	}
	//Display data to screen- debugging purposes
	cout << "Old" << endl;
	for(int i = 0; i < num; i++){
		cout << setprecision(2) << fixed << periods[i] << " & " <<uncertains[i] << " & " << weights[i] << " \\\\" <<  endl;
	}

	sort(stars, stars + num, compareStars);

	//Display again
	cout << endl << "New:" << endl;
       for(int i =0; i<num;i++){
		cout << setprecision(2) << fixed << stars[i].period << " & " << stars[i].uncertain << " & " << stars[i].weight << " \\\\" << endl;

	}	       
	

	//Write output
	for(int i = 0; i < num; i++){
                
		//Only go to next line when not first line
                if(i != 0){
                        output << endl;
			noweight << endl;
                }

                //Write period/weight to output
                output << stars[i].period << " " << stars[i].weight;	
		noweight << stars[i].period << " " << "1";
	}

	return 0;
}

bool compareStars(Star one, Star two){
        return one.period < two.period;
}
