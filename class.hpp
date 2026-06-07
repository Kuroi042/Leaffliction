#pragma once
#include <iostream>
#include <Rcpp.h>
#include <string>
using namespace Rcpp;


class hh
{
private:
    /* data */
    int a;
    int b;

public:
    hh(int _a , int _b);
    ~hh();
    int lasom(int a , int b);
    int neolasom();
};

