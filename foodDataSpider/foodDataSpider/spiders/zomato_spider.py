import simplejson as json

import scrapy
import requests
import re
import chompjs
from ..items import *
from .Restaurant import *


class ZomatoSpiderSpider(scrapy.Spider):
    name = 'zomato_spider'
    allowed_domains = ['zomato.com']
    delivery_subzone = 3655
    regex = r"JSON\.parse\(.*\)"
    db_name = 'zomatoDB'
    localityUrl = ""
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    infinite_scroll_url = "https://www.zomato.com/webroutes/search/home?context=delivery" \
                          "&filters={{%22searchMetadata%22:{{%22previousSearchParams%22:%22" \
                          "{{\%22PreviousSearchFilter\%22:[\%22{{\\\%22category_context\\" \
                          "\%22:\\\%22delivery_home\\\%22}}\%22]}}%22,%22postbackParams%22" \
                          ":%22{{\%22processed_chain_ids\%22:{processed_ids},\%22shown_res_count\%22:{show_res_count}%22,%22totalResults%22:" \
                          "{total_result},%22hasMore%22:{isHasMore},%22getInactive%22:{isGetInactive},%22dineoutAdsMetaData%22" \
                          ":,%22appliedFilter%22:[{{%22filterType%22:%22category_sheet%22,%22filterValue" \
                          "%22:%22delivery_home%22,%22isHidden%22:true,%22isApplied%22:true," \
                          "%22postKey%22:%22{{\%22category_context\%22:\%22delivery_home\%22}}%" \
                          "22}}]}}&addressId={address_id}&entityId={entity_id}&entityType={entity_type}&locationType=&isOrderLocation={isOrderLocation}" \
                          "&cityId={cityId}&latitude={latitude}&longitude={longitude}&userDefinedLatitude" \
                          "={userDefinedLatitude}&userDefinedLongitude={userDefinedLongitude}&entityName={entityName}&orderLocationName={orderLocationName}" \
                          "&cityName={cityName}&" \
                          "countryId={countryId}&countryName={countryName}&displayTitle={displayTitle}&o2Serviceable={o2Serviceable}" \
                          "&placeId={placeId}&cellId={cellId}&deliverySubzoneId={deliverySubzoneId}" \
                          "&placeType={placeType}&placeName={placeName}&isO2City={isO2City}" \
                          "&fetchFromGoogle={fetchFromGoogle}&isO2OnlyCity={isO2OnlyCity}&"
    start_urls = [
        # 'https://www.zomato.com/bangalore/ishta-upahar-ulsoor/order'
        'https://www.zomato.com/bangalore'
    ]

    def parse(self, response, **kwargs):
        # client = MongoClient('localhost', 27017)
        # db = client[self.db_name]
        # collection = db['restaurants']
        # self.parseDish(response)
        localities = LocalitiesItem()
        links = self.cleanLocalityLinks(self.getLocalities(response))
        print("********** DATA START ***********")
        locality = links[0].split("/")[-1]
        self.localityUrl = '/bangalore/' + locality
        yield response.follow(links[0], self.parse_restaurants)
        # for link in links:
        #     locality = link.split("/")[-1]
        #     self.localityUrl = '/bangalore/' + locality
        #     yield response.follow(link, self.parse_restaurants)

    def parseDish(self, response):
        # nameList = response.css('.fqvQEo+ .fqvQEo .ezKciv').css('::text').extract()
        # ratingAndVotes = response.css('.ezKciv+ .ioFTDV').css('::text').extract()
        # openNowAndTiming = response.css('.gXGhgv span').css('::text').extract()
        # price = response.css('.fqvQEo+ .fqvQEo .cCiQWA').css('::text').extract()
        script_data = response.css('script::text').extract()
        index = 0
        matchList = list()
        found = False
        json_text = ""
        for i in script_data:
            matches = re.finditer(self.regex, i, re.MULTILINE)
            matchList = list(matches)
            if len(matchList) > 0:
                found = True
                json_text = i
                break
            else:
                index += 1

        if str != "":
            matches = re.finditer(self.regex, json_text, re.MULTILINE)

            for matchNum, match in enumerate(matches, start=1):
                loaded_data = str(match.group()).replace("JSON.parse", "")
                data_len = len(loaded_data)
                loaded_data = loaded_data[1:data_len - 1]
                data = json.loads(loaded_data)
                new_data = json.loads(data)
                print(new_data)

    def cleanLists(self, list):
        for element in enumerate(list):
            list[element[0]] = ' '.join(element[1].split())
        return list

    def addDictToDB(self, restaurant):
        self.collection.insert(restaurant)

    def cleanLocalityLinks(self, links):
        corrected_links = list()
        for link in links:
            if link.startswith("https") and link.endswith("restaurants"):
                corrected_links.append(link.strip())
        return corrected_links

    def getLocalities(self, response):
        return response.css('.bke1zw-1').css('::attr(href)').extract()

    def parse_json(self, response):
        print("called")
        print(response)

    def parse_restaurants(self, response):
        conn = DataPipeline()
        script_data = response.css('script::text').extract()
        json_text = ""
        for i in script_data:
            matches = re.finditer(self.regex, i, re.MULTILINE)
            matchList = list(matches)
            if len(matchList) > 0:
                json_text = i
                break

        matches = re.finditer(self.regex, json_text, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            loaded_data = str(match.group()).replace("JSON.parse", "")
            data_len = len(loaded_data)
            loaded_data = loaded_data[1:data_len - 1]
            data = json.loads(loaded_data)
            new_data = json.loads(data)
            search_result = new_data['pages']['search'][self.localityUrl]['sections']['SECTION_SEARCH_RESULT']
            for result in search_result:
                if result['type'] == "restaurant":
                    conn.process_data(result)
            meta_info = new_data['pages']['search'][self.localityUrl]['sections']['SECTION_SEARCH_META_INFO'][
                'searchMetaData']
            processesd_info = json.loads(meta_info['postbackParams'])
            location_info = new_data['location']['currentLocation']
            # print(meta_info['hasMore'], type(meta_info['hasMore']))
            hasMore = meta_info['hasMore']
            while hasMore:
                url = self.infinite_scroll_url.format(processed_ids=processesd_info['processed_chain_ids'],
                                                      show_res_count=processesd_info['shown_res_count'],
                                                      total_result=meta_info['totalResults'],
                                                      isHasMore=meta_info['hasMore'],
                                                      isGetInactive=meta_info['getInactive'],
                                                      address_id=location_info['addressId'],
                                                      entity_id=location_info['entityId'],
                                                      entity_type=location_info['entityType'],
                                                      isOrderLocation=location_info['isOrderLocation'],
                                                      cityId=location_info['cityId'],
                                                      latitude=location_info['latitude'],
                                                      longitude=location_info['longitude'],
                                                      userDefinedLatitude=location_info['userDefinedLatitude'],
                                                      userDefinedLongitude=location_info['userDefinedLongitude'],
                                                      entityName=location_info['entityName'],
                                                      orderLocationName=location_info['orderLocationName'],
                                                      cityName=location_info['cityName'],
                                                      countryId=location_info['countryId'],
                                                      countryName=location_info['countryName'],
                                                      displayTitle=location_info['displayTitle'],
                                                      o2Serviceable=location_info['o2Serviceable'],
                                                      placeId=location_info['placeId'],
                                                      cellId=location_info['cellId'],
                                                      deliverySubzoneId=location_info['deliverySubzoneId'],
                                                      placeType=location_info['placeType'],
                                                      placeName=location_info['placeName'],
                                                      isO2City=location_info['isO2City'],
                                                      fetchFromGoogle=location_info['fetchFromGoogle'],
                                                      isO2OnlyCity=location_info['isO2OnlyCity'])
                print(url)
                r = requests.get(url, headers=self.headers)
                json_response = r.json()
                search_result = json_response['sections']['SECTION_SEARCH_RESULT']
                for result in search_result:
                    if result['type'] == 'restaurant':
                        conn.process_data(result)
                meta_info = json_response['sections']['SECTION_SEARCH_META_INFO']['searchMetaData']
                if 'processed_chain_ids' in json.loads(meta_info['postbackParams']):
                    processesd_info = json.loads(meta_info['postbackParams'])
                elif 'TotalRestaurantsShown' in json.loads(meta_info['postbackParams']):
                    processesd_info['shown_res_count'] = json.loads(meta_info['postbackParams'])['TotalRestaurantsShown']
                else:
                    pass
                hasMore = False
            conn.close_conn()
