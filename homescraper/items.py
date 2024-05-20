import scrapy
class HomeItem(scrapy.Item):
    name = scrapy.Field()
    basic_details = scrapy.Field()
    address_map = scrapy.Field()
    features = scrapy.Field()
    images = scrapy.Field()
    video_link = scrapy.Field()
    blueprint = scrapy.Field()

class CoopRate(scrapy.Item):
    honors_coop_rate = scrapy.Field(default="True")
    coop_rate_pct = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Promotion(scrapy.Item):
    promo_id = scrapy.Field(default="")
    promo_type = scrapy.Field(default="")
    promo_headline = scrapy.Field(default="")
    promo_description = scrapy.Field(default="")
    promo_url = scrapy.Field(default="")
    promo_start_date = scrapy.Field(default="")
    promo_end_date = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class SubImage(scrapy.Item):
    sub_image_url = scrapy.Field(default="")
    sub_image_caption = scrapy.Field(default="")
    sub_image_url_content_type = scrapy.Field(default="")
    sub_image_order_by = scrapy.Field(default="")
    main_flag = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class SubVideo(scrapy.Item):
    sub_video_url = scrapy.Field(default="")
    sub_video_caption = scrapy.Field(default="")
    sub_video_url_content_type = scrapy.Field(default="")
    sub_video_order_by = scrapy.Field(default="")
    main_flag = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class SubdivisionFlyer(scrapy.Item):
    subdivision_flyer_image_url = scrapy.Field(default="")
    subdivision_flyer_description = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class PropertyElevationImage(scrapy.Item):
    property_elevation_image_url = scrapy.Field(default="")
    property_elevation_image_description = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class PropertyExteriorInteriorImage(scrapy.Item):
    property_interior_image_url = scrapy.Field(default="")
    property_interior_image_description = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class PropertyFloorPlanImage(scrapy.Item):
    property_floor_plan_image_url = scrapy.Field(default="")
    property_floor_plan_image_description = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class SubdivisionProperty(scrapy.Item):
    property_id = scrapy.Field(default="")
    property_address = scrapy.Field()
    property_zip = scrapy.Field()
    property_price = scrapy.Field()
    property_latitude = scrapy.Field()
    property_longitude = scrapy.Field()
    property_class_code = scrapy.Field(default='PROPERTY')
    property_status_id = scrapy.Field(default='AV')
    property_stage_id = scrapy.Field()
    completion_date = scrapy.Field(default = "")
    property_type_id = scrapy.Field()
    property_remarks = scrapy.Field()
    property_show_directions = scrapy.Field(default="")
    property_contact1_name = scrapy.Field(default='Sales representative')
    property_contact1_phone = scrapy.Field(default='(904) 831 8050')
    property_contact1_phone_alt = scrapy.Field(default="")
    property_contact2_name = scrapy.Field(default="")
    property_contact2_phone = scrapy.Field(default="")
    property_contact2_phone_alt = scrapy.Field(default="")
    property_contact_email = scrapy.Field(default='newhomes@sihomesfl.com')
    property_driving_directions = scrapy.Field(default="")
    property_baths = scrapy.Field()
    property_half_baths = scrapy.Field(default=0)
    property_beds = scrapy.Field()
    property_living = scrapy.Field()
    property_dining = scrapy.Field()
    property_other_rooms = scrapy.Field(default="")
    property_stories = scrapy.Field()
    property_master = scrapy.Field(default="")
    property_garage = scrapy.Field()
    property_school_district_leaid = scrapy.Field(default = ["",""])
    property_schools_ncesid = scrapy.Field(default = ["",""])
    property_square_feet = scrapy.Field()
    lot_size = scrapy.Field(default="")
    lot_description = scrapy.Field(default="")
    floor_plan_number = scrapy.Field(default="")
    floor_plan_name = scrapy.Field(default="")
    propertycommunity_type_id = scrapy.Field(default=11)
    property_virtual_tour = scrapy.Field(default = "")
    property_plan_view_url = scrapy.Field()
    property_school_comments = scrapy.Field(default="")
    property_has_hoa = scrapy.Field(default="True")
    property_hoa_fee = scrapy.Field(default="")
    property_hoa_billing_period = scrapy.Field(default="")
    property_floor_plan_image = scrapy.Field(default=PropertyFloorPlanImage())
    property_elevation_image = scrapy.Field(default=PropertyElevationImage())
    property_exterior_interior_image = scrapy.Field()
    promotion = scrapy.Field(default=Promotion())

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Subdivision(scrapy.Item):
    subdivision_name = scrapy.Field()
    subdivision_state_code = scrapy.Field()
    subdivision_city_name = scrapy.Field()
    subdivision_number = scrapy.Field(default="")
    community_status_type_code = scrapy.Field()
    community_min_price = scrapy.Field(default="")
    community_max_price = scrapy.Field(default="")
    subdivision_zip = scrapy.Field()
    subdivision_address = scrapy.Field()
    builder_brand_name = scrapy.Field(default='SI Homes')
    subdivision_latitude = scrapy.Field()
    subdivision_longitude = scrapy.Field()
    subdivision_contact1_name = scrapy.Field(default='Sales representative')
    subdivision_contact1_phone = scrapy.Field(default='(904) 831 8050')
    subdivision_contact1_phone_alt = scrapy.Field(default="")
    subdivision_contact2_name = scrapy.Field(default="")
    subdivision_contact2_phone = scrapy.Field(default="")
    subdivision_contact2_phone_alt = scrapy.Field(default="")
    subdivision_contact_email = scrapy.Field(default='newhomes@sihomesfl.com')
    subdivision_description = scrapy.Field(default="")
    subdivision_show_directions = scrapy.Field(default="")
    subdivision_driving_directions = scrapy.Field(default="")
    subdivision_property_type_id = scrapy.Field()
    subdivision_community_type_id = scrapy.Field(default=11)
    subdivision_school_district_leaid = scrapy.Field(default=["",""])
    subdivision_schools_ncesid = scrapy.Field(default=["",""])
    subdivision_school_comments = scrapy.Field(default="")
    subdivision_has_hoa = scrapy.Field(default="True")
    subdivision_hoa_fee = scrapy.Field(default="")
    subdivision_hoa_billing_period = scrapy.Field(default="")
    subdivision_notes = scrapy.Field(default="This is a note")
    subdivision_website = scrapy.Field(default="")
    subdivision_property = scrapy.Field()
    subdivision_flyer = scrapy.Field(default=SubdivisionFlyer())
    sub_image = scrapy.Field(default=SubImage())
    sub_video = scrapy.Field(default=SubVideo())
    promotion = scrapy.Field(default=Promotion())

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Builder(scrapy.Item):
    coop_rate = scrapy.Field(default=CoopRate())
    subdivision = scrapy.Field()
    xmlns_p1 = scrapy.Field(default='SubdivisionSchema')
    xmlns_xsi = scrapy.Field(default = 'http://www.w3.org/2001/XMLSchema-instance')

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Welcome10(scrapy.Item):
    builder = scrapy.Field()