# import scrapy
# from bs4 import BeautifulSoup
# from bug_report_scraper.items import BugReportItem
# from urllib.parse import urljoin



# class BugSpider(scrapy.Spider):
#     name = 'bug_spider'
#     domain = 'https://answers.ea.com'
#     main_page_id = 2 #used for pagination of the main bug report page
#     post_page_id = 2 #used for pagination of the post page
#     image_urls =[]
#     def __init__(self, start_urls=None, game_name=None, *args, **kwargs):
#         super(BugSpider, self).__init__(*args, **kwargs)
#         if start_urls:
#             self.start_urls = [start_urls]
#         self.game_name = game_name
#     def check_pages_in_each_thread(self, response):
#         soup = BeautifulSoup(response.text, 'lxml')
#         #look for images
#         images = soup.find_all('a', class_='lia-link-navigation attachment-link')
#         base_url = self.domain
        
#         for img in images:
#             download_url = img.find('span')['li-download-url']
            
#             #if the last 3 characters are not png, jpg or jpeg, skip the image
#             if download_url[-3:] not in ['png', 'jpg', 'jpeg','bmp','heic']:
#                 #this need improvement
#                 continue
#             full_url = urljoin(base_url, download_url)
#             print(full_url)
#             print('original post url:', response.url)
#             self.image_urls.append(full_url)
#         # scrape the other pages inside this post if there are any
#         link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.post_page_id)
#         next_page = response.css(link).get()
#         if next_page is not None:
#             self.post_page_id = self.post_page_id + 1
#             yield response.follow(next_page, callback=self.check_pages_in_each_thread)

#     def parse_thread(self, response):
#          #reset page id for the next thread
#         self.post_page_id = 2
#         #reset the image urls here
#         self.image_urls = []
#         soup = BeautifulSoup(response.text, 'lxml')
#         original_post_div = soup.find('div', class_='lia-message-body-content')#find the first post in this thread  
        
#         if original_post_div:
#             original_post_text = ' '.join(original_post_div.stripped_strings)
#         else:
#             original_post_text = "Original post not found."

#         images = soup.find_all('a', class_='lia-link-navigation attachment-link')
#         base_url = self.domain
        
#         for img in images:
#             download_url = img.find('span')['li-download-url']
#             #if the last 3 characters are not png, jpg or jpeg, skip the image
#             if download_url[-3:] not in ['png', 'jpg', 'jpeg','bmp','heic']:#elimate possible .txt file or other file when bug report usually contains
#                 #this need improvement
#                 continue
#             full_url = urljoin(base_url, download_url)
#             self.image_urls.append(full_url)

#         num_people_has_same_issue = soup.find('a', class_='lia-link-navigation lia-rating-value-summary')
#         if num_people_has_same_issue:
#             num_people_has_same_issue = num_people_has_same_issue.text[0]


        

#         # scrape the other pages inside this post if there are any
#         link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.post_page_id)
#         next_page = response.css(link).get()
#         if next_page is not None:
#             self.post_page_id += 1
#             yield response.follow(next_page, callback=self.check_pages_in_each_thread)

#         if not self.image_urls:
#             return

#         item = BugReportItem()
#         item['description'] = original_post_text
#         item['image_urls'] = self.image_urls
#         item['original_post_url'] = response.url
#         #try converting the number of people to int, if it fails, set it to 0, not every post has this, ex. replys under the original post
#         try:
#             item['num_people_has_same_issue'] = int(num_people_has_same_issue)
#         except:
#             item['num_people_has_same_issue'] = 0
#         item['images_names'] = []

#         yield item

#     def parse(self, response):
#         thread_links = response.css('a.page-link.lia-link-navigation.lia-custom-event::attr(href)').getall()
#         for link in thread_links:
#             yield response.follow(link, self.parse_thread)
#         #go to next page in the bug report main page
#         link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.main_page_id)
#         self.main_page_id += 1
#         next_page = response.css(link).get()
        
#         if next_page is not None:
#             yield response.follow(next_page, callback=self.parse)



# import scrapy
# from bs4 import BeautifulSoup
# from bug_report_scraper.items import BugReportItem
# from urllib.parse import urljoin

# class BugSpider(scrapy.Spider):
#     name = 'bug_spider'
#     domain = 'https://answers.ea.com'
#     main_page_id = 2
#     post_page_id = 2
#     image_urls = []

#     def __init__(self, start_urls=None, game_name=None, *args, **kwargs):
#         super(BugSpider, self).__init__(*args, **kwargs)
#         if start_urls:
#             self.start_urls = [start_urls]
#         self.game_name = game_name

