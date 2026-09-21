#include "transform.hpp"

transform::transform(std::string _path) : path(_path)
{
    this->myimg = cv::imread(this->path);
        // this->allimages.push_back(this->myimg.clone());

    this->GrayScale = cv::imread(this->path,cv::IMREAD_GRAYSCALE);

    this->width = this->myimg.rows;
    this->height = this->myimg.cols;
}

transform::~transform()
{
}

void transform::summary()
{
    // ft_finalize();

    for (auto &img : this->allimages)
    {
        if (img.channels() == 1) {
        cv::cvtColor(img, img, cv::COLOR_GRAY2BGR);
    }
    if (img.type() != CV_8UC3) {
        img.convertTo(img, CV_8UC3);
    }
        // std::cout << "channels: " << img.channels() << std::endl << "type:" << img.type()  << " " << CV_8UC3 << " " << cv::COLOR_GRAY2BGR << std::endl;
        /* code */
    }
    

    cv::hconcat(this->allimages, this->combined);
    cv::imshow("transforms", this->combined);

    cv::waitKey(0);
}

void transform::ft_finalize()
{
    for (auto &img : this->allimages)
        cv::resize(img, img, cv::Size(this->width, this->height));
}

void transform::edge_detect()
{
    
    cv::Mat temp;
    // cv::Mat kernel = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(15, 15));
    // cv::Mat blackhat;
    // cv::morphologyEx(this->GrayScale, blackhat, cv::MORPH_BLACKHAT, kernel);
    // cv::GaussianBlur(blackhat,this->modified, cv::Size(5, 5),1.5f);
    
    // cv::threshold(blackhat, this->modified, 0, 255, cv::THRESH_BINARY | cv::THRESH_OTSU);
    // this->allimages.push_back(this->modified.clone());
    // cv::GaussianBlur(this->GrayScale, this->modified, cv::Size(5, 5),1.5f);
    cv::GaussianBlur(this->GrayScale,temp, cv::Size(5, 5),1.5f);
    
    cv::threshold(temp, this->modified, 0, 255, cv::THRESH_BINARY_INV | cv::THRESH_OTSU);
    this->allimages.push_back(this->modified.clone());
    // cv::threshold(this->GrayScale, this->modified, 0, 255, cv::THRESH_BINARY_INV | cv::THRESH_OTSU);
    // this->allimages.push_back(this->modified.clone());
    this->allimages.push_back(this->GrayScale.clone());

    
    //     this->allimages.push_back(this->modified.clone());

    // cv::GaussianBlur(this->GrayScale, this->modified, cv::Size(5, 5),1.5f);
    // this->allimages.push_back(this->modified.clone());
    
    // cv::GaussianBlur(this->myimg, this->modified, cv::Size(0, 0), 0.9f, 0.9f);
    
    
    // cv::Canny(this->myimg,this->modified,100,200);


    // this->allimages.push_back(this->modified.clone());
    // cv::Canny(this->GrayScale,this->modified,255/3,255);
    // this->allimages.push_back(this->modified.clone());
    // cv::Canny(this->myimg,this->modified,255/3,255);
    // this->allimages.push_back(this->modified.clone());

}

void transform::mask()
{

    cv::Mat temp;
    // cv::Mat masked;
    // int sup[] = {160,255,255};
    // int low[] = {90,0,0};
        this->allimages.push_back(this->myimg.clone());

    cv::Scalar low(40,30,30); // fine tune
    cv::Scalar sup(75,255,255);

    cv::cvtColor(this->myimg,temp,   cv::COLOR_BGR2HSV );
    cv::inRange(temp,low,sup,temp);
    
        this->allimages.push_back(temp.clone());

        // cv


}