# データがない箇所に欠損値を代入
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# パラメータ
year_check = 2020

#うるう年の判定
if year_check % 4 == 0:
    all_day = 366
    feb_day = 29
else:
    all_day = 365
    feb_day = 28

#地点を選択
for location in [47406, 47417, 47423, 47585, 47587, 47590, 47570, 47612, 47640, 47656, 47626, 47629, 47674, 47636, 47663, 47616, 
                 47678, 47795, 47746, 47755, 47893, 47898, 47800, 47805, 47836, 47912, 47819, 47815, 47822, 47848, 47909, 47945]:
    #地点によって観測高度変更
    if location in [47590, 47570]:
        list_height = [394, 690, 985, 1281, 1576, 1872, 2168, 2463, 2759, 3054]
    else:
        list_height = [291, 582, 873, 1164, 1455, 1747, 2038, 2329, 2620, 2911]
        
    # 高度ごとに処理
    for height in list_height:
        df = pd.read_csv("D:\\master_research\\高層データ\\"+str(year_check)+"_"+str(location)+"\\"+str(year_check)+"_"+str(location)+"_"+str(height)+".csv")

        #各コラムの１行目の値
        lat = df.loc[0,"lat"]
        lon = df.loc[0,"lon"]
        h_above_antenna =df.loc[0,"h_above_antenna"]

        current_time = datetime(year=year_check-1, month=12, day=31, hour=23, minute=10)

        list_temp = []
        index_number = 0

        while index_number < len(df):
            i = df.iloc[index_number,:]
            if i["year"] == current_time.year and \
                i["month"] == current_time.month and \
                i["day"] == current_time.day and \
                i["hour"] == current_time.hour and \
                i["minute"] ==current_time.minute:
                    list_temp.append(i)
                    index_number = index_number + 1
            else:
                list_temp.append(pd.Series({"location": location,"lat": lat,"lon": lon,"year": current_time.year,
                                "month": current_time.month,"day": current_time.day,
                                "hour": current_time.hour,"minute": current_time.minute,
                                "second": 1.0,"h_above_antenna": h_above_antenna,"qc_info": 255,
                                "u": np.nan,"v": np.nan,"w": np.nan,"snratio": np.nan}))

            current_time = current_time + timedelta(minutes=10)
            
        df_temp = pd.DataFrame(list_temp)
            
        # インデックスナンバーをリセット
        df_temp = df_temp.reset_index(drop=True)
            
        #末尾が12月31日23時ではない場合の処理
        if df.loc[len(df)-1,'year'] != year_check or df.loc[len(df)-1,'month'] != 12.0 or df.loc[len(df)-1,'day'] != 31.0 or \
                    df.loc[len(df)-1,'hour'] != 23.0 or df.loc[len(df)-1,'minute'] != 0.0:
                            
            last_year = df.loc[len(df)-1,'year']
            last_month = df.loc[len(df)-1,'month']
            last_day = df.loc[len(df)-1,'day']
            last_hour = df.loc[len(df)-1,'hour']
            last_minute = df.loc[len(df)-1,'minute']
                
            current_time = datetime(year=last_year, month=last_month, day=last_day, hour=last_hour, minute=last_minute)
                
            for k in range(144*all_day):
                                
                current_time = current_time + timedelta(minutes=10)
                list_add = []
                list_add.append(pd.Series({"location": location,"lat": lat,"lon": lon,"year": current_time.year,
                                    "month": current_time.month,"day": current_time.day,
                                    "hour": current_time.hour,"minute": current_time.minute,
                                    "second": 1.0,"h_above_antenna": h_above_antenna,"qc_info": 255,
                                    "u": np.nan,"v": np.nan,"w": np.nan,"snratio": np.nan}))
                    
                df_add = pd.DataFrame(list_add)

                # df_tempにdf_addを末尾に追加
                df_temp = df_temp._append(df_add, ignore_index=True)
                    
                if len(df_temp) == 144*all_day:
                    break

        # インデックスナンバーをリセット
        df_temp = df_temp.reset_index(drop=True)

        print(location, height, len(df_temp))

        # 出力ファイルのパス
        output_path = os.path.join("D:\\master_research\\高層データ\\%04d_%05d"  %(year_check, location), '%04d_%05d_%03d_fill.csv' %(year_check, location, height))
        # ファイルに書き出す
        df_temp.to_csv(output_path, index=False)