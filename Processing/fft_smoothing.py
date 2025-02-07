###################################################################################
# 風速データからfftを用いてスペクトルを算出するプログラム
###################################################################################

import pandas as pd
import numpy as np

###################################### パラメータ #################################
file_path = "スペクトルを計算したい補間後の風速データのファイルパス"
sampling_freq = 1/(60*10) # サンプリング周波数


############################ fft ############################
def fft(sig, spr):
    sampling_rate = spr  # サンプリングレート(サンプル/秒)
    N = len(sig) # サンプル数
    # 周波数軸の作成
    freq = np.fft.rfftfreq(N, 1/sampling_rate)
    freq = freq[1:]
    # FFTを計算
    fft_result = np.fft.rfft(sig)
    fft_result = np.abs(fft_result)
    fft_result = fft_result[1:]
    # 強度の計算
    spectrum = fft_result ** 2 / sampling_rate / (N/2)
    
    # リスト化
    freq = freq.tolist()
    fft_result = spectrum.tolist()
    mean_wind = np.mean(sig)

    return freq, fft_result, mean_wind

############################ 平滑化 ############################
def smoothing(freq, fft_result):
    # 1日周りの周波数領域のみを取り出す
    around_1day_spectrum = [fft_result[i] for i, f in enumerate(freq) if 10**-5 < f < 1.5*10**-5]
    
    # 12時間周りの周波数領域のみを取り出す
    around_12hour_spectrum = [fft_result[i] for i, f in enumerate(freq) if 1.5*10**-5 < f < 3*10**-5]
    
    # ピークの値の取得
    day_peak = np.max(around_1day_spectrum)
    half_day_peak = np.max(around_12hour_spectrum)
    
    # ピークの値の周波数の取得
    day_freq_row = [i for i, x in enumerate(fft_result) if x == day_peak]
    half_day_freq_row = [i for i, x in enumerate(fft_result) if x == half_day_peak]
    
    # fft_resultをデータフレームへ
    df_fft_result = pd.DataFrame(fft_result)
    
    # 1日・12時間ピークを抜く
    df_fft_result.loc[day_freq_row] = np.nan
    df_fft_result.loc[half_day_freq_row] = np.nan
    
    # 1日・12時間ピークを抜いた強度を線形補完
    nan_fft_result = df_fft_result.interpolate().values.flatten()
    
    # 移動平均の窓サイズ
    window_size = 10
    # 移動平均フィルタを適用
    spectrum = np.convolve(nan_fft_result, np.ones(window_size)/window_size, mode='same')
    
    # 平滑後の周波数とスペクトルを入れるリスト
    list_freq = []
    list_spectrum = []
    
    # 周波数をlog形式へ
    log_freq = np.log10(freq)
    min_log_freq = np.min(log_freq)
    max_log_freq = np.max(log_freq)
    
    # 処理する周波数の幅を決める
    list_scale = np.arange(min_log_freq, max_log_freq, 0.04)
    
    # それぞれの周波数幅の平均値を求める
    for i in range(len(list_scale) - 1):
        selected_indices = (log_freq >= list_scale[i]) & (log_freq < list_scale[i + 1])
        if np.any(selected_indices):
            freq_mean = np.mean(log_freq[selected_indices])
            spectrum_mean = np.mean(spectrum[selected_indices])
            list_freq.append(freq_mean)
            list_spectrum.append(spectrum_mean)
    
    # リストからNaNを取り除く
    list_freq = [f for f in list_freq if not np.isnan(f)]
    list_spectrum = [s for s in list_spectrum if not np.isnan(s)]
    
    # 周波数をlog形式から戻す
    list_freq = np.power(10, list_freq).tolist()
    
    # 移動平均の窓サイズ
    window_size = 4
    # 移動平均フィルタを適用
    list_spectrum = np.convolve(np.array(list_spectrum), np.ones(window_size)/window_size, mode='same')
    # spectrumをリストへ
    list_spectrum = list_spectrum.tolist()
    
    # リストに1日・12時間ピークを戻す
    for period, peak in zip([86400, 43200], [day_peak, half_day_peak]):
        freq_to_insert = 1 / period
        index_to_insert = next((i for i, f in enumerate(list_freq) if f > freq_to_insert), len(list_freq))
        list_freq.insert(index_to_insert, freq_to_insert)
        list_spectrum.insert(index_to_insert, peak)
    
    # 出力する周波数とスペクトル
    return list_freq, list_spectrum


############################ 補間後のデータの取得 ############################
df_interpolation = pd.read_csv(file_path)

############################ スペクトルの計算 ############################            
wind = np.array(df_interpolation["fftを行う任意のカラム"]) # データの準備
freq, fft_result, mean_wind = fft(wind, sampling_freq) # スペクトルの計算

############################ 平滑化 ############################            
list_freq, list_spectrum = smoothing(freq, fft_result)

############################ 結果の出力 ############################            
print(f"周波数:{list_freq}")
print(f"スペクトル:{list_spectrum}")