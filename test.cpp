
#include "class.hpp"

// [[Rcpp::plugins(cpp17)]]


int onlycpp(std::string towrite)
{
    std::cout << "c++ wrote " << towrite << std::endl;
    return(0);
}



// [[Rcpp::export]]
int cppmain(std::string fromR , Rcpp::List folders_list)
{


    Rcpp::print(folders_list.names());

    Rcpp::StringVector files_diali = folders_list[1];

    onlycpp(Rcpp::as<std::string>(files_diali[1]));

    image obj(Rcpp::as<std::string>(files_diali[1]),Rcpp::as<std::string>(folders_list[1]));

    obj.summary();




    return(1);
}


