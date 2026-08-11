
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
int cppmain(Rcpp::IntegerVector fromR , Rcpp::List folders_list)
{

    // std::cout << folders_list[0].names() << std::endl;
    // Rcpp::print(folders_list.names());
    // exit(0);
    CharacterVector R = fromR.names();


    for (int i = 0; i < fromR.size(); i++)
    {
        std::cout << R[i] << " " << fromR[i] << std::endl;
        /* code */
    }
    
    
    Rcpp::StringVector files_diali = folders_list[0];

    // std::cout  <<  folders_list[0];
    
    Rcpp::StringVector folders_diali = folders_list.names();
    
    // for (int i = 0; i < folders_diali.size(); i++)
    // {

    //     for (int j = 0; j < files_diali.size(); j++)
    //     {
    //         std::cout << files_diali[j] << std::endl;
    //     }
        
    // }
    
    
    // onlycpp(Rcpp::as<std::string>(files_diali[1]));
    
    std::string foldername = Rcpp::as<std::string>(folders_diali[0]);
    std::string filename = Rcpp::as<std::string>(files_diali[3]);
    int count = fromR[0]; 
    
    onlycpp(foldername);
    onlycpp(filename);
    std::cout << count << std::endl;


    // cv::Mat myimg = cv::imread(files_diali[1]);

    image obj(filename,foldername,count);


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


