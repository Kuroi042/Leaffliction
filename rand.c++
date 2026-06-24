#include <iostream>
#include <random>
#include <numeric>

#include <iostream>
#include <vector>
#include <algorithm>

// using namespace std;



int main()
{
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

    int ints[] =  {a , b,c,d};
    int needed = 0;

    
    
    int mean  = (a+b+c+d)/4;
    int selection = 0;
    
    for (int i = 0; i < 4; i++)
    {
        needed = abs(ints[i] - mean);

        while (needed > 0)
        {

            
            selection = rnd_selection(gen);
            if (needed < selection)
            {
                selection = needed;
                /* code */
            }
            /* code */
            if (selection == 2 )
            {
                std::cout << "khdit "<< selection << " homa "<< fn[functionss(gen)] << " o  "<< fn[functionss(gen)] <<" o ba9i " << needed << std::endl;

            }
            else 
            {
                std::cout << "khdit "<< selection << " homa "<< fn[functionss(gen)] << " o  "<< fn[functionss(gen)] <<  " o  "<< fn[functionss(gen)] <<" o ba9i " << needed << std::endl;

            }
            
            
            needed -= selection ;
        }
        
            // int selection

        

    }
    int a_need = abs(a-mean);




    // int max = max()
    // auto _ 

    // std::cout << std::lcm(620,std::lcm(1640,std::lcm(275,629))) << std::endl;
    std::cout << mean << " " << a_need << " " << std::gcd(mean,a_need) << std::endl;

}