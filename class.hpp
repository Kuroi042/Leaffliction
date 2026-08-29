#pragma once
#include <iostream>
#include <Rcpp.h>
#include <string>
#include <typeinfo>
#include <vector>
#include <map>
#include <random>
#include <variant>
#include <algorithm>
#include <filesystem>


#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/geometry/2d.hpp>
#include <opencv2/core/mat.hpp>

using namespace Rcpp;



class image 
{
    private:
    std::string path;
    std::string marad;
    std::string aug;
    int remaining;

    cv::Mat myimg;
    cv::Mat modified;
    std::vector<cv::Mat>allimages;
    std::vector<std::pair<cv::Mat , std::string>>mapimages;
    cv::Mat combined;
    std::vector<std::function<void(bool)>> transformations;
    int width;
    int height;
    
    static std::mt19937 &get_rng();
    public:
    enum augment
    {
        rotation,
        blur,
        brightness,
        scale,
        flip,
        zoom,
        shear,
        translate,
        noise,
        distort
    };
    image(std::string _path , std::string _marad,int count);
    ~image();
    // using params = std::variant<int,float,double>;
    typedef std::variant<int,float,double> params;

    void summary();
    void saveimg(std::string path);
    static void copy_original(std::string path);
    void ft_rotation(int degree);
    void ft_blur(float sigma );
    void ft_brightness(float degree);
    void ft_scale(float size);
    void ft_flip(int direction);
    void ft_zoom(float height);
    void ft_shear(float right, float down);
    void ft_translate(int dx, int dy);
    void ft_noise(double stddev);
    void ft_distort(float strength);


    image::params ft_randomize(image::augment what);

    void ft_finalize();

    void ft_selection(int type);

    void init();





};