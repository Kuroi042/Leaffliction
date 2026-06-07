
#include "class.hpp"
using namespace Rcpp;


int onlycpp(std::string towrite)
{
    std::cout << towrite << std::endl;
    return(0);
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