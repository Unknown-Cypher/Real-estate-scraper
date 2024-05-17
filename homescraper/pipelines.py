from itemadapter import ItemAdapter
import json
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
                        self.items.append(item)
                adapter[field] = value
        return item
        
    
    def close_spider(self,spider):
        Builder = homescraper.items.Builder()
        Builder['subdivision'] = []
        for item in self.items:
            i=0
            for subdivision in Builder['subdivision']:
                if item['address_map']['City'] == subdivision['subdivision_name']:
                    i = 1
                    break
            if i == 0:
                Subdivision = homescraper.items.Subdivision()
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
                Subdivision['subdivision_property'] = []
                Builder['subdivision'].append(Subdivision)
            else:
                i=0
        
        for item in self.items:
            SubdivisionProperty = homescraper.items.SubdivisionProperty()
            SubdivisionProperty['property_address'] = item['address_map']['address']
            SubdivisionProperty['property_zip'] = item['address_map']['Zip_Code']
            SubdivisionProperty['property_latitude'] = item['address_map']['latitude']
            SubdivisionProperty['property_longitude'] = item['address_map']['longitude']
            SubdivisionProperty['property_price'] = item["basic_details"]["Price"]
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
            SubdivisionProperty['property_living'] =None
            SubdivisionProperty['property_dining'] = None
            SubdivisionProperty['property_stories'] = None
            SubdivisionProperty['property_garage'] = item["basic_details"]["Garage"]
            SubdivisionProperty['property_schools_ncesid'] = None
            SubdivisionProperty['property_square_feet'] = item["basic_details"]["Square_Footage"]
            SubdivisionProperty['property_virtual_tour'] = item['video_link']
            SubdivisionProperty['property_plan_view_url'] = item['blueprint'][0]
            SubdivisionProperty['property_exterior_interior_image'] = []
            for image in item['images']:
               Image =  homescraper.items.PropertyExteriorInteriorImage()
               Image['property_interior_image_url'] = image
               SubdivisionProperty['property_exterior_interior_image'].append(Image)
            for subdivision in Builder['subdivision']:
                 if item['address_map']['City'] == subdivision['subdivision_name']:
                    subdivision['subdivision_property'].append(SubdivisionProperty)
                    break
            print(item['basic_details'].keys())
        

        pass


        