#     def extract_images(self, soup):
#         images = soup.find_all('a', class_='lia-link-navigation attachment-link')
#         base_url = self.domain
#         for img in images:
#             download_url = img.find('span')['li-download-url']
#             if download_url.split('.')[-1].lower() in ['png', 'jpg', 'jpeg', 'bmp', 'heic']:
#                 full_url = urljoin(base_url, download_url)
#                 self.image_urls.append(full_url)

#     def check_pages_in_each_thread(self, response):
#         if int(response.url[-1]) < self.post_page_id-1:
#             print('No more pages in this thread')
#             return
#         soup = BeautifulSoup(response.text, 'lxml')
#         self.extract_images(soup)
#         next_page_url = response.url[:-1] + str(self.post_page_id)
#         self.post_page_id += 1
#         print(next_page_url)
#         yield response.follow(next_page_url, callback=self.check_pages_in_each_thread)

#     def parse_thread(self, response):
#         self.post_page_id = 2
#         self.image_urls = []
#         soup = BeautifulSoup(response.text, 'lxml')
#         original_post_div = soup.find('div', class_='lia-message-body-content')
#         original_post_text = ' '.join(original_post_div.stripped_strings) if original_post_div else "Original post not found."
#         self.extract_images(soup)
        
#         num_people_same_issue = soup.find('a', class_='lia-link-navigation lia-rating-value-summary')
#         num_people_same_issue = num_people_same_issue.text[0] if num_people_same_issue else 0

#         link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.post_page_id)
#         next_page = response.css(link).get()
#         if next_page is not None:
#             self.post_page_id += 1
#             yield response.follow(next_page, callback=self.check_pages_in_each_thread)

#         if not self.image_urls:
#             return

#         item = BugReportItem()
#         item['description'] = original_post_text
#         item['image_urls'] = self.image_urls
#         item['original_post_url'] = response.url
#         try:
#             item['num_people_has_same_issue'] = int(num_people_same_issue)
#         except ValueError:
#             item['num_people_has_same_issue'] = 0
#         item['images_names'] = []

#         yield item

#     def parse(self, response):
#         thread_links = response.css('a.page-link.lia-link-navigation.lia-custom-event::attr(href)').getall()
#         for link in thread_links:
#             yield response.follow(link, self.parse_thread)
        
#         link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.main_page_id)
#         self.main_page_id += 1
#         next_page = response.css(link).get()
#         if next_page is not None:
#             yield response.follow(next_page, callback=self.parse)






# import scrapy
# from bs4 import BeautifulSoup
# from bug_report_scraper.items import BugReportItem
# from urllib.parse import urljoin

# class BugSpider(scrapy.Spider):
#     name = 'bug_spider'
#     domain = 'https://answers.ea.com'
#     main_page_id = 2
#     post_page_id = 2
#     item = BugReportItem()

#     def __init__(self, start_urls=None, game_name=None, *args, **kwargs):
#         super(BugSpider, self).__init__(*args, **kwargs)
#         if start_urls:
#             self.start_urls = [start_urls]
#         self.game_name = game_name

#     def extract_images(self, soup):
#         images = soup.find_all('a', class_='lia-link-navigation attachment-link')
#         base_url = self.domain
#         for img in images:
#             download_url = img.find('span')['li-download-url']
#             if download_url.split('.')[-1].lower() in ['png', 'jpg', 'jpeg', 'bmp', 'heic']:
#                 full_url = urljoin(base_url, download_url)
#                 print(full_url)
#                 self.item['image_urls'].append(full_url)

#     def parse_thread(self, response):
#         self.item['image_urls'] = []
#         print('re-initialize image_urls')
#         self.post_page_id = 2


#         self.item['original_post_url'] = response.url

#         soup = BeautifulSoup(response.text, 'lxml')
         
#         original_post_div = soup.find('div', class_='lia-message-body-content')
#         original_post_text = ' '.join(original_post_div.stripped_strings) if original_post_div else "Original post not found."
#         self.item['description'] = original_post_text

#         self.extract_images(soup)
        
#         num_people_same_issue = soup.find('a', class_='lia-link-navigation lia-rating-value-summary')
#         num_people_same_issue = num_people_same_issue.text[0] if num_people_same_issue else 0
#         try:
#             self.item['num_people_has_same_issue'] = int(num_people_same_issue)
#         except ValueError:
#             self.item['num_people_has_same_issue'] = 0
#         self.item['images_names'] = []

