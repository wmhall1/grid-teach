/*
 *
 * Weston Hall
 * Original:08-19-21
 * Final: 03-30-22
 *
 * This code will get minimums from output file below S cutoff
 *
 * Input:
 *  -"output" file, generally one directory back, "../output"
 *  -user input S cutoff
 *
 * Output:
 *  -"minoutput1" file containing all matches below S cutoff
 *   from output with S's and Probs
 *  -"minoutput" file containing all matches below S cutoff
 *   in proper format.
 *
 *
 */

#include<iostream>
#include<iomanip>
#include<fstream>
#include<string>
#include<cmath>

using namespace std;

int main(){
    
    //Declare variables
    ifstream input;
    ifstream modecs;
    ofstream output;
    //Name output:
    string filename = "../output_n";
    string title;
    string trash;
    double sigma;
    double S;
    string mintitle;
    double min = 100;

    input.open(filename);
    modecs.open("../modecs_n");
    output.open("minoutput1_n");

    //Input S cutoff
    cout << "How small of S looking for? ";
    cin >> S;
    
    //Read through matches
    while(!input.eof()){
        //Read line up to 'S'
        getline(input,title,'S');
        //Get the S
        input >> trash >> sigma;
        
        //If less than cutoff write to "minoutput"
        if(sigma < S){
            output << title;
            //output << "S= " << sigma;
            output << " " << sigma;
            getline(input, trash);

            output << "\t" << trash.substr(7,15) << endl;

            if(sigma < min){
                min = sigma;
                mintitle = title;
            }
        }
        //If not, trash it
        else{
            getline(input,trash);    
    
        }
    }

    //Output to screen overall minimum
    cout << "minimum is " << mintitle << " S= " << min << endl;
    input.close();
    output.close();

    input.clear();
    output.clear();
    input.open("minoutput1_n");
    output.open("minoutput_n");

    while(!input.eof()){
        getline(input, trash);
        output << trash.substr(0,52) << endl;
    }
    
    input.close();
    output.close();
    modecs.close();
    return 0;
}
