import scrapy
from bs4 import BeautifulSoup
from bug_report_scraper.items import BugReportItem
from urllib.parse import urljoin



class BugSpider(scrapy.Spider):
    name = 'bug_spider'
    domain = 'https://answers.ea.com'
    main_page_id = 2 #used for pagination of the main bug report page
    post_page_id = 2 #used for pagination of the post page
    image_urls =[]
    def __init__(self, start_urls=None, game_name=None, *args, **kwargs):
        super(BugSpider, self).__init__(*args, **kwargs)
        if start_urls:
            self.start_urls = [start_urls]
        self.game_name = game_name
    def check_pages_in_each_thread(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        #look for images
        images = soup.find_all('a', class_='lia-link-navigation attachment-link')
        base_url = self.domain
        # print("HHHHHHHHHHHHHHHHH")
        for img in images:
            download_url = img.find('span')['li-download-url']
            #if the last 3 characters are not png, jpg or jpeg, skip the image
            if download_url[-3:] not in ['png', 'jpg', 'jpeg','bmp','heic']:
                #this need improvement
                continue
            full_url = urljoin(base_url, download_url)
            self.image_urls.append(full_url)
        # scrape the other pages inside this post if there are any
        link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.post_page_id)
        next_page = response.css(link).get()
        if next_page is not None:
            self.post_page_id = self.post_page_id + 1
            yield response.follow(next_page, callback=self.check_pages_in_each_thread)

    def parse_thread(self, response):
        #reset the image urls here
        self.image_urls = []
        soup = BeautifulSoup(response.text, 'lxml')
        original_post_div = soup.find('div', class_='lia-message-body-content')#find the first post in this thread  
        
        if original_post_div:
            original_post_text = ' '.join(original_post_div.stripped_strings)
        else:
            original_post_text = "Original post not found."

        images = soup.find_all('a', class_='lia-link-navigation attachment-link')
        base_url = self.domain
        
        for img in images:
            download_url = img.find('span')['li-download-url']
            #if the last 3 characters are not png, jpg or jpeg, skip the image
            if download_url[-3:] not in ['png', 'jpg', 'jpeg','bmp','heic']:#elimate possible .txt file or other file when bug report usually contains
                #this need improvement
                continue
            full_url = urljoin(base_url, download_url)
            self.image_urls.append(full_url)

        num_people_has_same_issue = soup.find('a', class_='lia-link-navigation lia-rating-value-summary')
        if num_people_has_same_issue:
            num_people_has_same_issue = num_people_has_same_issue.text[0]


        

        # scrape the other pages inside this post if there are any
        link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.post_page_id)
        next_page = response.css(link).get()
        if next_page is not None:
            self.post_page_id += 1
            yield response.follow(next_page, callback=self.check_pages_in_each_thread)

        if not self.image_urls:
            return

        item = BugReportItem()
        item['description'] = original_post_text
        item['image_urls'] = self.image_urls
        item['original_post_url'] = response.url
        #try converting the number of people to int, if it fails, set it to 0, not every post has this, ex. replys under the original post
        try:
            item['num_people_has_same_issue'] = int(num_people_has_same_issue)
        except:
            item['num_people_has_same_issue'] = 0
        item['images_names'] = []

        yield item

    def parse(self, response):
        thread_links = response.css('a.page-link.lia-link-navigation.lia-custom-event::attr(href)').getall()
        for link in thread_links:
            #reset page id for the next thread
            self.post_page_id = 2
            yield response.follow(link, self.parse_thread)
        #go to next page in the bug report main page
        link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.main_page_id)
        self.main_page_id += 1
        next_page = response.css(link).get()
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)




