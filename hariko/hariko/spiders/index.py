# -*- coding: utf-8 -*-
import scrapy
from hariko.items import HarikoItem


class IndexSpider(scrapy.Spider):
    '''インデックスを作成するスパイダー
    '''
    
    name = 'index'
    allowed_domains = ['haritora.net']
    start_urls = ['https://haritora.net/script.cgi']

    def parse(self, response):
        '''ダウンロードサービスのページごとのクロール
        '''
        
        # 各台本の詳細ページへのリンク
        xpath = "//a[contains(@href, 'look.cgi?script=')]"
        
        # 詳細ページへのリンクの周辺からデータ取得
        for detail_link in response.xpath(xpath):
            # 詳細ページへのリンク (相対パス)
            link = detail_link.attrib['href']
            # そのフルパス
            url = response.urljoin(link)
            # 台本番号
            script_id = int(link.split('=')[-1])
            # 題名
            title = detail_link.xpath(
                "parent::td/preceding-sibling::th/font/text()").get()
            # 著者名
            author = detail_link.xpath(
                "parent::td/following-sibling::th/a/text()").get()
            # インスタンス生成
            item = HarikoItem(
                url = url,
                script_id = script_id,
                title = title,
                author = author
            )
            
            yield item
        
        # 次のページへのリンク
        xpath = "//a[text()='次へ->']"
        next_links = response.xpath(xpath)
        
        # あれば再帰呼び出し
        if next_links:
            url = response.urljoin(next_links[0].attrib['href'])
            yield scrapy.Request(url, callback=self.parse)
