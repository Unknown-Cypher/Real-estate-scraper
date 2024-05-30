import scrapy
import os
from dotenv import load_dotenv
load_dotenv()
class HomeItem(scrapy.Item):
    cities = scrapy.Field()
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

class Image(scrapy.Item):
    sub_image = scrapy.Field(default = SubImage())

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

class Video(scrapy.Item):
    sub_video = scrapy.Field(default = SubVideo())

class SubdivisionFlyer(scrapy.Item):
    subdivision_flyer_image_url = scrapy.Field(default="")
    subdivision_flyer_description = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Flyer(scrapy.Item):
    subdivision_flyer = scrapy.Field(default = SubdivisionFlyer())

class PropertyElevationImage(scrapy.Item):
    property_elevation_image_url = scrapy.Field(default="")
    property_elevation_image_description = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Elevation(scrapy.Item):
    property_elevation_image = scrapy.Field(default = PropertyElevationImage())

class PropertyExteriorInteriorImage(scrapy.Item):
    property_interior_image_url = scrapy.Field(default="")
    property_interior_image_description = scrapy.Field(default="")
    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class ExteriorInterior(scrapy.Item):
    property_exterior_interior_image = scrapy.Field(default = PropertyExteriorInteriorImage())

class PropertyFloorPlanImage(scrapy.Item):
    property_floor_plan_image_url = scrapy.Field(default="")
    property_floor_plan_image_description = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class FloorPlan(scrapy.Item):
    property_floor_plan_image = scrapy.Field(default = PropertyFloorPlanImage())
class SubdivisionProperty(scrapy.Item):
    property_id = scrapy.Field(default="")
    property_address = scrapy.Field()
    property_zip = scrapy.Field()
    property_price = scrapy.Field()
    property_latitude = scrapy.Field()
    property_longitude = scrapy.Field()
    property_class_code = scrapy.Field(default=os.getenv('PROPERTY_CLASS_CODE'))
    property_status_id = scrapy.Field(default=os.getenv('PROPERTY_STATUS_ID'))
    property_stage_id = scrapy.Field()
    completion_date = scrapy.Field(default="")
    property_type_id = scrapy.Field()
    property_remarks = scrapy.Field()
    property_show_directions = scrapy.Field(default="")
    property_contact1_name = scrapy.Field(default=os.getenv('PROPERTY_CONTACT1_NAME'))
    property_contact1_phone = scrapy.Field(default=os.getenv('PROPERTY_CONTACT1_PHONE'))
    property_contact1_phone_alt = scrapy.Field(default="")
    property_contact2_name = scrapy.Field(default="")
    property_contact2_phone = scrapy.Field(default="")
    property_contact2_phone_alt = scrapy.Field(default="")
    property_contact_email = scrapy.Field(default=os.getenv('PROPERTY_CONTACT_EMAIL'))
    property_driving_directions = scrapy.Field(default="")
    property_baths = scrapy.Field()
    property_half_baths = scrapy.Field(default=os.getenv('PROPERTY_HALF_BATHS'))
    property_beds = scrapy.Field()
    property_living = scrapy.Field()
    property_dining = scrapy.Field()
    property_other_rooms = scrapy.Field(default="")
    property_stories = scrapy.Field(default="")
    property_master = scrapy.Field(default="")
    property_garage = scrapy.Field()
    property_school_district_leaid = scrapy.Field(default = ["",""])
    property_schools_ncesid = scrapy.Field(default = ["",""])
    property_square_feet = scrapy.Field()
    lot_size = scrapy.Field(default="")
    lot_description = scrapy.Field(default="")
    floor_plan_number = scrapy.Field(default="")
    floor_plan_name = scrapy.Field(default="")
    propertycommunity_type_id = scrapy.Field(default=os.getenv('PROPERTYCOMMUNITY_TYPE_ID'))
    property_virtual_tour = scrapy.Field(default = "")
    property_plan_view_url = scrapy.Field(default = "")
    property_school_comments = scrapy.Field(default="")
    property_has_hoa = scrapy.Field(default=os.getenv('PROPERTY_HAS_HOA'))
    property_hoa_fee = scrapy.Field(default="")
    property_hoa_billing_period = scrapy.Field(default="")
    property_floor_plan_image_ = scrapy.Field(default=FloorPlan())
    property_elevation_image_ = scrapy.Field(default=Elevation())
    property_exterior_interior_image_ = scrapy.Field()
    promotion = scrapy.Field(default=Promotion())

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Property(scrapy.Item):
    subdivision_property = scrapy.Field(default = SubdivisionProperty())

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
    builder_brand_name = scrapy.Field(default=os.getenv('BUILDER_BRAND_NAME'))
    subdivision_latitude = scrapy.Field()
    subdivision_longitude = scrapy.Field()
    subdivision_contact1_name = scrapy.Field(default=os.getenv('SUBDIVISION_CONTACT1_NAME'))
    subdivision_contact1_phone = scrapy.Field(default=os.getenv('SUBDIVISION_CONTACT1_PHONE'))
    subdivision_contact1_phone_alt = scrapy.Field(default="")
    subdivision_contact2_name = scrapy.Field(default="")
    subdivision_contact2_phone = scrapy.Field(default="")
    subdivision_contact2_phone_alt = scrapy.Field(default="")
    subdivision_contact_email = scrapy.Field(default=os.getenv('SUBDIVISION_CONTACT_EMAIL'))
    subdivision_description = scrapy.Field(default="")
    subdivision_show_directions = scrapy.Field(default="")
    subdivision_driving_directions = scrapy.Field(default="")
    subdivision_property_type_id = scrapy.Field()
    subdivision_community_type_id = scrapy.Field(default=os.getenv('SUBDIVISION_COMMUNITY_TYPE_ID'))
    subdivision_school_district_leaid = scrapy.Field(default=["",""])
    subdivision_schools_ncesid = scrapy.Field(default=["",""])
    subdivision_school_comments = scrapy.Field(default="")
    subdivision_has_hoa = scrapy.Field(default=os.getenv('SUBDIVISION_HAS_HOA'))
    subdivision_hoa_fee = scrapy.Field(default="")
    subdivision_hoa_billing_period = scrapy.Field(default="")
    subdivision_notes = scrapy.Field(default=os.getenv('SUBDIVISION_NOTES'))
    subdivision_website = scrapy.Field(default="")
    subdivision_property_ = scrapy.Field()
    subdivision_flyer_ = scrapy.Field(default=Flyer())
    sub_image_ = scrapy.Field(default=Image())
    sub_video_ = scrapy.Field(default=Video())
    promotion = scrapy.Field(default=Promotion())

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Division(scrapy.Item):
    subdivision = scrapy.Field(default = Subdivision())

class Builder(scrapy.Item):
    coop_rate = scrapy.Field(default=CoopRate())
    subdivision_ = scrapy.Field()
    xmlns_p1 = scrapy.Field(default=os.getenv('XMLNS_P1'))
    xmlns_xsi = scrapy.Field(default=os.getenv('XMLNS_XSI'))

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Welcome10(scrapy.Item):
    builder = scrapy.Field()