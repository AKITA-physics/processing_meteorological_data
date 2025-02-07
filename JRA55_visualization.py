############################################################################
# netcdf形式のJRA-55の等圧面データを開封し、グリッドデータを作成するプログラム
############################################################################

import xarray as xr
import numpy as np 
import pandas as pd
from datetime import datetime, timedelta
from geopy.distance import geodesic
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import metpy
import os
import sys
import cv2

################################ パラメータ ################################
year = "処理する年"
month = "処理する月"
data_folder_path = "NetCDF形式のJRA-55の入っているフォルダーパス"
level_p = "処理したい圧力面のレベル"
lat_max = 70 #抽出する最大緯度
lat_min = 10 #抽出する最大緯度
lon_max = 180 #抽出する最大経度
lon_min = 100 #抽出する最大経度
ini_t = f"{year}-{str(month).zfill(2)}-01T00:00:00.000000000"
output_folder_path_griddata = "グリッドデータの出力先フォルダーパス"
output_filename_griddata = "グリッドデータの出力ファイル名"
output_folder_path_movie = "動画の出力先フォルダーパス"
output_filename_movie = "動画の出力ファイル名"

################################ 風速強度のグリッドデータ作成 ################################
def arrangement():
    
    # 風速の大きさを計算
    m = np.sqrt(u**2 + v**2)
    # 緯度、経度データ
    lat = np.linspace(-90.0, 90.0, 145)[::-1]
    lon = np.linspace(0, 358.8, 288)
    # 合成風速のデータを生成
    wind_speed = xr.DataArray(data=m, 
                              dims=["lat", "lon"], 
                              coords={"lat": lat, "lon": lon}, 
                              attrs={"long_name": "Wind Speed", "units": "m/s",}
                              )
    # 緯度と経度の範囲でフィルタリング
    wind_speed = wind_speed.sel(lat=slice(lat_max, lat_min), lon=slice(lon_min, lon_max))

    # 緯度・経度とデータをxarrayから取得
    lat_values = wind_speed.lat.values  # 緯度
    lon_values = wind_speed.lon.values  # 経度
    data_values = wind_speed.values     # データ本体

    # 緯度と経度をグリッドにする
    lon_grid, lat_grid = np.meshgrid(
        np.linspace(lon_values.min(), lon_values.max(), 100),
        np.linspace(lat_values.min(), lat_values.max(), 100)
    )

    # 元データを平面座標と値に変換
    points = np.array([(lo, la) for la in lat_values for lo in lon_values])
    values = data_values.flatten()

    # griddataで補間
    grid_data = griddata(points, values, (lon_grid, lat_grid), method='cubic')

    return grid_data

################################ 動画作成 ################################
def movie():
    # 出力ファイル名を指定（フォルダー内に保存）
    video = cv2.VideoWriter(os.path.join(output_folder_path_movie, f'{output_filename_movie}.mp4'), fourcc, 5, (1320, 990))

    # 保存
    if not video.isOpened():
        print("can't be opened")
        sys.exit()
        
    for filename in gridfile_list:
        img = cv2.imread(output_folder_path_griddata+filename)

        # can't read image, escape
        if img is None:
            print("can't read")
            break
        
        # リサイズ（画像サイズが異なる場合、指定したサイズにリサイズ）
        img_resized = cv2.resize(img, (1320, 990))

        # add
        video.write(img_resized)
        print(filename)

    video.release()
    print('written')

################################################################################################
###################################### グリッドデータの作成 #####################################
################################################################################################

for month in range(1,12+1):
    ################################ xarrayデータセットとして、NetCDF形式のJRA-55を読み込む ################################
    ds_u = xr.open_dataset(f"{data_folder_path}\\UGRD_{year}{str(month).zfill(2)}.nc")
    ds_v = xr.open_dataset(f"{data_folder_path}\\VGRD_{year}{str(month).zfill(2)}.nc")
    data_u = ds_u.metpy.parse_cf('UGRD').squeeze()
    data_v = ds_v.metpy.parse_cf('VGRD').squeeze()

    for time_number in range(len(ds_u.variables["time"][:])):
        ################################ 各時間のデータを抽出 ################################
        t = ds_u.variables["time"][time_number].values 
        u = data_u.isel(time=time_number, level=level_p)
        v = data_v.isel(time=time_number, level=level_p)
        grid_data = arrangement()

        ################################ 連番の生成 ################################
        if str(t) == ini_t:
            i = 0
        ################################ 結果の出力 ################################
        output_path = os.path.join(output_folder_path_griddata, f'{output_filename_griddata}_{str(i).zfill(3)}.csv')
        pd.DataFrame(grid_data).to_csv(output_path, index=False, header=False)

        ################################ 進捗の出力 ################################
        i += 1
        print(t)

################################################################################################
################################ JRA55の風速強度分布を動画で可視化 ################################
################################################################################################

################################ グリッドデータの取得 ################################
gridfile_list = os.listdir(output_folder_path_griddata)
gridfile_list = np.sort(gridfile_list)
gridfile_list = [name for name in gridfile_list if "png" in name]

################################ encoder(for mp4) ################################
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

################################ 動画の作成 ################################
movie()