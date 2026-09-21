#pragma once

#include <iostream>
#include <Rcpp.h>
#include <string>
#include <vector>

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/geometry/2d.hpp>
#include <opencv2/core/mat.hpp>

class transform
{
private:
    std::string path;
    cv::Mat myimg;
    cv::Mat GrayScale;
    cv::Mat modified;
    std::vector<cv::Mat>allimages;
    int width;
    int height;
    cv::Mat combined;

public:
    transform(std::string _path);
    ~transform();

    void summary();
    void ft_finalize();
    void edge_detect();
    void mask();
};

