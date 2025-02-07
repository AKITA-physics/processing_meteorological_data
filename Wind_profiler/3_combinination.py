import pandas as pd
import numpy as np
import os

# パラメータ
year = 2020

for l in [str(year)+"_47406_47417_47423.send",str(year)+"_47585_47587_47590_47570.send",str(year)+"_47612_47640_47656.send",
                str(year)+"_47626_47629_47674.send",str(year)+"_47636_47663_47616.send",str(year)+"_47678_47795_47746.send",
                str(year)+"_47755_47893_47898.send",str(year)+"_47800_47805_47836_47912.send",str(year)+"_47819_47815_47822.send",
                str(year)+"_47848_47909_47945.send"]:
    
    # フォルダパスの獲得
    folder_path = "D:\\master_research\\高層データ\\"+l
        
    if l == str(year)+"_47406_47417_47423.send":
        list = [47406, 47417, 47423]
    elif l == str(year)+"_47585_47587_47590_47570.send":
        list = [47585, 47587, 47590, 47570]
    elif l == str(year)+"_47612_47640_47656.send":
        list = [47612, 47640, 47656]
    elif l == str(year)+"_47626_47629_47674.send":
        list = [47626, 47629, 47674]
    elif l == str(year)+"_47636_47663_47616.send":
        list = [47636, 47663, 47616]
    elif l == str(year)+"_47678_47795_47746.send":
        list = [47678, 47795, 47746]
    elif l == str(year)+"_47755_47893_47898.send":
        list = [47755, 47893, 47898]
    elif l == str(year)+"_47800_47805_47836_47912.send":
        list = [47800, 47805, 47836, 47912]
    elif l == str(year)+"_47819_47815_47822.send":
        list = [47819, 47815, 47822]
    elif l == str(year)+"_47848_47909_47945.send":
        list = [47848, 47909, 47945]
            
    for location in list:
        #地点によって観測高度変更
        if location in [47590, 47570]:
            list_height = [394, 690, 985, 1281, 1576, 1872, 2168, 2463, 2759, 3054]
        else:
            list_height = [291, 582, 873, 1164, 1455, 1747, 2038, 2329, 2620, 2911]

        for height in list_height:
            # データフレームの用意
            df_data_height = pd.DataFrame(columns = ["location","lat","lon","year","month","day","hour","minute","second","h_above_antenna","qc_info","u","v","w","snratio"])
            # フォルダ内のファイル一覧を取得
            file_list = os.listdir(folder_path)
            # 1月から順にファイルを開く
            for m in range(1,12+1):
                
                # file_listからファイルを取り出す
                for file_name in file_list:
                    
                    # 指定した特定の月の時のみ実行
                    if m < 10:
                        if file_name[23:25] == "0"+str(m):
                            # ファイルパスの指定
                            file_path = os.path.join(folder_path, file_name)
                            # CSVファイルのみ処理を実行
                            if file_name.endswith('.csv'):
                                # ファイルをDataFrameとして読み込み
                                df_original = pd.read_csv(file_path)
                                # 欠損値を示す数字をnp.nanに変換
                                df_original['u'] = df_original['u'].replace(8191.0, np.nan)
                                df_original["v"] = df_original["v"].replace(8191.0, np.nan)
                                df_original["w"] = df_original["w"].replace(8191.0, np.nan)
                                df_original["snratio"] = df_original["snratio"].replace(255, np.nan)

                                df_data = df_original[(df_original["location"] == location) & (df_original["h_above_antenna"] == height)].copy()

                                # インデックスナンバーをリセット
                                df_data = df_data.reset_index(drop=True)
                                # データフレームに追加
                                df_data_height = df_data_height._append(df_data, ignore_index=True)
                    else:
                        if file_name[23:25] == str(m):
                            # ファイルパスの指定
                            file_path = os.path.join(folder_path, file_name)
                            # CSVファイルのみ処理を実行
                            if file_name.endswith('.csv'):
                                # ファイルをDataFrameとして読み込み
                                df_original = pd.read_csv(file_path)
                                # 欠損値を示す数字をnp.nanに変換
                                df_original['u'] = df_original['u'].replace(8191.0, np.nan)
                                df_original["v"] = df_original["v"].replace(8191.0, np.nan)
                                df_original["w"] = df_original["w"].replace(8191.0, np.nan)
                                df_original["snratio"] = df_original["snratio"].replace(255, np.nan)

                                df_data = df_original[(df_original["location"] == location) & (df_original["h_above_antenna"] == height)].copy()
                                # インデックスナンバーをリセット
                                df_data = df_data.reset_index(drop=True)
                                # データフレームに追加
                                df_data_height = df_data_height._append(df_data, ignore_index=True)
                            
            # インデックスナンバーをリセット
            df_data_height = df_data_height.reset_index(drop=True)
            
            # 出力ファイルのパス
            output_path = os.path.join("D:\\master_research\\高層データ\\%04d_%05d"  %(year, location), '%04d_%05d_%03d.csv' %(year, location, height))
            # ファイルに書き出す
            df_data_height.to_csv(output_path, index=False)
            
            print(height, l, location)
