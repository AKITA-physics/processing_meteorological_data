# 気象データの処理に関するプログラム

## AMeDASフォルダ
・気象庁ホームページの「過去の気象データ」から10分値の気象データをスクレイピングするためのコードが入っています。

・バイナリ形式の地上気象観測1分値を展開するためのコード

## JRA-55フォルダ
NetCDF形式のJRA-55のデータを展開し、風速強度の時系列動画を生成するコードが入っています。

## Wind_profilerフォルダ
・京都大学のホームページからウィンドプロファイラ観測データをスクレイピングするコード

・BUFR形式のウィンドプロファイラデータを展開するコード（http://macroscope.world.coocan.jp/ja/edu/compex/use_jma_wind_profiler/index.html を参照してください）

・日データを各年で結合するコード

・ウィンドプロファイラデータは欠損データがNaNで定義されておらず抜けているため、NaNで欠損データを補間するコード

## Processフォルダ
・風速データからFFT（高速フーリエ変換）でスペクトルを計算し、平滑化するコード

・２変数関数でスペクトルをフィッティングするコード
