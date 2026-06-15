#pragma once
#include <iostream>
#include <Rcpp.h>
#include <string>
#include <typeinfo>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/geometry/2d.hpp>

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
    std::string aug;

    cv::Mat myimg;
    cv::Mat modified;
    std::vector<cv::Mat>allimages;

    //tswora
    public:
    image(std::string _path , std::string _marad);
    ~image();
    void summary();
    void saveimg(std::string path);
    void ft_rotation(int degree);
    void ft_blur(int sigmaX , int sigmaY );
    void ft_brightness(float degree);
    void ft_scale(float size);
    void ft_flip(int direction);
    void ft_zoom(float height);


    // std::string ft_crop(int degree);
    // std::string ft_crop(int degree);
    // std::string ft_crop(int degree);



};