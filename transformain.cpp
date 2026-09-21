#include "transform.hpp"

// [[Rcpp::plugins(cpp17)]]


// [[Rcpp::export]]
int cppmaintranform(Rcpp::List folders_list)
{
    Rcpp::StringVector folders_diali = folders_list.names();
    Rcpp::StringVector files_diali = folders_list[0];

    std::string foldername;
    std::string filename;
    foldername = Rcpp::as<std::string>(folders_diali[0]);
    filename = Rcpp::as<std::string>(files_diali[0]);

    transform obj(filename);

    obj.edge_detect();
    obj.mask();

    obj.summary();


    return(1);
}
