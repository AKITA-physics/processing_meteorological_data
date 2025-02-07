############################################################################
# ウィンドプロファイラのデータをスクレイピングするコード
############################################################################

import requests
from bs4 import BeautifulSoup
import urllib.request
import io
import os
import shutil
import tarfile

################################ パラメータ ################################
year = 2020 # データを取得する年数
original_folder_path = "スクレイピングしたデータの入っているフォルダーパス"
output_folder_path = "データの出力先のフォルダーパス"
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

################################ 月末日の定義 ################################
def month_day(month):
    if month in [1,3,5,7,8,10,12]:
        last_day = 31
    elif month in [4,6,9,11]:
        last_day = 30
    elif month in [2]:
        last_day = 28
    return last_day

################################ webサイトからファイルのURLを取得する関数 ################################
def extract_urls_from_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    list_urls = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith('IUPC'):
            list_urls.append(href)
    return list_urls


for month in range(1,12+1):
    for day in range(1,month_day(month)+1):
        ################################ webサイトからファイルのURLを取得し、リストにまとめる ################################
        webpage_url = f'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/jma-radar/wprof/original/{year}/{str(month).zfill(2)}/{str(day).zfill(2)}/'
        list_urls = extract_urls_from_webpage(webpage_url)

        ################################ データの取得 ################################
        for part_url in list_urls:
            # ウェブページのURLを指定して実行
            url = f'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/jma-radar/wprof/original/{year}/{str(month).zfill(2)}/{str(day).zfill(2)}/'+str(part_url)
            # ファイルをダウンロード
            response = urllib.request.urlopen(url)
            
            # tar.gzファイルを展開
            with tarfile.open(fileobj=io.BytesIO(response.read()), mode='r:gz') as tar:
                tar.extractall()
        
        ################################ 指定したファイルを特定のファイルに移す ################################
        for filename in os.listdir(original_folder_path):
            for j in range(41,50+1):
                if filename[4:6] == str(j):
                    source_file_path = os.path.join(original_folder_path, filename)
                    destination_file_path = os.path.join(f"{output_folder_path}\\{year}_{block_no_lists[j]}.send", filename)
                    
                    # 移動先のフォルダが存在するか確認
                    output_dir = os.path.dirname(destination_file_path)  # ファイルパスからフォルダパスを取得
                    if not os.path.exists(output_dir):  # フォルダが存在しない場合
                        os.makedirs(output_dir)  # フォルダを作成
                    
                    # ファイルを移動する
                    shutil.move(source_file_path, destination_file_path)
                    # print(f"ファイルを移動しました: {destination_file_path}")

        ################################ 進捗を出力 ################################
        print(month, day)