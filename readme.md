# 概要

[はりこのトラの穴](https://haritora.net/) というサイトで公開されている台本を、まとめてダウンロードするプログラムです。

# 環境

Python 3 なら動くと思います。
`Pipfile` を使って仮想環境を作るか、以下のパッケージをインストールしてください。

- scrapy
- requests
- pandas

# 使い方

## インデックスの取得

`hariko` ディレクトリ (2つありますが、上の方) に入ります。

```
cd hariko
```

`hariko/index.csv` がある場合は削除しておかないと、クロールの結果が既存の内容に追記されるようです。

```
rm index.csv
```

"脚本ダウンロードサービス" のページから、登録されている全ての台本のインデックスを取得します。  
これには時間がかかります。

```
scrapy crawl index -o index.csv
```

## ダウンロードの設定

`hariko/download.py` を編集します。

```python
#%% 設定
index_file = 'index.csv'    # インデックスファイル名
dl_dir = 'scripts'          # 台本保存先ディレクトリ名
overwrite = False           # ファイルが存在したら上書きするか
max_count = 500             # 最大ダウンロード数
interval = 2                # ダウンロード間の待ち時間 (秒)
```

- `overwrite` を False にすると、下記の `hariko/download.py` の実行を繰り返すことで、`max_count` ずつダウンロードできます。
- サイトに迷惑をかけないよう、`interval` は必ず設定しましょう。

`hariko` ディレクトリ (2つありますが、上の方) に入った状態で、ダウンロードを実行します。  
実行時間については、`max_count` と `interval` の値からだいたい分かると思います。

```
python download.py
```

- 上記の設定ですと、`hariko/scripts` というフォルダの中に、ダウンロードした台本が保存されます。
