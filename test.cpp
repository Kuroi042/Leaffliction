
#include "class.hpp"

#define VERTICAL_FLIP 1
#define HORIZONTAL_FLIP 0
#define BOTH_FLIP -1

// [[Rcpp::plugins(cpp17)]]

int onlycpp(std::string towrite)
{
    std::cout << "c++ wrote " << towrite << std::endl;
    return (0);
}

static void print_progress(int current, int total, const std::string &label)
{
    const int barWidth = 40;
    float progress = (total > 0) ? static_cast<float>(current) / total : 1.0f;
    int pos = static_cast<int>(barWidth * progress);

    Rcpp::Rcout << "\r[";
    for (int i = 0; i < barWidth; ++i)
        Rcpp::Rcout << (i < pos ? "=" : (i == pos ? ">" : " "));
    Rcpp::Rcout << "] " << current << "/" << total
                << " (" << static_cast<int>(progress * 100.0f) << "%) "
                << label << std::string(15, ' '); // pad so shorter labels overwrite longer ones
    R_FlushConsole();
}

// [[Rcpp::export]]
int cppmain(Rcpp::IntegerVector fromR, Rcpp::List folders_list, int target)
{

    CharacterVector R = fromR.names();
    Rcpp::StringVector folders_diali = folders_list.names();
    Rcpp::StringVector files_diali = folders_list[0];
    std::string foldername;
    std::string filename;

    if (R.size() == 1 && files_diali.size() == 1)
    {
        /* code */
        foldername = Rcpp::as<std::string>(folders_diali[0]);
        filename = Rcpp::as<std::string>(files_diali[0]);

        image obj(filename, foldername, 1);
        obj.ft_selection(0);
        obj.summary();
    }
    int total_files = 0;
    for (int i = 0; i < R.size(); i++)
    {
        Rcpp::StringVector tmp = folders_list[i];
        total_files += tmp.size();
    }
    int processed_files = 0;

    for (int i = 0; i < R.size(); i++) // folder number
    {
        files_diali = folders_list[i];
        int real_count = fromR[i];
        int needed = target - real_count;
        int distribution = needed / real_count; // Base per file
        int chyata = needed % real_count;       // Leftovers needing +1
        foldername = Rcpp::as<std::string>(folders_diali[i]);

        for (int j = 0; j < files_diali.size(); j++)
        {
            int to_aug = distribution;
            if (chyata > 0)
            {
                to_aug += 1;
                chyata--;
            }

            filename = Rcpp::as<std::string>(files_diali[j]);
            if (to_aug > 0)
            {
                image obj(filename, foldername, to_aug);
                obj.ft_selection(1);
            }
            else
                image::copy_original(filename);
            processed_files++;
            print_progress(processed_files, total_files, foldername);
            Rcpp::checkUserInterrupt(); // lets Ctrl+C in R actually stop long runs
        }
    }
    Rcpp::Rcout << std::endl; // move past the progress bar line once done


    int count = fromR[0];

    return (1);
}
