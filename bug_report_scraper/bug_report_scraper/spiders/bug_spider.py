import scrapy
from bs4 import BeautifulSoup

class BugSpider(scrapy.Spider):
    name = 'bug_spider'
    start_urls = ['https://answers.ea.com/t5/Bug-Reports/bd-p/wrc-bug-reports-en/page/2']

    def parse_thread(self, response):
        # text = response.css('div.lia-message-body-content span::text').getall()
        # description = ' '.join(text)


        image_url = response.css('a.lia-link-navigation.attachment-link::attr(href)').get()


        original_post = response.css('div.lia-message-body-content').getall()[0]

        # Extracting all text within this div
        text = ''.join(response.xpath("string(//div[@class='lia-message-body-content'][1])").get())

        # Clean up the text to replace multiple whitespaces with a single space
        cleaned_text = ' '.join(text.split())
        
   

        #if no image, skip
        if image_url is None:
            return

        yield {
            'description': cleaned_text,
            'image_urls': image_url
        }

    def parse(self, response):
        thread_links = response.css('a.page-link.lia-link-navigation.lia-custom-event::attr(href)').getall()
        for link in thread_links:
            yield response.follow(link, self.parse_thread)
