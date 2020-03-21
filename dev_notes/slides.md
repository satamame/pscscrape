# Python で Web から台本を収集する

---

**[さた@satamame](https://twitter.com/satamame)**

[株式会社リーディング・エッジ社](https://www.leadinge.co.jp/)
[劇団 GAIA_crew](https://gaiacrew.com/)

----

### 概要

---

- Python を使った Web スクレイピングの基本をやります
    - 台本公開サイトからテキストデータをダウンロードします
- 2段階でやります
    1. ダウンロードしたいデータについての情報収集
        - `scrapy` を使います
    1. その情報を使ってダウンロード
        - `reuqests` を使います

----

### 動機

---

世の中の台本がデータとして扱えるようになっていない
　▼
データとして扱えればいろいろメリットがあるのに…
　▼
うまいことフォーマット化できないか
　▼
そもそも世の中の台本はどうなっているのか
　▼
**データを集めよう**

(解析とかフォーマット化については考えてないけど、集める)

----

### 条件

---

- テキストデータであること
    - ❌ Word
    - ❌ PDF

----

### 参考までに

---

- 私が今までに見た台本はほぼ全て Word または PDF
- 世の中にはこんなフォーマットも
    - Fountain
    - Θέσπης
    - O's Editor 2 の「台本」スタイル *\**
    - VerticalEditor の「シナリオ形式」*\**

(*\** 書式は設定によります)

----

### ソースの選定

---

「はりこのトラの穴」というサイトに4,000本ある

> https://haritora.net/

- ダウンロードして読むだけなら問題なさそう
- 形式がプレーンテキスト (重要)

----

### 準備

---

- Python (3.8)
- 以下のパッケージ
    - scrapy (2.0.0)
    - requests (2.23.0)
    - pandas (1.0.2)

----

# 情報収集フェーズ

---


----

### scrapy のプロジェクトを作る

---

適当なディレクトリで実行すると、プロジェクト用のサブディレクトリができます

```
> scrapy startproject hariko
```

以降の作業はこのサブディレクトリの中でやります

```
> cd hariko
```

----

### 収集する情報を決める (1)

---

サイトの台本リストのページはこんな感じ

![](https://cdn.slideship.com/users/CB4haVXqcoujFL1byXTcv3/img/2020/03/Le1YXkk985MT8XAaqPPS2K.jpg =70%x)

- リストになっていてページネーションがある

----

### 取得する情報を決める (2)

---

ソースを見ると、リストは `<talbe>` になっている

- 各行はこんな形です

```html
<tr>
<td></td>
<th bgcolor="FF3030"><font color="white" size="+1">題名</font>
</th>
<td><a href="look.cgi?script=16224">詳細</a></td>
<th><a href="script.cgi?writer=7791">著者名</a>
</th>
</tr>
```

----

### 取得する情報を決める (3)

---

「詳細」を押して表示されるページにダウンロードフォームがあります

![](https://cdn.slideship.com/users/CB4haVXqcoujFL1byXTcv3/img/2020/03/LxQ5qdcJS36N3gQn9YLS6K.jpg =70%x)

----

### 取得する情報を決める (4)

---

ダウンロードフォームのソースがこうなので…

```html
<form method="POST" action="scriptdl.cgi/16224.txt">
<input type="hidden" name="script" value="16224">
<table>(...中略...)</table>
<br>
<input type="submit" value="全文ダウンロード">
</form>
```

詳細ページへのリンクのパラメタが、ダウンロードにも使えそう

↓これ (`script=` のところ)

```html
<td><a href="look.cgi?script=16224">詳細</a></td>
```

----

### 取得する情報を決める (5)

---

#### 方針

情報収集フェーズでは詳細ページには入らずに、台本リストから各台本の以下の情報を得る

1. 詳細ページの URL
1. その URL のパラメタ (`script=xxx`) の値
1. タイトル
1. 著者名

<br>※ダウンロードのリクエストに必要な情報は 2 だけ

----

### scrapy の Item を作る

---

プロジェクトディレクトリ (hariko) の中に `items.py` があるので、編集してサイトから取ってくるデータを定義します

```python
class HarikoItem(scrapy.Item):
    url = scrapy.Field()
    script_id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
```

----

### scrapy のスパイダーを作る (1)

---
スパイダーはサイトを巡回して情報を取ってくるやつです
`genspider` コマンドで作ります

```
> scrapy genspider (スパイダー名) (開始 URL)
```

今回は名前を `index` として、台本リストの URL を指定して作ります

```
> scrapy genspider index https://haritora.net/script.cgi
```

----

### scrapy のスパイダーを作る (2)

---

`hariko/spiders` ディレクトリの中に `index.py` ができます

```python
import scrapy

class IndexSpider(scrapy.Spider):
    name = 'index'
    allowed_domains = ['https://haritora.net/script.cgi']
    start_urls = ['http://https://haritora.net/script.cgi/']

    def parse(self, response):
        pass

----

### scrapy のスパイダーを作る (3)

---

`allowed_domains` と `start_urls` が変なので修正します

```python
class IndexSpider(scrapy.Spider):
    name = 'index'
    allowed_domains = ['https://haritora.net/script.cgi']
    start_urls = ['http://https://haritora.net/script.cgi/']
```
▼
```python
    allowed_domains = ['haritora.net']
    start_urls = ['https://haritora.net/script.cgi']
```

----

### scrapy のスパイダーを作る (4)

---

#### parse() メソッド

スパイダーの `parse()` メソッドは、サイトからのレスポンスを受け取って、以下のいずれかを `yield` で返します
1. 取得した情報
    - `scrapy.Item` オブジェクトまたは `dict`
        - 出力に追加されます
1. さらなるリクエスト
    - `scrapy.http.Response` オブジェクト
        - これにより、芋づる式にページを渡り歩きます

<br>※ `yield` なので何個返しても OK

----

### scrapy のスパイダーを作る (5)

---

たとえば以下のようにすると、台本リストの全てのページの URL を出力します

```python
    def parse(self, response):
        yield {'url': response.url}
        next_links = response.xpath("//a[text()='次へ->']")
        if next_links:
            url = response.urljoin(next_links[0].attrib['href'])
            yield scrapy.Request(url, callback=self.parse)
```

- 「次へ」要素があれば、その `href` をリクエストして再び `parse()` で受け取る、という処理になっています

![](https://cdn.slideship.com/users/CB4haVXqcoujFL1byXTcv3/img/2020/03/WreMDhakXUHoZ8uSQ7g2cw.jpg =70%x)


----

### scrapy のスパイダーを作る (6)

---

#### XPath について

XPath は、XML や HTML 内の要素を見つけるための、パターンマッチングの記法です

#### 例

台本リストの詳細ページへのリンク部分は以下のようでした

```html
<td><a href="look.cgi?script=16224">詳細</a></td>
```

この `<a>` 要素を見つけるためのパターンは、こうなります

```python
xpath = "//a[contains(@href, 'look.cgi?script=')]"
```

<br>※見つけた要素の親/兄弟要素をマッチングすることも可能

----

### scrapy のスパイダーを作る (7)

---

ここまでを踏まえて `parse()` メソッドを作ります
やることは以下のとおり

1. `response` から「詳細」リンク要素 (複数) を取得
1. 各リンク要素について
    - 周辺要素から `HarikoItem` 情報を得て `yield` で返す
1. `response` から「次へ」リンク要素を取得
1. 要素が見つかったらリクエストを作って `yield` で返す

<br>実際のコードは GitHub を御覧ください

- [pscscrape/hariko/hariko/spiders/index.py](https://github.com/satamame/pscscrape/blob/master/hariko/hariko/spiders/index.py)

