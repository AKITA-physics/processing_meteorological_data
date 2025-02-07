import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# パラメータ
year_check = 2020

# 月から月末日を産出する関数
def month_day(month):
    if month in [1,3,5,7,8,10,12]:
        last_day = 31
    elif month in [4,6,9,11]:
        last_day = 30
    elif month in [2]:
        last_day = 28
    return last_day

#うるう年の判定
if year_check % 4 == 0:
    all_day = 366
    feb_day = 29
else:
    all_day = 365
    feb_day = 28

# ----------------------------------------------------------データのダウンロード-----------------------------------------------------------------
for location in [47406, 47417, 47423, 47585, 47587, 47590, 47570, 47612, 47640, 47656, 47626, 47629, 47674, 47636, 47663, 47616, 
                 47678, 47795, 47746, 47755, 47893, 47898, 47800, 47805, 47836, 47912, 47819, 47815, 47822, 47848, 47909, 47945]:
    if location in [47590, 47570]:
        list_height = [394, 690, 985, 1281, 1576, 1872, 2168, 2463, 2759, 3054]
    else:
        list_height = [291, 582, 873, 1164, 1455, 1747, 2038, 2329, 2620, 2911]
    
    for height in list_height:
        df_original = pd.read_csv("D:\\master_research\\高層データ\\"+str(year_check)+"_"+str(location)+"\\"+str(year_check)+"_"+str(location)+"_"+str(height)+"_fill.csv")

        # 新しいデータフレームの作成
        df_data = pd.DataFrame(columns = ['year','month','day','hour','minute','u','v','w'])
        # 必要なデータだけ入れる
        df_data['year'] = df_original['year']
        df_data['month'] = df_original['month']
        df_data['day'] = df_original['day']
        df_data['hour'] = df_original['hour']
        df_data['minute'] = df_original['minute']
        df_data['u'] = df_original['u']
        df_data['v'] = df_original['v']
        df_data['w'] = df_original['w']
        # ---------------------------------------------1カ月の時間ごとの平均風速をdf_averageにまとめる--------------------------------------------------
        # 新しいデータフレームの作成
        df_average = pd.DataFrame(columns = ['year','month','hour','minute'])
        current_time = datetime(year=year_check-1, month=12, day=31, hour=23, minute=10)

        # 日時データをdf_averageに追加
        for i in range(144*all_day):
            df_average = df_average._append({
                'year': current_time.year,
                'month': current_time.month,
                'day': current_time.day,
                'hour': current_time.hour,
                'minute': current_time.minute,
            }, ignore_index=True)
            current_time = current_time + timedelta(minutes=10)

        # 風速のカラムの列を月ごとに日数×144の行列へ分解
        split_mean_u_1 = pd.DataFrame(np.reshape(df_data.loc[0:144*31-1,'u'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_v_1 = pd.DataFrame(np.reshape(df_data.loc[0:144*31-1,'v'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_w_1 = pd.DataFrame(np.reshape(df_data.loc[0:144*31-1,'w'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_u_2 = pd.DataFrame(np.reshape(df_data.loc[144*31:144*(31+feb_day)-1,'u'].values, (feb_day, 144)), columns =  [str(i) for i in range(144)])
        split_mean_v_2 = pd.DataFrame(np.reshape(df_data.loc[144*31:144*(31+feb_day)-1,'v'].values, (feb_day, 144)), columns =  [str(i) for i in range(144)])
        split_mean_w_2 = pd.DataFrame(np.reshape(df_data.loc[144*31:144*(31+feb_day)-1,'w'].values, (feb_day, 144)), columns =  [str(i) for i in range(144)])
        split_mean_u_3 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day):144*(31+feb_day+31)-1,'u'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_v_3 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day):144*(31+feb_day+31)-1,'v'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_w_3 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day):144*(31+feb_day+31)-1,'w'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_u_4 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31):144*(31+feb_day+31+30)-1,'u'].values, (30, 144)), columns =  [str(i) for i in range(144)])
        split_mean_v_4 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31):144*(31+feb_day+31+30)-1,'v'].values, (30, 144)), columns =  [str(i) for i in range(144)])
        split_mean_w_4 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31):144*(31+feb_day+31+30)-1,'w'].values, (30, 144)), columns =  [str(i) for i in range(144)])
        split_mean_u_5 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30):144*(31+feb_day+31+30+31)-1,'u'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_v_5 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30):144*(31+feb_day+31+30+31)-1,'v'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_w_5 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30):144*(31+feb_day+31+30+31)-1,'w'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_u_6 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31):144*(31+feb_day+31+30+31+30)-1,'u'].values, (30, 144)), columns =  [str(i) for i in range(144)])
        split_mean_v_6 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31):144*(31+feb_day+31+30+31+30)-1,'v'].values, (30, 144)), columns =  [str(i) for i in range(144)])
        split_mean_w_6 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31):144*(31+feb_day+31+30+31+30)-1,'w'].values, (30, 144)), columns =  [str(i) for i in range(144)])
        split_mean_u_7 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30):144*(31+feb_day+31+30+31+30+31)-1,'u'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_v_7 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30):144*(31+feb_day+31+30+31+30+31)-1,'v'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_w_7 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30):144*(31+feb_day+31+30+31+30+31)-1,'w'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_u_8 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31):144*(31+feb_day+31+30+31+30+31+31)-1,'u'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_v_8 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31):144*(31+feb_day+31+30+31+30+31+31)-1,'v'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_w_8 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31):144*(31+feb_day+31+30+31+30+31+31)-1,'w'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_u_9 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31+31):144*(31+feb_day+31+30+31+30+31+31+30)-1,'u'].values, (30, 144)), columns =  [str(i) for i in range(144)])
        split_mean_v_9 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31+31):144*(31+feb_day+31+30+31+30+31+31+30)-1,'v'].values, (30, 144)), columns =  [str(i) for i in range(144)])
        split_mean_w_9 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31+31):144*(31+feb_day+31+30+31+30+31+31+30)-1,'w'].values, (30, 144)), columns =  [str(i) for i in range(144)])
        split_mean_u_10 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31+31+30):144*(31+feb_day+31+30+31+30+31+31+30+31)-1,'u'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_v_10 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31+31+30):144*(31+feb_day+31+30+31+30+31+31+30+31)-1,'v'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_w_10 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31+31+30):144*(31+feb_day+31+30+31+30+31+31+30+31)-1,'w'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_u_11 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31+31+30+31):144*(31+feb_day+31+30+31+30+31+31+30+31+30)-1,'u'].values, (30, 144)), columns =  [str(i) for i in range(144)])
        split_mean_v_11 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31+31+30+31):144*(31+feb_day+31+30+31+30+31+31+30+31+30)-1,'v'].values, (30, 144)), columns =  [str(i) for i in range(144)])
        split_mean_w_11 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31+31+30+31):144*(31+feb_day+31+30+31+30+31+31+30+31+30)-1,'w'].values, (30, 144)), columns =  [str(i) for i in range(144)])
        split_mean_u_12 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31+31+30+31+30):144*(31+feb_day+31+30+31+30+31+31+30+31+30+31)-1,'u'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_v_12 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31+31+30+31+30):144*(31+feb_day+31+30+31+30+31+31+30+31+30+31)-1,'v'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        split_mean_w_12 = pd.DataFrame(np.reshape(df_data.loc[144*(31+feb_day+31+30+31+30+31+31+30+31+30):144*(31+feb_day+31+30+31+30+31+31+30+31+30+31)-1,'w'].values, (31, 144)), columns =  [str(i) for i in range(144)])
        # 時間ごとに平均をとる
        split_mean_u_1 = split_mean_u_1.mean()
        split_mean_v_1 = split_mean_v_1.mean()
        split_mean_w_1 = split_mean_w_1.mean()
        split_mean_u_2 = split_mean_u_2.mean()
        split_mean_v_2 = split_mean_v_2.mean()
        split_mean_w_2 = split_mean_w_2.mean()
        split_mean_u_3 = split_mean_u_3.mean()
        split_mean_v_3 = split_mean_v_3.mean()
        split_mean_w_3 = split_mean_w_3.mean()
        split_mean_u_4 = split_mean_u_4.mean()
        split_mean_v_4 = split_mean_v_4.mean()
        split_mean_w_4 = split_mean_w_4.mean()
        split_mean_u_5 = split_mean_u_5.mean()
        split_mean_v_5 = split_mean_v_5.mean()
        split_mean_w_5 = split_mean_w_5.mean()
        split_mean_u_6 = split_mean_u_6.mean()
        split_mean_v_6 = split_mean_v_6.mean()
        split_mean_w_6 = split_mean_w_6.mean()
        split_mean_u_7 = split_mean_u_7.mean()
        split_mean_v_7 = split_mean_v_7.mean()
        split_mean_w_7 = split_mean_w_7.mean()
        split_mean_u_8 = split_mean_u_8.mean()
        split_mean_v_8 = split_mean_v_8.mean()
        split_mean_w_8 = split_mean_w_8.mean()
        split_mean_u_9 = split_mean_u_9.mean()
        split_mean_v_9 = split_mean_v_9.mean()
        split_mean_w_9 = split_mean_w_9.mean()
        split_mean_u_10 = split_mean_u_10.mean()
        split_mean_v_10 = split_mean_v_10.mean()
        split_mean_w_10 = split_mean_w_10.mean()
        split_mean_u_11 = split_mean_u_11.mean()
        split_mean_v_11 = split_mean_v_11.mean()
        split_mean_w_11 = split_mean_w_11.mean()
        split_mean_u_12 = split_mean_u_12.mean()
        split_mean_v_12 = split_mean_v_12.mean()
        split_mean_w_12 = split_mean_w_12.mean()
        
        # その月の日分長くする
        split_mean_u_1 = np.tile(split_mean_u_1, 31)
        split_mean_v_1 = np.tile(split_mean_v_1, 31)
        split_mean_w_1 = np.tile(split_mean_w_1, 31)
        split_mean_u_2 = np.tile(split_mean_u_2, feb_day)
        split_mean_v_2 = np.tile(split_mean_v_2, feb_day)
        split_mean_w_2 = np.tile(split_mean_w_2, feb_day)
        split_mean_u_3 = np.tile(split_mean_u_3, 31)
        split_mean_v_3 = np.tile(split_mean_v_3, 31)
        split_mean_w_3 = np.tile(split_mean_w_3, 31)
        split_mean_u_4 = np.tile(split_mean_u_4, 30)
        split_mean_v_4 = np.tile(split_mean_v_4, 30)
        split_mean_w_4 = np.tile(split_mean_w_4, 30)
        split_mean_u_5 = np.tile(split_mean_u_5, 31)
        split_mean_v_5 = np.tile(split_mean_v_5, 31)
        split_mean_w_5 = np.tile(split_mean_w_5, 31)
        split_mean_u_6 = np.tile(split_mean_u_6, 30)
        split_mean_v_6 = np.tile(split_mean_v_6, 30)
        split_mean_w_6 = np.tile(split_mean_w_6, 30)
        split_mean_u_7 = np.tile(split_mean_u_7, 31)
        split_mean_v_7 = np.tile(split_mean_v_7, 31)
        split_mean_w_7 = np.tile(split_mean_w_7, 31)
        split_mean_u_8 = np.tile(split_mean_u_8, 31)
        split_mean_v_8 = np.tile(split_mean_v_8, 31)
        split_mean_w_8 = np.tile(split_mean_w_8, 31)
        split_mean_u_9 = np.tile(split_mean_u_9, 30)
        split_mean_v_9 = np.tile(split_mean_v_9, 30)
        split_mean_w_9 = np.tile(split_mean_w_9, 30)
        split_mean_u_10 = np.tile(split_mean_u_10, 31)
        split_mean_v_10 = np.tile(split_mean_v_10, 31)
        split_mean_w_10 = np.tile(split_mean_w_10, 31)
        split_mean_u_11 = np.tile(split_mean_u_11, 30)
        split_mean_v_11 = np.tile(split_mean_v_11, 30)
        split_mean_w_11 = np.tile(split_mean_w_11, 30)
        split_mean_u_12 = np.tile(split_mean_u_12, 31)
        split_mean_v_12 = np.tile(split_mean_v_12, 31)
        split_mean_w_12 = np.tile(split_mean_w_12, 31)
        
        # 平均データを一つにまとめる
        split_mean_u = np.concatenate((split_mean_u_1, split_mean_u_2, split_mean_u_3, split_mean_u_4, 
                                    split_mean_u_5, split_mean_u_6, split_mean_u_7, split_mean_u_8, 
                                    split_mean_u_9, split_mean_u_10, split_mean_u_11, split_mean_u_12))
        split_mean_v = np.concatenate((split_mean_v_1, split_mean_v_2, split_mean_v_3, split_mean_v_4, 
                                    split_mean_v_5, split_mean_v_6, split_mean_v_7, split_mean_v_8,
                                    split_mean_v_9, split_mean_v_10, split_mean_v_11, split_mean_v_12))
        split_mean_w = np.concatenate((split_mean_w_1, split_mean_w_2, split_mean_w_3, split_mean_w_4, 
                                    split_mean_w_5, split_mean_w_6, split_mean_w_7, split_mean_w_8, 
                                    split_mean_w_9, split_mean_w_10, split_mean_w_11, split_mean_w_12))
        # df_averageに追加
        df_average['average_u'] = split_mean_u
        df_average['average_v'] = split_mean_v
        df_average['average_w'] = split_mean_w
        
        #df_averageをファイルとして出力
        # 出力ファイルのパス
        output_path = os.path.join("D:\\master_research\\高層データ\\%04d_%05d"  %(year_check, int(location)), '%04d_%05d_%03d_average_data.csv' %(year_check, int(location), height))
        # ファイルに書き出す
        df_average.to_csv(output_path, index=False)
        
        # df_dataの列の長さ
        N = len(df_data)
        # カラム'mean'の欠損値の個数
        missing_num = df_data['u'].isnull().sum()
        # カラム'mean'の欠損率
        missing_rate = (missing_num / N) * 100
        #欠損率を出力
        print(missing_rate)
        #欠損したデータを出力
        # df_data.to_csv('df_data_output.csv')#, index=False)
        #-----------------------------------------------------------'u'に関して補間を行う------------------------------------------------------------------
        # 連続する np.nan の範囲を取得する処理
        nan_ranges = []
        start_nan_index = None
        nan_count = 0
        for index, value in df_data['u'].items():
            if pd.isna(value):
                if nan_count == 0:
                    start_nan_index = index
                nan_count = nan_count + 1
            else:
                if nan_count > 0:
                    nan_ranges.append((start_nan_index, index - 1))
                    nan_count = 0
        if nan_count > 0:
                    nan_ranges.append((start_nan_index, len(df_data) - 1))

        # np.nanが含まれている場合
        if len(nan_ranges) > 0:
            for i, (start, end) in enumerate(nan_ranges):

                # データフレームの生成
                newframe = pd.DataFrame(columns=["linear","average_u","linear_average"])
                if start == 0:
                    df_data['u'][start:end+1] = df_average['average_u'][start:end+1]
                elif end == len(df_data)-1:
                    df_data['u'][start:end+1] = df_average['average_u'][start:end+1]
                else:
                    # -----------------------------------------補間する---------------------------------------------------
                    # df_dataの欠損部分を線形補間してnewframeに代入
                    newframe["linear"] = df_data.iloc[start-1:end+1+1, df_data.columns.get_loc('u')].interpolate()
                    # インデックスナンバーをリセット
                    newframe = newframe.reset_index(drop=True)
                        
                    # df_averageの指定された行をnewframeに代入
                    newframe_average = df_average['average_u'][start-1:end+1+1]
                    # インデックスナンバーをリセット
                    newframe_average = newframe_average.reset_index(drop=True)
                    newframe["average_u"] =newframe_average

                    # 特定の値をnp.nanに置き換える
                    newframe_average[1:end+1] = np.nan
                    # np.nanにしたところを線形補間
                    newframe_linear_average = newframe_average.interpolate()
                    # newframeに代入
                    newframe["linear_average"] = newframe_linear_average
                            
                    #newframeの端をけずる（欠損値のみを扱うため）
                    newframe = newframe[1:len(newframe)-1]

                    # 元データの線形補完に平均データの変動を加える
                    df_data.iloc[start:end+1, df_data.columns.get_loc('u')]\
                        = newframe["linear"]+newframe["average_u"]-newframe["linear_average"]              
        #-----------------------------------------------------------'v'に関して補間を行う------------------------------------------------------------------
        # 連続する np.nan の範囲を取得する処理
        nan_ranges = []
        start_nan_index = None
        nan_count = 0
        for index, value in df_data['v'].items():
            if pd.isna(value):
                if nan_count == 0:
                    start_nan_index = index
                nan_count = nan_count + 1
            else:
                if nan_count > 0:
                    nan_ranges.append((start_nan_index, index - 1))
                    nan_count = 0
        if nan_count > 0:
                    nan_ranges.append((start_nan_index, len(df_data) - 1))

        # np.nanが含まれている場合
        if len(nan_ranges) > 0:
            for i, (start, end) in enumerate(nan_ranges):

                # データフレームの生成
                newframe = pd.DataFrame(columns=["linear","average_v","linear_average"])
                if start == 0:
                    df_data['v'][start:end+1] = df_average['average_v'][start:end+1]
                elif end == len(df_data)-1:
                    df_data['v'][start:end+1] = df_average['average_v'][start:end+1]
                else:
                    # -----------------------------------------補間する---------------------------------------------------
                    # df_dataの欠損部分を線形補間してnewframeに代入
                    newframe["linear"] = df_data.iloc[start-1:end+1+1, df_data.columns.get_loc('v')].interpolate()
                    # インデックスナンバーをリセット
                    newframe = newframe.reset_index(drop=True)
                        
                    # df_averageの指定された行をnewframeに代入
                    newframe_average = df_average['average_v'][start-1:end+1+1]
                    # インデックスナンバーをリセット
                    newframe_average = newframe_average.reset_index(drop=True)
                    newframe["average_v"] =newframe_average

                    # 特定の値をnp.nanに置き換える
                    newframe_average[1:end+1] = np.nan
                    # np.nanにしたところを線形補間
                    newframe_linear_average = newframe_average.interpolate()
                    # newframeに代入
                    newframe["linear_average"] = newframe_linear_average
                            
                    #newframeの端をけずる（欠損値のみを扱うため）
                    newframe = newframe[1:len(newframe)-1]

                    # 元データの線形補完に平均データの変動を加える
                    df_data.iloc[start:end+1, df_data.columns.get_loc('v')]\
                        = newframe["linear"]+newframe["average_v"]-newframe["linear_average"]
        #-----------------------------------------------------------'w'に関して補間を行う------------------------------------------------------------------
        # 連続する np.nan の範囲を取得する処理
        nan_ranges = []
        start_nan_index = None
        nan_count = 0
        for index, value in df_data['w'].items():
            if pd.isna(value):
                if nan_count == 0:
                    start_nan_index = index
                nan_count = nan_count + 1
            else:
                if nan_count > 0:
                    nan_ranges.append((start_nan_index, index - 1))
                    nan_count = 0
        if nan_count > 0:
                    nan_ranges.append((start_nan_index, len(df_data) - 1))

        # np.nanが含まれている場合
        if len(nan_ranges) > 0:
            for i, (start, end) in enumerate(nan_ranges):

                # データフレームの生成
                newframe = pd.DataFrame(columns=["linear","average_w","linear_average"])
                if start == 0:
                    df_data['w'][start:end+1] = df_average['average_w'][start:end+1]
                elif end == len(df_data)-1:
                    df_data['w'][start:end+1] = df_average['average_w'][start:end+1]
                else:
                    # -----------------------------------------補間する---------------------------------------------------
                    # df_dataの欠損部分を線形補間してnewframeに代入
                    newframe["linear"] = df_data.iloc[start-1:end+1+1, df_data.columns.get_loc('w')].interpolate()
                    # インデックスナンバーをリセット
                    newframe = newframe.reset_index(drop=True)
                        
                    # df_averageの指定された行をnewframeに代入
                    newframe_average = df_average['average_w'][start-1:end+1+1]
                    # インデックスナンバーをリセット
                    newframe_average = newframe_average.reset_index(drop=True)
                    newframe["average_w"] =newframe_average

                    # 特定の値をnp.nanに置き換える
                    newframe_average[1:end+1] = np.nan
                    # np.nanにしたところを線形補間
                    newframe_linear_average = newframe_average.interpolate()
                    # newframeに代入
                    newframe["linear_average"] = newframe_linear_average
                            
                    #newframeの端をけずる（欠損値のみを扱うため）
                    newframe = newframe[1:len(newframe)-1]

                    # 元データの線形補完に平均データの変動を加える
                    df_data.iloc[start:end+1, df_data.columns.get_loc('w')]\
                        = newframe["linear"]+newframe["average_w"]-newframe["linear_average"]

        # カラム'mean'の欠損値の個数
        missing_num = df_data['u'].isnull().sum()
        # カラム'mean'の欠損率
        missing_rate = (missing_num / N) * 100
        #欠損率を出力
        print(missing_rate)
        # np.nanが存在する行のインデックスを取得する
        # nan_indices = df_data.index[df_data['u'].isnull()]
        # print(nan_indices)
        # 出力ファイルのパス
        output_path = os.path.join("D:\\master_research\\高層データ\\%04d_%05d"  %(year_check, int(location)), '%04d_%05d_%03d_interpolation.csv' %(year_check, int(location), height))
        # ファイルに書き出す
        df_data.to_csv(output_path, index=False)
        
        print(location, height, len(df_data))