#         link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.post_page_id)
#         next_page = response.css(link).get()
#         if next_page is not None:
#             print('next page id:', self.post_page_id)
#             print('url:', next_page)
#             self.post_page_id += 1
            
#             yield response.follow(next_page, callback=self.check_pages_in_each_thread)

#         if not self.item['image_urls']:
#             return
#         else:
#             yield self.item

#     def check_pages_in_each_thread(self, response):
#         # we are now in the next page of the thread
#         soup = BeautifulSoup(response.text, 'lxml')
#         #grab content of this page
#         self.extract_images(soup)

#         link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.post_page_id)
#         next_page = response.css(link).get() 
#         if next_page is not None:
#             print('next page id:', self.post_page_id)
#             print('url:', next_page)
#             self.post_page_id += 1
#             yield response.follow(next_page, callback=self.check_pages_in_each_thread)
       


#     def parse(self, response):
#         thread_links = response.css('a.page-link.lia-link-navigation.lia-custom-event::attr(href)').getall()
#         for link in thread_links:
#             yield response.follow(link, self.parse_thread)
        
#         link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.main_page_id)
#         self.main_page_id += 1
#         # next_page = response.css(link).get()
#         # if next_page is not None:
#         #     yield response.follow(next_page, callback=self.parse)



import scrapy
from bs4 import BeautifulSoup
from bug_report_scraper.items import BugReportItem
from urllib.parse import urljoin

class BugSpider(scrapy.Spider):
    name = 'bug_spider'
    domain = 'https://answers.ea.com'
    main_page_id = 2
    post_page_id = 2

    def __init__(self, start_urls=None, game_name=None, *args, **kwargs):
        super(BugSpider, self).__init__(*args, **kwargs)
        if start_urls:
            self.start_urls = [start_urls]
        self.game_name = game_name
        self.image_urls = []

    def extract_images(self, soup):
        images = soup.find_all('a', class_='lia-link-navigation attachment-link')
        base_url = self.domain
        for img in images:
            download_url = img.find('span')['li-download-url']
            if download_url.split('.')[-1].lower() in ['png', 'jpg', 'jpeg', 'bmp', 'heic']:
                full_url = urljoin(base_url, download_url)
                print(full_url)
                self.image_urls.append(full_url)

    def parse_thread(self, response):
        item = BugReportItem()
        item['image_urls'] = []
        self.image_urls = []
        print('re-initialize image_urls')
        self.post_page_id = 2

        item['original_post_url'] = response.url

        soup = BeautifulSoup(response.text, 'lxml')

        original_post_div = soup.find('div', class_='lia-message-body-content')
        original_post_text = ' '.join(original_post_div.stripped_strings) if original_post_div else "Original post not found."
        item['description'] = original_post_text

        self.extract_images(soup)

        num_people_same_issue = soup.find('a', class_='lia-link-navigation lia-rating-value-summary')
        num_people_same_issue = num_people_same_issue.text[0] if num_people_same_issue else 0
        try:
            item['num_people_has_same_issue'] = int(num_people_same_issue)
        except ValueError:
            item['num_people_has_same_issue'] = 0
        item['images_names'] = []

        link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.post_page_id)
        next_page = response.css(link).get()
        if next_page is not None:
            print('next page id:', self.post_page_id)
            print('url:', next_page)
            self.post_page_id += 1

            request = response.follow(next_page, callback=self.check_pages_in_each_thread)
            request.meta['item'] = item
            yield request
        else:
            item['image_urls'] = self.image_urls
            if not item['image_urls']:
                return
            yield item

    def check_pages_in_each_thread(self, response):
        # we are now in the next page of the thread
        item = response.meta['item']
        soup = BeautifulSoup(response.text, 'lxml')
        #grab content of this page
        self.extract_images(soup)

        link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.post_page_id)
        next_page = response.css(link).get() 
        if next_page is not None:
            print('next page id:', self.post_page_id)
            print('url:', next_page)
            self.post_page_id += 1
            request = response.follow(next_page, callback=self.check_pages_in_each_thread)
            request.meta['item'] = item
            yield request
        else:
            item['image_urls'] = self.image_urls
            yield item

    def parse(self, response):
        thread_links = response.css('a.page-link.lia-link-navigation.lia-custom-event::attr(href)').getall()
        for link in thread_links:
            yield response.follow(link, self.parse_thread)

        link = 'a.lia-link-navigation.lia-js-data-pageNum-{id}.lia-custom-event::attr(href)'.format(id=self.main_page_id)
        self.main_page_id += 1
        next_page = response.css(link).get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
