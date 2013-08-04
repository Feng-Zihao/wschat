#include <iostream>
#include <string>
using namespace std;
#include "netstream.h"

int main(int argc, const char *argv[])
{
    char a[] = "1234";
    cout << __FILE__ << " " << __LINE__ << " " << __FUNCTION__ << "\n";
    SocketBuf socketBuf;
    socketBuf.pubsetbuf(a, 5);
    iostream io(&socketBuf);
    string str;
    cout << __FILE__ << " " << __LINE__ << " " << __FUNCTION__ << "\n";
    cin >> str;
    io << str;
    str = "";
    io >> str;
    cout << __FILE__ << " " << __LINE__ << " " << __FUNCTION__ << "\n";
    cout << str;
    cout << __FILE__ << " " << __LINE__ << " " << __FUNCTION__ << "\n";
    return 0;
}
