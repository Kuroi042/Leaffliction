import os
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
def createBar(data : dict , key:str):
    plt.figure(figsize=(15, 5) )
    df = pd.DataFrame(list(data.items()), columns=["Class", "Count"])
    print(df.head())
    plt.subplot(1, 2, 1)
    plt.pie(df.Count , labels = df.Class , autopct='%1.1f%%')
    plt.title(f"{key} Pie Chart")

    plt.subplot(1, 2, 2)
    plt.bar(df["Class"],df["Count"], color='skyblue')
    plt.title(f"{key} Bar Chart")
    plt.tight_layout()
    plt.suptitle(f"{key} class distribution")
    plt.show()  


def ft_load(text :str):
    data = {}
    for root, dirs, files in os.walk("Apple"):
            if len(files) == 0:
                continue
            value =  len(files)
            key= root.split('/')[1]
            data[key]=value
            key1 =  root.split('/')[0]
    createBar(data , key1)

def main():
    try:
          assert len(sys.argv) ==2 ,"the arguments are bad"
    except AssertionError as e:
        print(f"AssertionError: {e}")
    path = str(sys.argv)
    ft_load(path)


if __name__ ==  "__main__":
     main()
 