import numpy as np
import matplotlib.pyplot as plt

# 139/5000 0.0278 0.3 < similarity <= 0.4
# 323/5000 0.0646 0.4 < similarity <= 0.5
# 9070/53815 0.1685 0.5 < similarity <= 0.6
# 3695/11485 0.3217 0.6 < similarity <= 0.7
# 1178/3621 0.3253 0.7 < similarity <= 0.8
# 270/712 0.3792 0.8 < similarity <= 0.9
# 331/3248 0.1019 0.9 < similarity <= 1.0
if __name__ == "__main__":
    name_list = ["0.1-0.2", "0.2-0.3", "0.3-0.4", "0.4-0.5", "0.5-0.6", "0.6-0.7", "0.7-0.8", "0.8-0.9", "0.9-1.0"]
    num_list = [0.009, 0.018, 0.0278, 0.0646, 0.1685, 0.3217, 0.3253, 0.3792, 0.1019]
    plt.figure(figsize=(10,7))
    bar = plt.bar(range(len(num_list)), num_list, tick_label=name_list)
    plt.bar_label(bar)
    plt.title("pairs of words both in word2vec (nearby) and have association", fontsize=15)
    plt.xlabel("similarity")
    plt.ylabel("percentage")
    plt.show()
