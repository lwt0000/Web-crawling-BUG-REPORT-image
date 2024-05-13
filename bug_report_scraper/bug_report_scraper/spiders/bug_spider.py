import scrapy
from bs4 import BeautifulSoup

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
    start_urls = ['https://answers.ea.com/t5/Bug-Reports/bd-p/wrc-bug-reports-en/page/2']

    def parse_thread(self, response):
        # Convert the Scrapy response to a BeautifulSoup object
        soup = BeautifulSoup(response.text, 'lxml')

        # Assuming the original post is the first div with class 'lia-message-body-content'
        original_post_div = soup.find('div', class_='lia-message-body-content')

        # Check if the div is found
        if original_post_div:
            # Extract all text, including handling nested tags
            original_post_text = ' '.join(original_post_div.stripped_strings)
        else:
            original_post_text = "Original post not found."

        # Extract image URLs using Scrapy's CSS selectors
        # This assumes images are linked in <a> tags with class 'attachment-link'
        image_urls = response.css('a.lia-link-navigation.attachment-link::attr(href)').getall()

        # if no image, skip
        if not image_urls:
            return
        
        yield {
            'description': original_post_text,
            'image_urls': image_urls
        }

    def parse(self, response):
        # Loop through all thread links on the page
        thread_links = response.css('a.page-link.lia-link-navigation.lia-custom-event::attr(href)').getall()
        for link in thread_links:
            yield response.follow(link, self.parse_thread)