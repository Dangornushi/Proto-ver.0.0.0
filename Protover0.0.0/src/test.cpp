#include "main.hpp"


void sub( int j, map <string, int> intvall ) {
    string ans;
    if ( j == 0 ) {
        ans = "x";
        j++;
    }
    if ( j == 1 ) {
        for ( int whilen = 0; whilen < 10; whilen++ ) {
            intvall[ans] = intvall[ans] + 1;
        }
        j = 2;
    }
    if ( j== 2 ) {
        cout << intvall["x"] << endl;
    }
}

int main( void ) {
    map <string, int> intvall;
    sub(0,  intvall);
    return 0;
}
