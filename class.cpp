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

image::image(std::string _path, std::string _marad,int count) : path(_path), marad(_marad) , remaining(count)
{
    this->myimg = cv::imread(this->path);
    this->width = this->myimg.rows;
    this->height = this->myimg.cols;
    std::cout << "created " << this->remaining << std::endl; 
    init();
}

image::~image()
{
}

void image::summary()
{
    std::cout << "this leaf have " << marad << " located in " << path << std::endl;
    std::cout << "size: " << this->allimages.size() << std::endl;
    ft_finalize();
    //     for (size_t i = 0; i < this->allimages.size(); ++i) {
    //     std::cout << "Image " << i << " -> "
    //               << "Rows: " << this->allimages[i].rows
    //               << ", Cols: " << this->allimages[i].cols
    //               << ", Type: " << this->allimages[i].type()
    //               << ", Dims: " << this->allimages[i].dims
    //               << std::endl;
    // }

    cv::hconcat(this->allimages, this->combined);
    cv::imshow("Window Name", this->combined);

    cv::waitKey(0);
}

void image::saveimg(std::string path)
{

    std::string newpath;
    std::string ext;
    std::string filename;

    ext = path.substr(path.rfind('.'));
    filename = path.substr(0, path.rfind('.'));

    for (std::vector<std::pair<cv::Mat , std::string>>::iterator it = this->mapimages.begin(); it != this->mapimages.end() ; ++it)
    { // hna
        newpath = filename + "_" + it->second + ext;
        cv::imwrite(newpath, it->first);
        /* code */
    }
    


}

void image::ft_rotation(int degree)
{
    cv::Point2f center(this->myimg.cols / 2.0F, this->myimg.rows / 2.0F);
    cv::Mat matrix = cv::getRotationMatrix2D(center, degree, 1.0);
    cv::warpAffine(this->myimg, this->modified, matrix, this->myimg.size(), 0, 2);
    this->allimages.push_back(this->modified.clone());
    this->mapimages.push_back(std::pair<cv::Mat , std::string>(this->modified.clone(),"Rotation"));


    this->aug = "Rotation";
}

void image::ft_blur(float sigma)
{
    // cv::Size(sigmaX,sigmaY);

    cv::GaussianBlur(this->myimg, this->modified, cv::Size(0, 0), sigma, sigma);
    this->allimages.push_back(this->modified.clone());
    this->mapimages.push_back(std::pair<cv::Mat , std::string>(this->modified.clone(),"blur"));


    this->aug = "blur";
}

void image::ft_scale(float size)
{
    cv::Mat scaled;
    cv::resize(this->myimg, scaled, cv::Size(0, 0), size, size);
    cv::resize(scaled, this->modified, cv::Size(this->width, this->height));
    this->allimages.push_back(this->modified.clone());
    this->mapimages.push_back(std::pair<cv::Mat , std::string>(this->modified.clone(),"Scale"));


    this->aug = "Scale";
}

void image::ft_flip(int direction)
{
    cv::flip(this->myimg, this->modified, direction);
    this->allimages.push_back(this->modified.clone());
    this->mapimages.push_back(std::pair<cv::Mat , std::string>(this->modified.clone(),"flip"));

    this->aug = "flip";

    // this->tranformations.push_back([this](){std::get<int>(ft_randomize(augment::flip))};);
}

void image::ft_zoom(float height)
{

    if (height >= 1.0)
    {
        std::cerr << "your zoom is not working please type a value < 1.0" << std::endl;
        return;
    }

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
    this->allimages.push_back(this->modified.clone());
    this->mapimages.push_back(std::pair<cv::Mat , std::string>(this->modified.clone(),"Zoom"));


    this->aug = "Zoom";
}

void image::ft_brightness(float degree)
{
    this->myimg.convertTo(this->modified, -1, degree, 0);
    this->allimages.push_back(this->modified.clone());
    this->mapimages.push_back(std::pair<cv::Mat , std::string>(this->modified.clone(),"Brightness"));


    this->aug = "Brightness";
}

void image::ft_shear(float right, float down)
{
    int h = this->myimg.rows;
    int w = this->myimg.cols;

    cv::Mat shear_matrix = (cv::Mat_<float>(2, 3) << 1, right, 0, down, 1, 0);

    int new_w = w + static_cast<int>(std::abs(right) * h);
    int new_h = h + static_cast<int>(std::abs(down) * w);

    cv::warpAffine(this->myimg, this->modified, shear_matrix, cv::Size(new_w, new_h), 0, 2);
    this->allimages.push_back(this->modified.clone());
    this->mapimages.push_back(std::pair<cv::Mat , std::string>(this->modified.clone(),"Shear"));

    // this->aug = "Shear";
}
void image::ft_noise(double stddev)
{
    cv::Mat noise(this->myimg.size(), this->myimg.type());
    cv::randn(noise, 0, stddev);
    this->modified = this->myimg + noise;
    this->allimages.push_back(this->modified.clone());
    this->mapimages.push_back(std::pair<cv::Mat , std::string>(this->modified.clone(),"noise"));

    // this->aug = ;
}

