################################################################################
# モデル式をスぺクトルにフィッティングするプログラム
################################################################################

import torch
import numpy as np
import pandas as pd
import torch.optim as optim
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

########################## パラメータ ##########################
fft_file_path = "fft結果のファイルパス"



########################## 1日と12時間のピークを除く ##########################
def dataset(x_original, y_original):
    x = x_original
    y = [x * y for x, y in zip(x_original, y_original)]
    
    # 1日周りの周波数領域のみを取り出す
    around_1day_freq = [f for f in x if  10**-5 < f < 1.5*10**-5]
    around_1day_spectrum = [y[i] for i, f in enumerate(x) if f in around_1day_freq]
    # 12時間周りの周波数領域のみを取り出す
    around_12hour_freq = [f for f in x if  1.5*10**-5 < f < 3*10**-5]
    around_12hour_spectrum = [y[i] for i, f in enumerate(x) if f in around_12hour_freq]

    # ピークの値の取得
    day_peak = np.max(around_1day_spectrum)
    half_day_peak = np.max(around_12hour_spectrum)
    # ピークの値の周波数の取得
    day_freq_row = [i for i, x in enumerate(y) if x == day_peak][0]
    half_day_freq_row = [i for i, x in enumerate(y) if x == half_day_peak][0]

    # 1日・12時間ピークを抜く
    x.pop(day_freq_row)
    y.pop(day_freq_row)
    x.pop(half_day_freq_row-1)
    y.pop(half_day_freq_row-1)

    # 移動平均の窓サイズ
    window_size = 9
    # 移動平均フィルタを適用
    y = np.convolve(np.array(y), np.ones(window_size)/window_size, mode='same')
    # spectrumをリストへ
    y = y.tolist()

    # 限定的な範囲の取得
    x_data = [f for f in x if  1/(3600*24) < f < 1/(3600*5)]
    y_data = [y[i] for i, f in enumerate(x) if f in x_data]
    
    #対数へ
    x_data = [np.log10(i) for i in x_data]
    
    
    return x_data, y_data, x_original, y

########################## フィッティング ##########################
def fitting(x_data, y_data, max_epochs, x_original, y_original):
    #テンソルへ
    x_data = torch.tensor(x_data)
    y_data = torch.tensor(y_data)
    
    # モデルを定義する
    def model(x, a, b):
        return a*10**(-2/3*x) + b*10**(-2*x)

    #初期値の修正のための係数
    c = y_data[int(len(y_data)/2)]/((3*10**-4)*10**(-2/3*x_data[int(len(x_data)/2)]) + (3*10**-11)*10**(-2*x_data[int(len(x_data)/2)]))

    # パラメータ（a, b）を初期値の決定
    a = (c * 3 * 10**-4).clone().detach().requires_grad_(True)
    b = (c * 3 * 10**-11).clone().detach().requires_grad_(True)
    
    # 最適化手法を選択する
    optimizer = optim.Adam([a, b], lr=10**-7)  # Adamを使用し、適切な学習率を設定

    # 損失関数を定義する
    def loss_fn(y_pred, y_true):
        return torch.mean((y_pred - y_true)**2)
    
    # Modelの初期設定
    min_loss = float('inf')
    best_a = None
    best_b = None
    
    for _ in range(max_epochs):
        # Model prediction
        y_pred = model(x_data, a, b)
        # Calculate loss
        loss = loss_fn(y_pred, y_data)
        
        # 逆伝播およびパラメータの更新
        optimizer.zero_grad() #勾配を初期化
        loss.backward() # 逆伝播
        optimizer.step() # パラメータの更新
        
        # best_aとbest_bの更新
        if loss < min_loss:
            min_loss = loss
            best_a = a.item()
            best_b = b.item()
    
    r2 = r2_score(y_data.detach().numpy(), y_pred.detach().numpy()) 
    
    # Check if best_a or best_b is negative
    if best_a < 0 or best_b < 0 or r2 < 0.8:
        best_a = "NaN"
        best_b = "NaN"
    
    # graph_psd_fit(model, best_a, best_b, x_original, y_original) # フィッティング結果の描画
    return best_a, best_b

########################## フィッティング結果の確認 ##########################
def graph_psd_fit(model, a, b, x_original, y_original):
    # 10のべき乗表示に変換
    integer_a = format(a, ".2E").split('E')[0]
    integer_b = format(b, ".2E").split('E')[0]
    exponent_a = str(int(format(a, ".2E").split('E')[-1]))
    exponent_b = str(int(format(b, ".2E").split('E')[-1]))
    
    # 予測データの整理
    x = torch.linspace(np.log10(4*10**-7), np.log10(4*10**-3), 100)  # プロットする範囲を指定
    y = model(x, a, b)
    x = np.power(10, np.array(x.numpy()))
    y = np.array(y.detach().numpy())
    
    plt.figure()
    plt.plot(x_original, y_original, color="orange", label="observation", lw=5)
    plt.plot(x, y, color="green", label=r"$d_{1}=$"+str(integer_a)+r"$\times{10}^{"+str(exponent_a)+"}, $"+
             r"$d_{2}=$"+str(integer_b)+r"$\times{10}^{"+str(exponent_b)+"}$")
    plt.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.2))
    plt.xlabel("$f$"+"(1/s)", fontsize=14)
    plt.ylabel("$fS(f)$"+r"$\rm{(m^2/s^2)}$", fontsize=14)
    plt.tick_params(labelsize=13)
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(which="major", axis="x")
    plt.grid(which="minor", axis="x", linestyle="--")
    plt.xlim([4*10**-7, 4*10**-4])
    plt.ylim([2*10**-2, 10])

    # 周波数帯域に対応する時間スケールの表示
    plt.text(1/(2592000), plt.ylim()[1], '1M', ha='center', va='bottom', fontsize=13)
    plt.text(1/(604800), plt.ylim()[1], '1W', ha='center', va='bottom', fontsize=13)
    plt.text(1/(259200), plt.ylim()[1], '3D', ha='center', va='bottom', fontsize=13)
    plt.text(1/(86400), plt.ylim()[1], '1D', ha='center', va='bottom', fontsize=13)
    plt.text(1/(43200), plt.ylim()[1], '12H', ha='center', va='bottom', fontsize=13)
    plt.text(1/(21600), plt.ylim()[1], '6H', ha='center', va='bottom', fontsize=13)
    plt.text(1/(10800), plt.ylim()[1], '3H', ha='center', va='bottom', fontsize=13)
    plt.text(1/(3600), plt.ylim()[1], '1H', ha='center', va='bottom', fontsize=13)
    plt.tight_layout()
    plt.show()

########################## fft結果のダウンロード ##########################
df_fft = pd.read_csv(fft_file_path)
freq = df_fft["周波数の任意のカラム"].tolist() # 周波数を取り出す
fft = df_fft["fft結果の任意のカラム"].tolist() # fft結果を取り出す
    
########################## フィッティング用のデータ生成 ##########################
x_data, y_data, x_original, y_original = dataset(freq, fft)

########################## フィッティングを行う ##########################
best_a, best_b = fitting(x_data, y_data, 5000, x_original, y_original)

########################## 結果を出力 ##########################
print(best_a, best_b)
