# 手順メモ

## インストール

[10分で理解する Scrapy](https://qiita.com/Chanmoro/items/f4df85eb73b18d902739)

```
pipenv install
```

```
pipenv install scrapy

pipenv run scrapy version
```

## プロジェクト作成

```
pipenv run scrapy startproject hariko
```

対象サイト: [はりこのトラの穴](https://haritora.net/)

- hariko/items.py を編集

```python
class HarikoItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
```

## settings.py

サイトへの負荷が気になるので、以下の変更をする。

```
CONCURRENT_REQUESTS = 1

DOWNLOAD_DELAY = 2
```

## スパイダー作成

インデックスを作るスパイダーなので `index` という名前にする

```
pipenv shell
cd hariko
scrapy genspider index https://haritora.net/script.cgi
```

- hariko/hariko/spiders/index.py を編集

参考: [Python, Scrapyの使い方](https://note.nkmk.me/python-scrapy-tutorial/)

ページ内のリンクを絶対 URL に統一する方法

```python
# たとえば最初の (href 属性を持つ) a タグ
link = response.xpath("//a[@href]")[0]
url = response.urljoin(link.attrib['href'])
```

### 実行

```
scrapy crawl <spyder name>
```

または

```
scrapy crawl <spyder name> -o index.csv
```

- ファイルが存在する場合は、追記になるっぽい。

## ダウンロード用スクリプト

参考: [HTTPのPOST/GETリクエストをする](https://python.civic-apps.com/http-request-post-get/)

```
pip install requests
```

