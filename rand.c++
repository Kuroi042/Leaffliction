#include <iostream>
#include <random>
#include <numeric>

#include <iostream>
#include <vector>
#include <algorithm>

// using namespace std;

#include <vector>
#include <numeric>
#include <algorithm>
#include <random>
#include <iostream>

struct ClassStat {
    std::string name;
    int count;
};

void calculate_augmentation_schedule(const std::vector<ClassStat>& stats, int target_count) 
{
    std::mt19937 rng(std::random_device{}());

    for (const auto& item : stats) 
    {
        if (item.count >= target_count) {
            std::cout << item.name << ": Base = " << item.count 
                      << " | Augmentations needed = 0\n";
            continue;
        }

        int total_needed = target_count - item.count;
        int base_k = total_needed / item.count;
        int remainder = total_needed % item.count;

        // Vector tracking how many augmentations each real image gets
        std::vector<int> aug_counts(item.count, base_k);
        
        // Distribute remainder randomly among real images
        for (int i = 0; i < remainder; ++i) {
            aug_counts[i] += 1;
        }
        std::shuffle(aug_counts.begin(), aug_counts.end(), rng);

        // Count distribution breakdown for logging
        int high_count = base_k + 1;
        int low_count = base_k;
        int high_instances = remainder;
        int low_instances = item.count - remainder;

        std::cout << "[" << item.name << "]\n"
                  << "  Real images: " << item.count << " -> Target: " << target_count << "\n";
        if (high_instances > 0) {
            std::cout << "  - " << high_instances << " images get " << high_count << " augmentations\n";
        }
        if (low_instances > 0) {
            std::cout << "  - " << low_instances << " images get " << low_count << " augmentations\n";
        }
        std::cout << "  Total generated = " << total_needed << "\n\n";
    }
}

int main()
{

    std::vector<ClassStat> dataset = {
    {"Apple_Black_rot", 620},
    {"Apple_healthy", 1640},
    {"Apple_rust", 275},
    {"Apple_scab", 629}
};

// calculate_augmentation_schedule(dataset, 1990);
// exit(0);
    std::random_device rd;
    std::mt19937 gen(rd());

    std::uniform_int_distribution<> randomnub(-10,5);
    std::uniform_real_distribution<float> randomfnub(0.5f,0.0f);
    std::pair<float,float> shear(randomfnub(gen),randomfnub(gen)); 
    std::uniform_real_distribution<float> blur(0.3f,2.0f);

    std::uniform_int_distribution<> functionss(0,8);
    std::uniform_int_distribution<> rnd_selection(2,3);

    int fn[] = {0,1,2,3,4,5,6,7,8};



    int a = 620 ;
    int b = 1640 ;
    int c = 275 ;
    int d = 629 ;

    // int ints[] =  {a*0.80 , b*0.80,c*0.80,d*0.80};
    // int needed = 0;

    
    
    // int mean  = (a+b+c+d)/4;
    // int selection = 0;
    
    // for (int i = 0; i < 4; i++)
    // {
    //     needed = abs(ints[i] - mean);

    //     while (needed > 0)
    //     {

            
    //         selection = rnd_selection(gen);
    //         if (needed < selection)
    //         {
    //             selection = needed;
    //             /* code */
    //         }
    //         /* code */
    //         if (selection == 2 )
    //         {
    //             std::cout << "khdit "<< selection << " homa "<< fn[functionss(gen)] << " o  "<< fn[functionss(gen)] <<" o ba9i " << needed << std::endl;

    //         }
    //         else 
    //         {
    //             std::cout << "khdit "<< selection << " homa "<< fn[functionss(gen)] << " o  "<< fn[functionss(gen)] <<  " o  "<< fn[functionss(gen)] <<" o ba9i " << needed << std::endl;

    //         }
            
            
    //         needed -= selection ;
    //     }
        
    //         // int selection

        

    // }
    // int a_need = abs(a-mean);




    // // int max = max()
    // // auto _ 

    // // std::cout << std::lcm(620,std::lcm(1640,std::lcm(275,629))) << std::endl;
    // std::cout << mean << " " << a_need << " " << std::gcd(mean,a_need) << std::endl;

    int real = 275; 
    int target = 1640; // max
    int needed = target - real ; 
    int distribution  = needed / real;
    int chyata = needed % real;
    

    std::cout << distribution << " chyata " << chyata  << std::endl;


}