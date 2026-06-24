
#include "class.hpp"

#define VERTICAL_FLIP 1
#define HORIZONTAL_FLIP 0
#define BOTH_FLIP -1


// [[Rcpp::plugins(cpp17)]]


int onlycpp(std::string towrite)
{
    std::cout << "c++ wrote " << towrite << std::endl;
    return(0);
}



// [[Rcpp::export]]
int cppmain(std::string fromR , Rcpp::List folders_list)
{


    Rcpp::print(folders_list.names());

    Rcpp::StringVector files_diali = folders_list[0];

    Rcpp::StringVector folders_diali = folders_list.names();


    // onlycpp(Rcpp::as<std::string>(files_diali[1]));

    std::string foldername = Rcpp::as<std::string>(folders_diali[0]);
    std::string filename = Rcpp::as<std::string>(files_diali[3]);

    onlycpp(foldername);
    onlycpp(filename);


    // cv::Mat myimg = cv::imread(files_diali[1]);

    image obj(filename,foldername);


    // obj.ft_noise(15);
    // obj.ft_rotation(-30);
    // obj.ft_blur(2.0);
    // obj.ft_scale(0.7f);
    // obj.ft_scale(1.7f);
    // obj.ft_scale(0.2f);

    // obj.ft_flip(VERTICAL_FLIP);
    // obj.ft_zoom(0.8f); 
    // obj.ft_brightness(0.3f);

    // obj.ft_shear(std::get<float>(obj.ft_randomize(image::augment::shear)),std::get<float>(obj.ft_randomize(image::augment::shear)));
    // obj.ft_shear(std::get<float>(obj.ft_randomize(image::augment::shear)),std::get<float>(obj.ft_randomize(image::augment::shear)));
    // obj.ft_shear(std::get<float>(obj.ft_randomize(image::augment::shear)),std::get<float>(obj.ft_randomize(image::augment::shear)));
    // obj.ft_shear(std::get<float>(obj.ft_randomize(image::augment::shear)),std::get<float>(obj.ft_randomize(image::augment::shear)));
    // obj.ft_shear(std::get<float>(obj.ft_randomize(image::augment::shear)),std::get<float>(obj.ft_randomize(image::augment::shear)));
    // obj.ft_shear(std::get<float>(obj.ft_randomize(image::augment::shear)),std::get<float>(obj.ft_randomize(image::augment::shear)));
    
    // obj.ft_flip(std::get<int>(obj.ft_randomize(image::augment::flip)));
    // obj.ft_flip(std::get<int>(obj.ft_randomize(image::augment::flip)));
    // obj.ft_flip(std::get<int>(obj.ft_randomize(image::augment::flip)));
    // obj.ft_flip(std::get<int>(obj.ft_randomize(image::augment::flip)));
    // obj.ft_flip(std::get<int>(obj.ft_randomize(image::augment::flip)));
    // obj.ft_flip(std::get<int>(obj.ft_randomize(image::augment::flip)));
    // obj.ft_flip(std::get<int>(obj.ft_randomize(image::augment::flip)));


    // obj.ft_selection();
    // obj.ft_selection();
    // obj.ft_selection();
    // obj.ft_selection();


    // obj.ft_rotation(std::get<int>(obj.ft_randomize(image::augment::rotation)));
    // obj.ft_rotation(std::get<int>(obj.ft_randomize(image::augment::rotation)));
    // obj.ft_rotation(std::get<int>(obj.ft_randomize(image::augment::rotation)));
    // obj.ft_rotation(std::get<int>(obj.ft_randomize(image::augment::rotation)));
    // obj.ft_rotation(std::get<int>(obj.ft_randomize(image::augment::rotation)));
    // obj.ft_rotation(std::get<int>(obj.ft_randomize(image::augment::rotation)));
    // obj.ft_rotation(std::get<int>(obj.ft_randomize(image::augment::rotation)));
    
    // obj.ft_shear(obj.ft_randomize(image::augment::shear),obj.ft_randomize(image::augment::shear));
    // obj.ft_shear(obj.ft_randomize(image::augment::shear),obj.ft_randomize(image::augment::shear));
    // obj.ft_shear(obj.ft_randomize(image::augment::shear),obj.ft_randomize(image::augment::shear));
    // obj.ft_shear(obj.ft_randomize(image::augment::shear),obj.ft_randomize(image::augment::shear));
    // obj.ft_shear(obj.ft_randomize(image::augment::shear),obj.ft_randomize(image::augment::shear));
    // obj.ft_shear(obj.ft_randomize(image::augment::shear),obj.ft_randomize(image::augment::shear));
    // obj.ft_shear(obj.ft_randomize(image::augment::shear),obj.ft_randomize(image::augment::shear));
    // obj.ft_shear(obj.ft_randomize("shear"),obj.ft_randomize("shear"));
    // obj.ft_shear(obj.ft_randomize("shear"),obj.ft_randomize("shear"));
    // obj.ft_shear(obj.ft_randomize("shear"),obj.ft_randomize("shear"));
    // obj.ft_shear(obj.ft_randomize("shear"),obj.ft_randomize("shear"));
    // obj.ft_shear(obj.ft_randomize("shear"),obj.ft_randomize("shear"));

    // obj.saveimg(filename);
    obj.ft_selection();
    obj.summary();

    



    return(1);
}


