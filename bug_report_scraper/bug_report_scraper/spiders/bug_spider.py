import scrapy
from bs4 import BeautifulSoup
from bug_report_scraper.items import BugReportItem
from urllib.parse import urljoin

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
        

        #find the number of people who have the same issue
        num_pepole_has_same_issue = soup.find('a', class_='lia-link-navigation lia-rating-value-summary')
        if num_pepole_has_same_issue:
            num_pepole_has_same_issue = num_pepole_has_same_issue.text[0]
        

        item = BugReportItem()
        item['description'] = original_post_text
        item['image_urls'] = image_urls
        item['original_post_url'] = response.url
        item['num_pepole_has_same_issue'] = int(num_pepole_has_same_issue)
        item['images_names'] = []
        yield item
        


    def parse(self, response):
        thread_links = response.css('a.page-link.lia-link-navigation.lia-custom-event::attr(href)').getall()
        for link in thread_links:
            yield response.follow(link, self.parse_thread)
        
        next_page = response.css('a.lia-link-navigation.lia-js-data-pageNum-2.lia-custom-event::attr(href)').get()
        
        if next_page is not None:#comment this line if don't want to scrape all pages
            yield response.follow(next_page, callback=self.parse)