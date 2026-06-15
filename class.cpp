#include "class.hpp"

hh::hh(int _a, int _b) : a(_a), b(_b)
{
    // std::cout << "created" << std::endl;
}

int hh::lasom(int a, int b)
{
    return (a + b);
}

int hh::neolasom()
{
    return (this->a + this->b);
}

hh::~hh()
{
}

image::image(std::string _path, std::string _marad) : path(_path), marad(_marad)
{
    this->myimg = cv::imread(this->path);
}

image::~image()
{
}

void image::summary()
{
    std::cout << "this leaf have " << marad << " located in " << path << std::endl;
    // cv::imwrite("./miw.jpg", cv::rotate(this->myimg))
    // this->modified  = this->myimg;
    cv::imshow("Window Name", this->modified);
    // cv::imshow("Window Name", this->myimg);


    cv::waitKey(0);
}

void image::saveimg(std::string path)
{

    std::string newpath ;

    std::string ext = path.substr(path.rfind('.'));
    std::string filename = path.substr(0,path.rfind('.'));

    newpath = filename + "_" + this->aug + ext;


    cv::imwrite(newpath, this->modified);
}

void image::ft_rotation(int degree)
{
    cv::Point2f center(this->myimg.cols/2.0F,this->myimg.rows/2.0F);
    cv::Mat matrix = cv::getRotationMatrix2D(center,degree,1.0);
    cv::warpAffine(this->myimg , this->modified, matrix , this->myimg.size() );
        this->aug="Rotation";

    
}

void image::ft_blur(int sigmaX , int sigmaY )
{
    // cv::Size(sigmaX,sigmaY);

    cv::GaussianBlur(this->myimg, this->modified,cv::Size(sigmaX,sigmaY),0,0 );
        this->aug="blur";


}

void image::ft_scale(float size)
{
    cv::resize(this->myimg, this->modified,cv::Size(0,0),size,size);
        this->aug="Scale";

}

    void image::ft_flip(int direction)
    {
        cv::flip(this->myimg, this->modified , direction);
        this->aug="flip";
    }


void image::ft_zoom(float height)
{
    int orig_h = this->myimg.rows;
    int orig_w = this->myimg.cols;

    int crop_h = static_cast<int>(orig_h * height);
    int crop_w = static_cast<int>(orig_w * height);

    crop_h = std::max(1, std::min(crop_h, orig_h));
    crop_w = std::max(1, std::min(crop_w, orig_w));

    int x = (orig_w - crop_w) / 2;
    int y = (orig_h - crop_h) / 2;

    cv::Rect roi(x, y, crop_w, crop_h);
    cv::Mat cropped = this->myimg(roi);

    cv::resize(cropped, this->modified, cv::Size(orig_w, orig_h));

    this->aug = "Zoom";
}

    void image::ft_brightness(float degree)
    {
    this->myimg.convertTo(this->modified, -1, degree, 0);

    this->aug = "Brightness";

    }
