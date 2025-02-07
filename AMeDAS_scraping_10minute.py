#######################################################################################
# AMeDASの10分データを1年間スクレイピングするプログラム
#######################################################################################

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

########################## パラメータ ##########################
year = "スクレイピングする年"
block_no = "地点コード"
no = "府県コード"
output_folder_path = "出力先のフォルダー名"
output_filename = "出力ファイル名"

########################## 各月の月末日の定義 ##########################
def day_in_month(year, month):
    if month in [1,3,5,7,8,10,12]:
        return 31
    elif month in [4,6,9,11]:
        return 30
    elif month in [2] and year % 4 == 0:
        return 29
    elif month in [2] and year % 4 != 0:
        return 28

########################## スクレイピング ##########################
def scraping():
    #result.getの引数にURLを指定する
    result = requests.get(f"https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no={no}&block_no={block_no}&year={year}&month={month}&day={day}&view=")
    #1秒ごとにリクエストを送る
    time.sleep(1)

    #data_1t_0,data_0_1bをdata_0_0として処理
    content = result.content.decode("utf-8").replace('data_1t_0','data_0_0')#.replace('data_0_1b','data_0_0')
    #BeautifulSoupの処理に解析したい文字列(result.content)と処理の種類(html.parser)を指定
    soup = BeautifulSoup(content, 'html.parser')
    #class_=data_0_0の部分を全て取り出す
    all_data = soup.find_all(class_='data_0_0')

    return all_data

########################## データの整理 ##########################
def arrangement():
    #以降で用いるリスト作る
    list_data = []
    #新しい変数を置く
    count = 0

    #dfという変数で一行目の見出しを定義
    df_day = pd.DataFrame(columns =  ['hour','day','month','year','現地気圧','海面気圧','降水量','気温','相対湿度','平均風速','平均風向','最大瞬間風速','風向','日照時間'])

    #日ごとのデータに入れる
    for hour in range(1,144+1):
        #観測量データリストに追加する
        for t in range(10):
            list_data.append(all_data[count].text)
            count += 1
        #データフレームにkを追加し、df_monthに追加する
        list_data.insert(0, hour)
        list_data.insert(1, day)
        list_data.insert(2, month)
        list_data.insert(3, year)
        df_day.loc[hour-1] = list_data
        list_data = []
    
    return df_day


for month in range(1, 12+1):
    for day in range(1, day_in_month(year, month) + 1):
        all_data = scraping() # 指定したURLからスクレイピング
        df_day = arrangement() # データを整理
        
        # 各月のデータをまとめる
        if day == 1:
            df_month = df_day # 1日の場合は新しいファイルを作成
        else:
            df_month = pd.concat([df_month, df_day], ignore_index=True) # 2日以降の場合は既存のDataFrameに追加
               
    # 各年のデータをまとめる
    if month == 1:
        df_all = df_month # 1月の場合は新しいファイルを作成
    else:
        df_all = pd.concat([df_all, df_month], ignore_index=True) # 2月以降の場合は既存のDataFrameに追加

########################## ファイルの書き出し ##########################
output_path = os.path.join(output_folder_path, output_filename)
df_all.to_pickle(output_path)