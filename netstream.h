
#include <streambuf>
#include <cstring>
#include <iostream>
#include <cstdio>
#include <sstream>
using namespace std;

class SocketBuf : public stringbuf{

public:

protected:
    int tmp = 'h';
    virtual streamsize xsgetn(char* s, streamsize n) {
        cout << __FUNCTION__ << " " << n << "\n";
        return streambuf::xsgetn(s, n);
    }

    virtual int underflow() {
        cout << __FUNCTION__ << "\n";
        cout << streambuf::underflow();
        return streambuf::underflow();
    }
};
