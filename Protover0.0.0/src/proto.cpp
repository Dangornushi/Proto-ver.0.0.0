#include "main.hpp"

int main( int argc, char **arg ) {

    string comp = "./proc ";
    string pyt = "python3 compile.py ";
    string passbuf = "./prun ";
    string edit = "./edit ";
    string name = arg[1];

    edit = edit + name;
    comp = comp + arg[1];
    passbuf = passbuf + name;
    pyt = pyt + name;

    system(pyt.c_str());
    system(edit.c_str());
    system(comp.c_str());

    return 0;
}