void image::ft_translate(int dx, int dy)
{
    cv::Mat t = (cv::Mat_<float>(2, 3) << 1, 0, dx, 0, 1, dy);
    cv::warpAffine(this->myimg, this->modified, t, this->myimg.size(),0,2);
    this->allimages.push_back(this->modified.clone());
    this->mapimages.push_back(std::pair<cv::Mat , std::string>(this->modified.clone(),"translate"));

    // this->aug = ;
}

image::params image::ft_randomize(image::augment what)
{

    switch (what)
    {
    case augment::shear:
    {
        std::uniform_real_distribution<float> shear_dist(-0.2f, 0.2f);
        return shear_dist(get_rng());
    }
    case augment::rotation:
    {
        std::uniform_int_distribution<int> rot_dist(-25, 25);
        return rot_dist(get_rng());
    }
    case augment::blur:
    {
        std::uniform_real_distribution<float> blur_dist(0.3f, 2.0f);
        return blur_dist(get_rng());
    }
    case augment::brightness:
    {
        std::uniform_real_distribution<float> bright_dist(0.6f, 1.4f);
        return bright_dist(get_rng());
    }
    case augment::scale:
    {
        std::uniform_real_distribution<float> scale_dist(0.8f, 1.2f);
        return scale_dist(get_rng());
    }
    case augment::flip:
    {
        std::uniform_int_distribution<int> flip_dist(0, 2);
        int flip_indeses[]{-1, 0, 1};
        return flip_indeses[flip_dist(get_rng())];
    }
    case augment::zoom:
    {
        std::uniform_real_distribution<float> zoom_dist(0.7f, 0.95f);
        return zoom_dist(get_rng());
    }
    case augment::translate:
    {
        std::uniform_int_distribution<int> rot_dist(-25, 25);
        return rot_dist(get_rng());
    }
    case augment::noise:
    {
        std::uniform_real_distribution<double> noise_dist(3.0, 15.0);
        return noise_dist(get_rng());
    }
    }

    return (0);
}

std::mt19937 &image::get_rng()
{
    thread_local std::mt19937 gen(std::random_device{}());
    return gen;
}

void image::ft_finalize()
{
    for (auto &img : this->allimages)
        cv::resize(img, img, cv::Size(this->width, this->height));
}

void image::ft_selection()
{
    
    // std::uniform_int_distribution<int> selection(0, 3);

    int needed; // ppcm
    std::shuffle(this->transformations.begin(),this->transformations.end(),get_rng());

    for (int i = 0; i < 5; i++)
    {
        this->transformations[i]();
    }

    saveimg(this->path);
    

    // this->transformations[0]();
    // this->transformations[2]();
    // this->transformations[1]();
    // this->transformations[5]();
    // this->transformations[4]();

    // std::cout << selection(get_rng()) << " " << noise << std ::endl;
}

void image::init()
{
    transformations.push_back([this]()
                              { ft_flip(std::get<int>(ft_randomize(augment::flip))); });
    transformations.push_back([this]()
                              { ft_rotation(std::get<int>(ft_randomize(augment::rotation))); });
    transformations.push_back([this]()
                              { ft_blur(std::get<float>(ft_randomize(augment::blur))); });
    transformations.push_back([this]()
                              { ft_brightness(std::get<float>(ft_randomize(augment::brightness))); });
    transformations.push_back([this]()
                              { ft_scale(std::get<float>(ft_randomize(augment::scale))); });
    transformations.push_back([this]()
                              { ft_flip(std::get<int>(ft_randomize(augment::flip))); });
    transformations.push_back([this]()
                              { ft_zoom(std::get<float>(ft_randomize(augment::zoom))); });
    transformations.push_back([this]()
                              { ft_shear(std::get<float>(ft_randomize(augment::shear)), std::get<float>(ft_randomize(augment::shear))); });
    transformations.push_back([this]()
                              { ft_translate(std::get<int>(ft_randomize(augment::translate)), std::get<int>(ft_randomize(augment::translate))); });
    transformations.push_back([this]()
                              { ft_noise(std::get<double>(ft_randomize(augment::noise))); });
}