# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BugReportItem(scrapy.Item):
    image_urls = scrapy.Field()
    images_names = scrapy.Field()#left empty, the name will be generated automatically in the next process step when the image is downloaded
    original_post_url = scrapy.Field()
    description = scrapy.Field()
    num_pepole_has_same_issue = scrapy.Field()

