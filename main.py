import sqlite3
import pandas as pd
import numpy as np
import csv
from random import sample
import pymysql


def reconstruct_table():
    data = pd.read_csv("SWOW-EN.R100.csv", dtype={"cue": str, "R1": str, "R2": str, "R3": str}, na_values="NA",
                       keep_default_na=False)
    data = data.loc[:, ["cue", "R1", "R2", "R3"]]
    data["cue"] = data["cue"].str.lower()
    data["R1"] = data["R1"].str.lower()
    data["R2"] = data["R2"].str.lower()
    data["R3"] = data["R3"].str.lower()
    data = data.sort_values(by="cue", ascending=True, key=lambda x: x.str.lower())
    print(data.shape)
    data = np.array(data).tolist()
    print(len(data))
    conn = sqlite3.connect("associate.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE swow")
    cursor.execute("CREATE TABLE swow (cue varchar(100), response varchar(100))")
    for i in range(1228200):
        for j in range(1, 4):
            cursor.execute("INSERT INTO swow VALUES(?, ?)", (data[i][0], data[i][j]))
    cursor.close()
    conn.commit()
    conn.close()


def search_df():
    data = pd.read_csv("SWOW-EN.R100.csv", dtype={"cue": str, "R1": str, "R2": str, "R3": str}, na_values="NA",
                       keep_default_na=False)
    data = data.loc[:, ["cue", "R1", "R2", "R3"]]
    data["cue"] = data["cue"].str.lower()
    data["R1"] = data["R1"].str.lower()
    data["R2"] = data["R1"].str.lower()
    data["R3"] = data["R1"].str.lower()
    tot = get_nearby()
    data = data.sort_values(by="cue", ascending=True, key=lambda x: x.str.lower())
    print(data.shape)
    data = np.array(data).tolist()
    print(len(data))
    for i in range(len(tot)):
        for j in range(len(data)):
            if data[j][0].lower() == tot[i][0].lower():
                if data[j][1].lower() == tot[i][1].lower() or data[j][2].lower() == tot[i][1].lower() or data[j][
                    3].lower() == tot[i][1].lower():
                    res = res + 1
        print(i)
    print(res)
    print(res / len(tot))


def get_nearby():
    conn = sqlite3.connect("word2vec.db")
    cursor = conn.cursor()
    tot = cursor.execute("SELECT word, neighbor, similarity FROM nearby")
    tot = tot.fetchall()
    # print(tot)
    cursor.close()
    conn.close()
    return tot


def get_top_similarity(word):
    conn = sqlite3.connect("word2vec.db")
    cursor = conn.cursor()
    top = cursor.execute("SELECT neighbor, similarity from nearby where word = ? order by similarity desc", (word,))
    top = top.fetchall()
    cursor.close()
    conn.close()
    return top


def get_top_p(word):
    conn = sqlite3.connect("associate.db")
    cursor = conn.cursor()
    top = cursor.execute("SELECT response, COUNT(*) FROM swow WHERE cue = ? group by response", (word, ))
    top = top.fetchall()
    cursor.close()
    cursor.close()
    top = sorted(top, key=lambda x: x[1], reverse=True)
    return top


def get_num(word, response):
    conn = sqlite3.connect("associate.db")
    cursor = conn.cursor()
    tot = cursor.execute("SELECT COUNT(*) FROM swow WHERE cue = ? and response = ?", (word, response))
    tot = tot.fetchall()
    cursor.close()
    conn.close()
    return tot[0][0]


def get_similarity(word, neighbor):
    conn = sqlite3.connect("word2vec.db")
    cursor = conn.cursor()
    tot = cursor.execute("SELECT similarity FROM nearby WHERE word = ? AND neighbor = ?", (word, neighbor))
    tot = tot.fetchall()
    cursor.close()
    conn.close()
    return tot


