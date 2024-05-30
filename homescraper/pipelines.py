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
            if field == 'basic_details':
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
        Builder['coop_rate'] =coop_rate
        Builder['subdivision_'] = []
        for item in self.items:
            i=0
            for subdivision in Builder['subdivision_']:
                subdivision = subdivision['subdivision']
                if item['address_map']['City'] == subdivision['subdivision_name']:
                    i = 1
                    break
            if i == 0:
                Subdivision = homescraper.items.Subdivision()
                Subdivision.initialize_defaults()
                SubdivisionFlyer = homescraper.items.SubdivisionFlyer()
                SubdivisionFlyer.initialize_defaults()
                flyer = homescraper.items.Flyer()
                flyer['subdivision_flyer'] = SubdivisionFlyer
                SubImage = homescraper.items.SubImage()
                SubImage.initialize_defaults()
                image = homescraper.items.Image()
                image['sub_image'] = SubImage
                SubVideo = homescraper.items.SubVideo()
                SubVideo.initialize_defaults()
                video = homescraper.items.Video()
                video['sub_video'] = SubVideo
                Promotion = homescraper.items.Promotion()
                Promotion.initialize_defaults()
                Subdivision['subdivision_flyer_'] = flyer
                Subdivision['sub_image_'] = image
                Subdivision['sub_video_'] = video
                Subdivision['promotion'] = Promotion

                Subdivision['subdivision_website'] = item['cities'][item['address_map']['City'].strip()]
                Subdivision['subdivision_name'] = item['address_map']['City']
                Subdivision['subdivision_state_code'] = item['address_map']['State']
                Subdivision['subdivision_city_name'] = item['address_map']['City']
                Subdivision['subdivision_zip'] = item['address_map']['Zip_Code']
                Subdivision['subdivision_address'] = item['address_map']['Zip_Code'] + ' ' +item['address_map']["Street"]
                Subdivision['subdivision_latitude'] = item['address_map']['latitude']
                Subdivision['subdivision_longitude'] = item['address_map']['longitude']
                if item["basic_details"]['Property_Type'] == 'Multi-Family':
                    Subdivision['subdivision_property_type_id'] = 2
                elif item["basic_details"]['Property_Type'] == 'Single Family':
                    Subdivision['subdivision_property_type_id'] = 1
                else:
                    Subdivision['subdivision_property_type_id'] = 23
                Subdivision['subdivision_property_'] = []
                division = homescraper.items.Division()
                division['subdivision'] = Subdivision
                Builder['subdivision_'].append(division)
            else:
                i=0
        
        for item in self.items:
            SubdivisionProperty = homescraper.items.SubdivisionProperty()
            SubdivisionProperty.initialize_defaults()
            PropertyFloorPlanImage = homescraper.items.PropertyFloorPlanImage()
            PropertyFloorPlanImage.initialize_defaults()
            PropertyFloorPlanImage['property_floor_plan_image_url'] = item['blueprint'][0]
            floor_plan = homescraper.items.FloorPlan()
            floor_plan['property_floor_plan_image'] = PropertyFloorPlanImage
            PropertyElevationImage = homescraper.items.PropertyElevationImage()
            PropertyElevationImage.initialize_defaults()
            elevation = homescraper.items.Elevation()
            elevation['property_elevation_image'] = PropertyElevationImage
            Promotion = homescraper.items.Promotion()
            Promotion.initialize_defaults()
            SubdivisionProperty['promotion'] = Promotion
            SubdivisionProperty['property_floor_plan_image_'] = floor_plan
            SubdivisionProperty['property_elevation_image_'] = elevation

            SubdivisionProperty['property_address'] = item['address_map']['address'].split(',')[0]
            SubdivisionProperty['property_zip'] = item['address_map']['Zip_Code']
            SubdivisionProperty['property_latitude'] = item['address_map']['latitude']
            SubdivisionProperty['property_longitude'] = item['address_map']['longitude']
            SubdivisionProperty['property_price'] = item["basic_details"]["Price"].replace(',','')
            if item["basic_details"]['Status'] == "Completed":
                SubdivisionProperty['property_stage_id'] = 'COM'
            else:
                SubdivisionProperty['property_stage_id'] = 'UNK'
            if "Year_Built" in item["basic_details"].keys():
                SubdivisionProperty['completion_date'] = item["basic_details"]["Year_Built"]+'-01-01'
            if item["basic_details"]['Property_Type'] == 'Multi-Family':
                    SubdivisionProperty['property_type_id'] = 2
            elif item["basic_details"]['Property_Type'] == 'Single Family':
                    SubdivisionProperty['property_type_id'] = 1
            else:
                    SubdivisionProperty['property_type_id'] = 23
            SubdivisionProperty['property_remarks'] = '. '.join(item["features"])
            SubdivisionProperty['property_baths'] = item["basic_details"]["Bathrooms"]
            SubdivisionProperty['property_beds'] = item["basic_details"]["Bedrooms"]
            SubdivisionProperty['property_garage'] = item["basic_details"]["Garage"]
            SubdivisionProperty['property_square_feet'] = item["basic_details"]["Square_Footage"].replace(',','')
            if item['video_link'] is not None:
                SubdivisionProperty['property_virtual_tour'] =item['video_link']
            else:
                SubdivisionProperty['property_virtual_tour'] = ""
            SubdivisionProperty['property_exterior_interior_image_'] = []
            for image in item['images']:
               Image =  homescraper.items.PropertyExteriorInteriorImage()
               Image.initialize_defaults()
               Image['property_interior_image_url'] =image
               img = homescraper.items.ExteriorInterior()
               img['property_exterior_interior_image'] = Image
               SubdivisionProperty['property_exterior_interior_image_'].append(img)
            for subdivision in Builder['subdivision_']:
                 subdivision = subdivision['subdivision']
                 if item['address_map']['City'] == subdivision['subdivision_name']:
                    property = homescraper.items.Property()
                    property['subdivision_property'] = SubdivisionProperty
                    subdivision['subdivision_property_'].append(property)
                    break
        welcome = homescraper.items.Welcome10()
        welcome['builder'] = Builder
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

        #code to convert snake case to pascal case
        def snake_to_pascal(text):
            parts = text.split('_')
            return ''.join(part.capitalize() for part in parts)
        def convert_xml_tags_to_pascal_case(root):
            root.tag = snake_to_pascal(root.tag)
            for elem in root.iter():
                elem.tag = snake_to_pascal(elem.tag)
        convert_xml_tags_to_pascal_case(xml)

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


        
