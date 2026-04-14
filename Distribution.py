import os
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
def createBar(data : dict):
    df = pd.DataFrame(list(data.items()), columns=["Class", "Count"])
    print(df.head())
    plt.pie(df.)
    plt.bar(df["Class"],df["Count"], color='skyblue')
    plt.show()  


def ft_load(text :str):
    data = {}
    for root, dirs, files in os.walk("Apple"):
            if len(files) == 0:
                continue
            value =  len(files)
            key= root.split('/')[1]
            # print("Folders inside" ,root , count)
            # print(key.split('/')[1] ,":",value)
            data[key]=value
            # print(key , value)
    createBar(data)

def main():
    try:
          assert len(sys.argv) ==2 ,"the arguments are bad"
    except AssertionError as e:
        print(f"AssertionError: {e}")
    path = str(sys.argv)
    ft_load(path)


if __name__ ==  "__main__":
     main()
 