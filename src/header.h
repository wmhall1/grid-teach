//header.h
#include<iostream>
#include<iomanip>
#include<string>
#include<fstream>
#include<cmath>
#include<chrono>
#include<vector>

using namespace std;

struct Star{
	public:
		int np;
		string starname, filename;
		vector<double> periods;
		vector<double> uncertains;
		vector<double> weights;
		vector<double> modecs;
		vector<int> ells;
		vector<int> ks;
		vector<int> llcs;
		//ofstream output;
	Star(string starname){
			this->starname = starname;
			filename = starname;
			np = 0;
                }
	//Star() : Star(0,0) {}
	void add_ell(int ell);
	void add_modec(double modec);
	void add_k(int k);
	void add_llcs(int llc);
	void display();
	void build();
	void write(string writing,string file);
};

struct Model{
	public:
		int ii;
		string header;
		vector<double> periods;
		vector<int> ells;
	Model(string header){
		this->header = header;
		ii=0;
	}
	void add_period(double period);
	void add_ell(int ell);
	void display();
};

struct Fit{
	public:
		double S, prob;
		bool oneto;
		vector<double> periods;
		vector<int> ells;
		vector<int> ks;
	void add_period(double period);
	void add_ell(int ell);
	void add_k(int k);
	void display();
};

Fit get_fit(Star star, Model model);

//endif
