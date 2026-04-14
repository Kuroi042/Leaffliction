import os
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
def createBar(data : dict):
    plt.figure(figsize=(10, 5))

    df = pd.DataFrame(list(data.items()), columns=["Class", "Count"])
    print(df.head())
    plt.subplot(1, 2, 1)
    plt.pie(df.Count , labels = df.Class )
    plt.title("Pie Chart")

    plt.subplot(1, 2, 2)
    plt.bar(df["Class"],df["Count"], color='skyblue')
    plt.title("bar Chart")
    plt.tight_layout()
    plt.show()  


def ft_load(text :str):
    data = {}
    for root, dirs, files in os.walk("Apple"):
            if len(files) == 0:
                continue
            value =  len(files)
            key= root.split('/')[1]
            data[key]=value
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
 