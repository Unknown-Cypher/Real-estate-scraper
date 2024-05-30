import scrapy
from homescraper.items import HomeItem
import re

class HomespiderSpider(scrapy.Spider):
    name = "homespider"
    allowed_domains = ["southernimpressionhomes.com"]
    start_urls = ["https://southernimpressionhomes.com/properties/"]
    output_data = []
    
    def __init__(self, *args, **kwargs):
        super(HomespiderSpider, self).__init__(*args, **kwargs)
        self.home_item = HomeItem()
    
    def parse(self, response):
        l1 = response.css('li.menu-item-object-page li.menu-item-type-custom a::text').extract()
        l2 = response.css('li.menu-item-object-page li.menu-item-type-custom a::attr(href)').extract()
        self.home_item['cities'] = {key:value for key,value in zip(l1,l2)}
        # Extracting links to individual home pages
        home_links = response.css('a.view_detail::attr(href)').extract()
        del home_links[1::2]
        for link in home_links:
            yield response.follow(link,callback = self.parse_home)
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not '#':
            yield response.follow(next_page,callback=self.parse)

    
    

    def parse_home(self, response):
        # Removes html elemnts from the strings extracted
        def clean_html(data):
          clean = re.compile('<.*?>')
          data = re.sub(clean,'',data)
          return data
        data = response.css('div.rows').extract()
        data = [clean_html(x) for x in data]
        features = response.css('div.wpl-column.rows.feature').extract()
        features = [clean_html(x) for x in features]
        basic_details = response.css('div.wpl_category_1 div.wpl_prp_show_detail_boxes_cont div').extract()
        basic_details = [clean_html(x) for x in basic_details]
        name = response.css('h1.title_text::text').get()
        video_link = response.css('li.wpl_videos_video iframe::attr(src)').get()
        images = response.xpath("//div[@id = 'wpl_gallery_wrapper-3']//li/@data-src").extract()
        blueprint = response.xpath("//div[@id = 'wpl_gallery_wrapper-101']//li/@data-src").extract()
        address_map = {entry.split(':')[0].strip().replace(' ', '_'): entry.split(':')[1] for entry in data[len(features):-len(basic_details)]}
        address_map ['latitude'] = float(response.text.split('googlemap_lt":')[1].split(',')[0])
        address_map ['longitude'] = float(response.text.split('googlemap_ln":')[1].split(',')[0])
        address_map['address'] = response.css('span.wpl-location::text').get()
        
        self.home_item['name']=name
        self.home_item['basic_details']={entry.split(':')[0].strip().replace(' ', '_'): entry.split(':')[1] for entry in basic_details}
        self.home_item['address_map']=address_map
        self.home_item['features']=features
        self.home_item['images']=images
        self.home_item['video_link']=video_link
        self.home_item['blueprint']=blueprint
        yield self.home_item