def write_csv():
    tot = get_nearby()
    header = ["word", "neighbor", "similarity"]
    with open("output/word2vec_nearby.csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(len(tot)):
            writer.writerow(tot[i])


def cal_p():
    res = 0
    tot = get_nearby()
    print(len(tot))
    if len(tot) > 5000:
        tot = sample(tot, 5000)
        print(len(tot))
    header = ["cue/word", "response/neighbor", "similarity", "P(r|c)"]
    conn = sqlite3.connect("associate.db")
    cursor = conn.cursor()
    with open("output/results-0.1-0.2.csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        # tmp = cursor.execute("Select * FROM swow where cue like '_% _%' or response like '_% _%' ")
        # cursor.execute("DELETE FROM swow where length(cue) < 2 or length(response) < 2")
        # print(tmp.fetchall())
        for i in range(len(tot)):
            result = []
            tmp = cursor.execute("SELECT COUNT(*) FROM swow WHERE cue=? and response=?",
                                 (tot[i][0].lower(), tot[i][1].lower()))
            # print(tmp.fetchall()[0][0])
            tmp = tmp.fetchall()

            if tmp[0][0] > 0:
                result.append(tot[i][0])
                result.append(tot[i][1])
                result.append(tot[i][2])
                cnt = tmp[0][0]
                tmp1 = cursor.execute("SELECT COUNT(*) FROM swow WHERE cue=?", (tot[i][0].lower(),))
                tmp1 = tmp1.fetchall()
                result.append(str(cnt / tmp1[0][0]))
                writer.writerow(result)
                print(i, end=" ")
                print(tot[i][0], tot[i][1], tot[i][2], end=" ")
                print(tmp[0][0], cnt / tmp1[0][0])
                res = res + 1
    cursor.close()
    conn.commit()
    conn.close()
    # # 697 0.1404 similarity>0.8
    # # 3870 0.92 cue中有word
    # 2853/8262 0.3453 0.65 < similarity < 0.95
    # 14240/69673 0.2044 0.5 < similarity < 0.95

    # 45/5000 0.009 0.1 < similarity <= 0.2
    # 90/5000 0.018 0.2 < similarity <= 0.3
    # 139/5000 0.0278 0.3 < similarity <= 0.4
    # 323/5000 0.0646 0.4 < similarity <= 0.5
    # 9070/53815 0.1685 0.5 < similarity <= 0.6
    # 3695/11485 0.3217 0.6 < similarity <= 0.7
    # 1178/3621 0.3253 0.7 < similarity <= 0.8
    # 270/712 0.3792 0.8 < similarity <= 0.9
    # 331/3248 0.1019 0.9 < similarity <= 1.0
    print(res)
    print(res / len(tot))


def write_mysql():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='20020909LMC',
                                 database='free association')
    conn = sqlite3.connect("word2vec.db")
    with connection:
        with connection.cursor() as cursor:
            sql = "CREATE TABLE IF NOT EXISTS nearby (word varchar(100), neighbor varchar(100), similarity DOUBLE);"
            cursor.execute(sql)
        connection.commit()

        with connection.cursor() as cursor:
            cursor1 = conn.cursor()
            res = cursor1.execute("SELECT * FROM nearby")
            res = res.fetchall()
            for i in range(len(res)):
                cursor.execute("INSERT INTO nearby VALUES (%s, %s, %s)", (res[i][0], res[i][1], res[i][2]))
                print(i)
            cursor1.close()
            conn.close()
        connection.commit()


if __name__ == '__main__':
    # top_p = get_top_p("apple")
    # # top_sim = get_top_similarity("apple")
    # for i in range(0, 10):
    #     # num = get_num("apple", top_sim[i][0])
    #     sim = get_similarity("apple", top_p[i][0])
    #     print(top_p[i][0], top_p[i][1], sim)
    # write_csv()
    # write_mysql()
    conn = sqlite3.connect("word2vec.db")
    cursor = conn.cursor()
    res = tot = cursor.execute("SELECT similarity from nearby where word='apple' and neighbor='apple'")
    print(res.fetchone())
