#include "main.hpp"

int main( int argc, char **arg ) {
    string inpfilename = arg[1], data;
    ifstream ifs ( inpfilename+"s" ) ;
    ofstream ofs ( split( inpfilename, "." )[0]+".way" ) ;

    while ( getline( ifs, data ) ) {
        ofs << data << endl;
    }
    return 0;
} 
