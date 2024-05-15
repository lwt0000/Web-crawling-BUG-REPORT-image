import scrapy
from bs4 import BeautifulSoup
from bug_report_scraper.items import BugReportItem
from urllib.parse import urljoin


# class BugSpider(scrapy.Spider):
#     name = 'bug_spider'
#     start_urls = ['https://answers.ea.com/t5/Bug-Reports/bd-p/wrc-bug-reports-en/page/2']

#     def parse_thread(self, response):
#         # text = response.css('div.lia-message-body-content span::text').getall()
#         # description = ' '.join(text)


#         image_url = response.css('a.lia-link-navigation.attachment-link::attr(href)').get()


#         original_post = response.css('div.lia-message-body-content').getall()[0]

#         # Extracting all text within this div
#         text = ''.join(response.xpath("string(//div[@class='lia-message-body-content'][1])").get())

#         # Clean up the text to replace multiple whitespaces with a single space
#         cleaned_text = ' '.join(text.split())
        
   

#         #if no image, skip
#         if image_url is None:
#             return

#         yield {
#             'description': cleaned_text,
#             'image_urls': image_url
#         }

#     def parse(self, response):
#         thread_links = response.css('a.page-link.lia-link-navigation.lia-custom-event::attr(href)').getall()
#         for link in thread_links:
#             yield response.follow(link, self.parse_thread)

class BugSpider(scrapy.Spider):
    name = 'bug_spider'
    start_urls = ['https://answers.ea.com/t5/Bug-Reports/bd-p/wrc-bug-reports-en']
    domain = 'https://answers.ea.com'
    def parse_thread(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        original_post_div = soup.find('div', class_='lia-message-body-content')
        
        if original_post_div:
            original_post_text = ' '.join(original_post_div.stripped_strings)
        else:
            original_post_text = "Original post not found."

        images = soup.find_all('a', class_='lia-link-navigation attachment-link')
        # print(images)
        base_url = self.domain
        image_urls =[]
        for img in images:
            download_url = img.find('span')['li-download-url']
            full_url = urljoin(base_url, download_url)
            # print(full_url)
            image_urls.append(full_url)

        if not image_urls:
            return

        item = BugReportItem()
        item['description'] = original_post_text
        item['image_urls'] = image_urls
        yield item
        


    def parse(self, response):
        thread_links = response.css('a.page-link.lia-link-navigation.lia-custom-event::attr(href)').getall()
        for link in thread_links:
            yield response.follow(link, self.parse_thread)
        
        next_page = response.css('a.lia-link-navigation.lia-js-data-pageNum-2.lia-custom-event::attr(href)').get()
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)