from itemadapter import ItemAdapter
import xml.etree.ElementTree as ET
import ast
import copy
import json
from json2xml import json2xml
import homescraper.items 
class HomescraperPipeline:
    def __init__(self):
        self.items = []
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field in field_names:
            if field == 'BasicDetails':
                value = adapter.get(field)
                for key in value.keys():
                    value[key] = value[key].replace('$', '').strip()
                    value[key] = value[key].rstrip('Sqft').strip()
                    if key == 'Status' and (value[key] == "Completed" or value[key] == "Under Construction"):
                        self.items.append(copy.deepcopy(item))
                adapter[field] = value
        return item
        
    
    def close_spider(self,spider):
        Builder = homescraper.items.Builder()
        Builder.initialize_defaults()
        coop_rate = homescraper.items.CoopRate()
        coop_rate.initialize_defaults()
        Builder['CoopRate'] =coop_rate
        Builder['Subdivision_'] = []
        for item in self.items:
            i=0
            for subdivision in Builder['Subdivision_']:
                subdivision = subdivision['Subdivision']
                if item['AddressMap']['City'] == subdivision['SubdivisionName']:
                    i = 1
                    break
            if i == 0:
                Subdivision = homescraper.items.Subdivision()
                Subdivision.initialize_defaults()
                SubdivisionFlyer = homescraper.items.SubdivisionFlyer()
                SubdivisionFlyer.initialize_defaults()
                flyer = homescraper.items.Flyer()
                flyer['SubdivisionFlyer'] = SubdivisionFlyer
                SubImage = homescraper.items.SubImage()
                SubImage.initialize_defaults()
                image = homescraper.items.Image()
                image['SubImage'] = SubImage
                SubVideo = homescraper.items.SubVideo()
                SubVideo.initialize_defaults()
                video = homescraper.items.Video()
                video['SubVideo'] = SubVideo
                Promotion = homescraper.items.Promotion()
                Promotion.initialize_defaults()
                Subdivision['SubdivisionFlyer_'] = flyer
                Subdivision['SubImage_'] = image
                Subdivision['SubVideo_'] = video
                Subdivision['Promotion'] = Promotion

                Subdivision['SubdivisionWebsite'] = item['Cities'][item['AddressMap']['City'].strip()]
                Subdivision['SubdivisionName'] = item['AddressMap']['City']
                Subdivision['SubdivisionStateCode'] = item['AddressMap']['State']
                Subdivision['SubdivisionCityName'] = item['AddressMap']['City']
                Subdivision['SubdivisionZip'] = item['AddressMap']['Zip_Code']
                Subdivision['SubdivisionAddress'] = item['AddressMap']['Zip_Code'] + ' ' +item['AddressMap']["Street"]
                Subdivision['SubdivisionLatitude'] = item['AddressMap']['latitude']
                Subdivision['SubdivisionLongitude'] = item['AddressMap']['longitude']
                if item["BasicDetails"]['Property_Type'] == 'Multi-Family':
                    Subdivision['SubdivisionPropertyTypeId'] = 2
                elif item["BasicDetails"]['Property_Type'] == 'Single Family':
                    Subdivision['SubdivisionPropertyTypeId'] = 1
                else:
                    Subdivision['SubdivisionPropertyTypeId'] = 23
                Subdivision['SubdivisionProperty_'] = []
                division = homescraper.items.Division()
                division['Subdivision'] = Subdivision
                Builder['Subdivision_'].append(division)
            else:
                i=0
        
        for item in self.items:
            SubdivisionProperty = homescraper.items.SubdivisionProperty()
            SubdivisionProperty.initialize_defaults()
            PropertyFloorPlanImage = homescraper.items.PropertyFloorPlanImage()
            PropertyFloorPlanImage.initialize_defaults()
            PropertyFloorPlanImage['PropertyFloorPlanImageUrl'] = item['Blueprint'][0]
            floor_plan = homescraper.items.FloorPlan()
            floor_plan['PropertyFloorPlanImage'] = PropertyFloorPlanImage
            PropertyElevationImage = homescraper.items.PropertyElevationImage()
            PropertyElevationImage.initialize_defaults()
            elevation = homescraper.items.Elevation()
            elevation['PropertyElevationImage'] = PropertyElevationImage
            Promotion = homescraper.items.Promotion()
            Promotion.initialize_defaults()
            SubdivisionProperty['Promotion'] = Promotion
            SubdivisionProperty['PropertyFloorPlanImage_'] = floor_plan
            SubdivisionProperty['PropertyElevationImage_'] = elevation

            SubdivisionProperty['PropertyAddress'] = item['AddressMap']['address'].split(',')[0]
            SubdivisionProperty['PropertyZip'] = item['AddressMap']['Zip_Code']
            SubdivisionProperty['PropertyLatitude'] = item['AddressMap']['latitude']
            SubdivisionProperty['PropertyLongitude'] = item['AddressMap']['longitude']
            SubdivisionProperty['PropertyPrice'] = item["BasicDetails"]["Price"].replace(',','')
            if item['BasicDetails']['Status'] == "Completed":
                SubdivisionProperty['PropertyStageId'] = 'COM'
            else:
                SubdivisionProperty['PropertyStageId'] = 'UNK'
            if "Year_Built" in item['BasicDetails'].keys():
                SubdivisionProperty['CompletionDate'] = item['BasicDetails']["Year_Built"]+'-01-01'
            if item['BasicDetails']['Property_Type'] == 'Multi-Family':
                    SubdivisionProperty['PropertyTypeId'] = 2
            elif item['BasicDetails']['Property_Type'] == 'Single Family':
                    SubdivisionProperty['PropertyTypeId'] = 1
            else:
                    SubdivisionProperty['PropertyTypeId'] = 23
            SubdivisionProperty['PropertyRemarks'] = '. '.join(item["Features"])
            SubdivisionProperty['PropertyBaths'] = item['BasicDetails']["Bathrooms"]
            SubdivisionProperty['PropertyBeds'] = item['BasicDetails']["Bedrooms"]
            SubdivisionProperty['PropertyGarage'] = item['BasicDetails']["Garage"]
            SubdivisionProperty['PropertySquareFeet'] = item['BasicDetails']["Square_Footage"].replace(',','')
            if item['VideoLink'] is not None:
                SubdivisionProperty['PropertyVirtualTour'] =item['VideoLink']
            else:
                SubdivisionProperty['PropertyVirtualTour'] = ""
            SubdivisionProperty['PropertyExteriorInteriorImage_'] = []
            for image in item['Images']:
               Image =  homescraper.items.PropertyExteriorInteriorImage()
               Image.initialize_defaults()
               Image['PropertyInteriorImageUrl'] =image
               img = homescraper.items.ExteriorInterior()
               img['PropertyExteriorInteriorImage'] = Image
               SubdivisionProperty['PropertyExteriorInteriorImage_'].append(img)
            for subdivision in Builder['Subdivision_']:
                 subdivision = subdivision['Subdivision']
                 if item['AddressMap']['City'] == subdivision['SubdivisionName']:
                    property = homescraper.items.Property()
                    property['SubdivisionProperty'] = SubdivisionProperty
                    subdivision['SubdivisionProperty_'].append(property)
                    break
        welcome = homescraper.items.Welcome10()
        welcome['Builder'] = Builder
        dt = ast.literal_eval(str(welcome))
        with open('data.json','w') as f:
            json.dump(dt,f,indent=4)
        xml = json2xml.Json2xml(dt,item_wrap=False).to_xml()
        root = ET.fromstring(xml)
        xml = list(root)[0]

        def remove_undesired_elements(parent):
            if 'type' in parent.attrib:
                del parent.attrib['type']
            for elem in list(parent):
                remove_undesired_elements(elem)
                if elem.tag.endswith('_'):
                    index = list(parent).index(elem)
                    for child in reversed(list(elem)):
                        parent.insert(index, child)
                    parent.remove(elem)
        remove_undesired_elements(xml)

        #code to remove unnecessary attributes
        # def remove_type_attributes(element):
        #     if 'type' in element.attrib:
        #         del element.attrib['type']
        #     for child in element:
        #         remove_type_attributes(child)
        # remove_type_attributes(xml)

        xml = ET.tostring(xml, encoding='unicode')
        with open('data.xml','w') as f:
            f.write('<?xml version="1.0" ?>\n' + xml)

        
        pass


        
