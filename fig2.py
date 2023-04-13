import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def draw_mean_p():
    num_list = [0.0088, 0.0099, 0.0121, 0.0184, 0.0237, 0.0333, 0.0423, 0.0679, 0.0159]
    name_list = ["0.1-0.2", "0.2-0.3", "0.3-0.4", "0.4-0.5", "0.5-0.6", "0.6-0.7", "0.7-0.8", "0.8-0.9", "0.9-1.0"]
    plt.figure(figsize=(10, 7))
    bar = plt.bar(range(len(num_list)), num_list, tick_label=name_list)
    plt.bar_label(bar)
    plt.title("mean of P(r|c)", fontsize=15)
    plt.xlabel("similarity")
    plt.ylabel("mean of p(r|c)")
    plt.show()


def draw_hist_p(path, is_sample, num):
    data = pd.read_csv(path)
    if is_sample:
        data = data.sample(num)
    print(data.shape)
    similarity = data.loc[:, "similarity"]
    p = data.loc[:, "P(r|c)"]
    # similarity = np.array(similarity).tolist()
    p = np.array(p).tolist()
    # p = np.array(p)
    # p = np.mean(p)
    # print(p, type(p))

    plt.figure(figsize=(10, 7))
    plt.hist(p)
    plt.title("distribution of P(r|c) (0.8 < similarity <= 0.9)", fontsize=15)
    plt.ylabel("number")
    plt.xlabel("P(r|c)")
    plt.show()


if __name__ == "__main__":
    draw_mean_p()
    draw_hist_p("output/results-0.8-0.9.csv", 0, 0)

# 0.1-0.2 0.0088
# 0.2-0.3 0.0099
# 0.3-0.4 0.0121
# 0.4-0.5 0.0184
# 0.5-0.6 0.0237
# 0.6-0.7 0.0333
# 0.7-0.8 0.0423
# 0.8-0.9 0.0679
# 0.9-1.0 0.0159
