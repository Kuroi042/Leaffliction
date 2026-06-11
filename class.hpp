#pragma once
#include <iostream>
#include <Rcpp.h>
#include <string>
#include <typeinfo>
#include <opencv2/opencv.hpp>

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

class image 
{
    private:
    std::string path;
    std::string marad;
    cv::Mat myimg;
    //tswora
    public:
    image(std::string _path , std::string _marad);
    ~image();
    void summary();

};