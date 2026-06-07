#include"class.hpp"

hh::hh(int _a , int _b): a(_a) , b(_b)
{
        // std::cout << "created" << std::endl;

}

int hh::lasom(int a, int b)
{
    return(a + b);
}

int hh::neolasom()
{
    return(this->a+this->b);
}




hh::~hh()
{
}
