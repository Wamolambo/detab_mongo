import scrapy
from news.items import NewsItem


class NewsspiderSpider(scrapy.Spider):
    name = "newsspider"
    allowed_domains = ["edition.cnn.com"]
    start_urls = ["https://edition.cnn.com/"]

    def parse(self, response):
        # Get webpage ohject
        articles = response.css("div.scope")
        # Get webpage links
        links = articles.css('a.container__link ::attr(href)').getall()
        
        for link in links:

            if link is None:
                pass
            else:
                article_url = 'https://edition.cnn.com' + link

            yield response.follow(article_url,callback=self.parse_article_page)

    def parse_article_page(self, response):

        news_items = NewsItem()

        article = response.css("div.layout__content-wrapper")

        # cleaning processing 
        title = article.css("h1.headline__text::text").get()
        title = title.strip()
        title = "".join(c for c in title if ord(c)<128)

        # process
        author = response.xpath("//meta[@name='author']/@content")[0].extract()
        if author != '':
            pass
        else:
            author = response.css(".byline__names ::text").getall()
            if bool(author):
                author = author = ''.join(author)
                author = author.strip()
                author = author.replace("\n", '')

            else:
                author = 'CNN'

        # check for article content
        if len(article.css("div.article__content::text").getall()) != 0:
            article_content = article.css("div.article__content ::text").getall()
            article_content = ' '.join(map(str,article_content))
            paragraph = article_content.replace('\n','').replace('  ','').replace('\xa0','').replace('\xa0—\xa0','')
        else:
            if len(article.css("div.video-resource__description::text").getall()) != 0:
                paragraph = article.css("div.video-resource__description::text").get()
            else:
                if len(article.css("span.inline-placeholder::text").getall()) != 0:
                          #paragraph = article.css("span.inline-placeholder::text").getall()
                    paragraph = article.css("span.inline-placeholder::text").get()
                else:
                    paragraph = "No content provided by article"

    
        
        news_items['paragraph'] = paragraph,
        news_items['title'] = title,
        news_items['author'] = author,
        news_items['url'] = response.url,
        
        
        yield news_items


    