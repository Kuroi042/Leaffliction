
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
int cppmain(Rcpp::IntegerVector fromR , Rcpp::List folders_list, int target)
{


    CharacterVector R = fromR.names();
    Rcpp::StringVector folders_diali = folders_list.names();
    Rcpp::StringVector files_diali = folders_list[0];
    std::string foldername;
    std::string filename;

    if (R.size() == 1 && files_diali.size() == 1 )
    {
        /* code */
            foldername = Rcpp::as<std::string>(folders_diali[0]);
            filename = Rcpp::as<std::string>(files_diali[0]);

       image obj(filename,foldername,1);
                obj.ft_selection(0);
                obj.summary();
    }
    


    for (int i = 0; i < R.size(); i++) // folder number
    {
        files_diali = folders_list[i];
        int real_count = fromR[i];
        // int test = needed_aug(fromR[i] , target);
        int needed = target - real_count;
        int distribution = needed / real_count; // Base per file
        int chyata = needed % real_count;       // Leftovers needing +1
        // std::vector<int> file_aug_counts(real_count, distribution);
        // for (int k = 0; k < chyata; ++k) {
            //     file_aug_counts[k] += 1;
            // }
            
            foldername = Rcpp::as<std::string>(folders_diali[i]);
            
            
            for (int j = 0; j < files_diali.size(); j++)
            {
            int to_aug = distribution;
            if (chyata > 0 )
            {
                to_aug += 1;
                chyata--;
            }
            
            filename = Rcpp::as<std::string>(files_diali[j]);
            // int file_aug_target = file_aug_counts[j];
            // std::cout << "target: " << test << " folder : "    << foldername << "file :" << filename << "count dialhom = " << fromR[i] << std::endl;
            // std::cout << "Folder: " << foldername 
            // << " | File: " << filename 
            // << " | Real total: " << real_count 
            // << " | Augmentations to make: " << to_aug
            // << std::endl;
            if (to_aug > 0)
            {
                image obj(filename,foldername,to_aug);
                obj.ft_selection(1);

                /* code */
            }
            


        }
        




    }
    // exit(0);
    

    int count = fromR[0]; 
    
    // onlycpp(foldername);
    // onlycpp(filename);



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
    // obj.ft_selection();
    // obj.summary();

    



    return(1);
}


