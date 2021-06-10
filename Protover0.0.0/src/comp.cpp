#include "main.hpp"

int main( int argc, char **arg ){
    string data, name = arg[1], funcs;
    stringstream ss, ss2;
    fstream ofs;
    ifstream ifs( split( name, "." )[0]+".way", ios::in );
    ofs.open ( split( name, "." )[0], ios::out|ios::binary );
    int fc = 0;
    vector<string> impv;

    while ( getline( ifs, data ) ) {
        if ( data.find( "call" ) != string::npos ) {
            funcs+=split( split( data, "call " )[1], "[" )[0];
        }
        if ( data.find( ":" ) != string::npos ) {
            funcs = replace( funcs, split( data, "(" )[0] );
        }
        for ( int i = 0; i < data.size();i++ ) {
            string data2 = data.substr( i, data.size()-(data.size()-1) );
            for (const auto &item : data2) {
                ss << hex << int(item);
            }
        }
    }

    ofs << ss.str() << flush;
    ofs.close();
    ifs.close();

    return 0;
}

//i`m an albatraoz
//YMCA
//Loshing it

/*
文字コード：
a 0x02 0x01 g 0x02 0x07 m 0x02 0x13 s 0x02 0x19 y 0x02 0x24
b 0x02 0x02 h 0x02 0x08 n 0x02 0x14 t 0x02 0x20 z 0x02 0x25
c 0x02 0x03 i 0x02 0x09 o 0x02 0x15 v 0x02 0x22
d 0x02 0x04 j 0x02 0x10 p 0x02 0x16 u 0x02 0x21
e 0x02 0x05 k 0x02 0x11 q 0x02 0x17 w 0x02 0x23
f 0x02 0x06 l 0x02 0x12 r 0x02 0x18 x 0x02 0x24
*/
