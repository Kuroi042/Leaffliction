#pragma once

#include <iostream>
#include <Rcpp.h>
#include <string>

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/geometry/2d.hpp>
#include <opencv2/core/mat.hpp>

class transform
{
private:
    std::string path;
public:
    transform(/* args */);
    ~transform();
};

