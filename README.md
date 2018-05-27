FOLLOW-BY-LOCATION-INFORMATION-TWITTERBOT
===========

## 概要

指定した位置情報を付与してtweetした人をフォローするbot。

tweet検索APIでは緯度経度と半径での指定、もしくはロケーションID(区や店)でしか検索できないので、
複数の半径で広めに指定した上で行政界データで範囲を絞る。

## 備考

* 既にフォロー済みの人へは何もしない
* デフォルトでは連続で10名までフォローする
* 連続フォロー時はランダムでsleepをかける

## 使い方

1. 半径データを用意
    - `data/serch_meguro.csv` を参考
    - http://www.nanchatte.com/map/circleService.html 等が便利
    - 必要な検索結果が多くなるのを防ぐため関係ない人工密集地(目黒区の場合、渋谷等)は避ける
2. 行政界データを用意
    - `convert.py` を参考
3. 必要な place name を確認
    - 位置情報が `Meguro-ku` 等の場合は検索結果のbounding_boxが区のmax,minの緯度経度のため行政界をはみ出るため区名での指定も可能
    - 目黒区の場合は、`Meguro-ku`
4. Twitter接続情報を用意
    - 下記のような `config.py` を用意
5. 起動用pyを作成
    - `main_meguro.py` を参考

``` config.py
CONSUMER_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"
CONSUMER_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
ACCESS_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
ACCESS_TOKEN_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

## License

* MIT
    + see LICENSE