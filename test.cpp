
#include "class.hpp"
using namespace Rcpp;


int onlycpp(std::string towrite)
{
    std::cout << towrite << std::endl;
    return(0);
}

void read_list(RCPP::list thas)
{
    RCPP::list::iterator it = thas.begin();
    while (it != it.end())
    {
        /* code */
        std::cout << *it
        it++; 
    }
    
}




// [[Rcpp::export]]
int totot(std::string fromR, int miw)
{
    hh *h = new hh(miw,20);

    std::cout << "hhlasom " << h->lasom(9 , 88) << std::endl;
    std::cout << "hhneolasom " << h->neolasom() << " " << std::endl;
    onlycpp(fromR);

    delete h;

    return(1);
}


// void run()