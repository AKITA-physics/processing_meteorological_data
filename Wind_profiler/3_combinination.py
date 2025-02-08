############################################################################
# ウィンドプロファイラのデータを各年でまとめるコード
############################################################################

import pandas as pd
import numpy as np
import os

############################### パラメータ ###############################
year = 2020 # 処理する年
original_folder_path = "元データの入っているフォルダーパス"
output_folder_path = "出力先のフォルダーパス"
block_no_lists = {41: "47406_47417_47423", 
                  42: "47585_47587_47590_47570", 
                  43: "47626_47629_47674", 
                  44: "47612_47640_47656", 
                  45: "47636_47663_47616",
                  46: "47755_47893_47898",
                  47: "47819_47815_47822",
                  48: "47800_47805_47836_47912",
                  49: "47678_47795_47746",
                  50: "47848_47909_47945"}

########################################################################
for l in block_no_lists:
    block_no = block_no_lists[l]
    list = [int(num) for num in block_no.split('_')]
    
    # フォルダパスの獲得
    folder_path = f"{original_folder_path}\\{year}_{block_no}.send"
            
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
                    if file_name[23:25] == str(m).zfill(2):
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
            
            # ファイルの出力
            output_path = os.path.join(output_folder_path, f'{year}_{location}_{height}.csv')
            df_data_height.to_csv(output_path, index=False)
            
            # 進捗の出力
            print(height, l, location)
