import scrapy
import os
from dotenv import load_dotenv
load_dotenv()

class HomeItem(scrapy.Item):
    Cities = scrapy.Field()
    Name = scrapy.Field()
    BasicDetails = scrapy.Field()
    AddressMap = scrapy.Field()
    Features = scrapy.Field()
    Images = scrapy.Field()
    VideoLink = scrapy.Field()
    Blueprint = scrapy.Field()

class CoopRate(scrapy.Item):
    HonorsCoopRate = scrapy.Field(default=os.getenv('HONORS_COOP_RATE'))
    CoopRatePct = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Promotion(scrapy.Item):
    PromoId = scrapy.Field(default="")
    PromoType = scrapy.Field(default="")
    PromoHeadline = scrapy.Field(default="")
    PromoDescription = scrapy.Field(default="")
    PromoUrl = scrapy.Field(default="")
    PromoStartDate = scrapy.Field(default="")
    PromoEndDate = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class SubImage(scrapy.Item):
    SubImageUrl = scrapy.Field(default="")
    SubImageCaption = scrapy.Field(default="")
    SubImageUrlContentType = scrapy.Field(default="")
    SubImageOrderBy = scrapy.Field(default="")
    MainFlag = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Image(scrapy.Item):
    SubImage = scrapy.Field(default=SubImage())

class SubVideo(scrapy.Item):
    SubVideoUrl = scrapy.Field(default="")
    SubVideoCaption = scrapy.Field(default="")
    SubVideoUrlContentType = scrapy.Field(default="")
    SubVideoOrderBy = scrapy.Field(default="")
    MainFlag = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Video(scrapy.Item):
    SubVideo = scrapy.Field(default=SubVideo())

class SubdivisionFlyer(scrapy.Item):
    SubdivisionFlyerImageUrl = scrapy.Field(default="")
    SubdivisionFlyerDescription = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Flyer(scrapy.Item):
    SubdivisionFlyer = scrapy.Field(default=SubdivisionFlyer())

class PropertyElevationImage(scrapy.Item):
    PropertyElevationImageUrl = scrapy.Field(default="")
    PropertyElevationImageDescription = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Elevation(scrapy.Item):
    PropertyElevationImage = scrapy.Field(default=PropertyElevationImage())

class PropertyExteriorInteriorImage(scrapy.Item):
    PropertyInteriorImageUrl = scrapy.Field(default="")
    PropertyInteriorImageDescription = scrapy.Field(default="")
    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class ExteriorInterior(scrapy.Item):
    PropertyExteriorInteriorImage = scrapy.Field(default=PropertyExteriorInteriorImage())

class PropertyFloorPlanImage(scrapy.Item):
    PropertyFloorPlanImageUrl = scrapy.Field(default="")
    PropertyFloorPlanImageDescription = scrapy.Field(default="")

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class FloorPlan(scrapy.Item):
    PropertyFloorPlanImage = scrapy.Field(default=PropertyFloorPlanImage())

class SubdivisionProperty(scrapy.Item):
    PropertyId = scrapy.Field(default="")
    PropertyAddress = scrapy.Field()
    PropertyZip = scrapy.Field()
    PropertyPrice = scrapy.Field()
    PropertyLatitude = scrapy.Field()
    PropertyLongitude = scrapy.Field()
    PropertyClassCode = scrapy.Field(default=os.getenv('PROPERTY_CLASS_CODE'))
    PropertyStatusId = scrapy.Field(default=os.getenv('PROPERTY_STATUS_ID'))
    PropertyStageId = scrapy.Field()
    CompletionDate = scrapy.Field(default="")
    PropertyTypeId = scrapy.Field()
    PropertyRemarks = scrapy.Field()
    PropertyShowDirections = scrapy.Field(default="")
    PropertyContact1Name = scrapy.Field(default=os.getenv('PROPERTY_CONTACT1_NAME'))
    PropertyContact1Phone = scrapy.Field(default=os.getenv('PROPERTY_CONTACT1_PHONE'))
    PropertyContact1PhoneAlt = scrapy.Field(default="")
    PropertyContact2Name = scrapy.Field(default="")
    PropertyContact2Phone = scrapy.Field(default="")
    PropertyContact2PhoneAlt = scrapy.Field(default="")
    PropertyContactEmail = scrapy.Field(default=os.getenv('PROPERTY_CONTACT_EMAIL'))
    PropertyDrivingDirections = scrapy.Field(default="")
    PropertyBaths = scrapy.Field()
    PropertyHalfBaths = scrapy.Field(default=os.getenv('PROPERTY_HALF_BATHS'))
    PropertyBeds = scrapy.Field()
    PropertyLiving = scrapy.Field()
    PropertyDining = scrapy.Field()
    PropertyOtherRooms = scrapy.Field(default="")
    PropertyStories = scrapy.Field(default="")
    PropertyMaster = scrapy.Field(default="")
    PropertyGarage = scrapy.Field()
    PropertySchoolDistrictLeaid = scrapy.Field(default=["",""])
    PropertySchoolsNcesid = scrapy.Field(default=["",""])
    PropertySquareFeet = scrapy.Field()
    LotSize = scrapy.Field(default="")
    LotDescription = scrapy.Field(default="")
    FloorPlanNumber = scrapy.Field(default="")
    FloorPlanName = scrapy.Field(default="")
    PropertyCommunityTypeId = scrapy.Field(default=os.getenv('PROPERTYCOMMUNITY_TYPE_ID'))
    PropertyVirtualTour = scrapy.Field(default="")
    PropertyPlanViewUrl = scrapy.Field(default="")
    PropertySchoolComments = scrapy.Field(default="")
    PropertyHasHoa = scrapy.Field(default=os.getenv('PROPERTY_HAS_HOA'))
    PropertyHoaFee = scrapy.Field(default="")
    PropertyHoaBillingPeriod = scrapy.Field(default="")
    PropertyFloorPlanImage_ = scrapy.Field(default=FloorPlan())
    PropertyElevationImage_ = scrapy.Field(default=Elevation())
    PropertyExteriorInteriorImage_ = scrapy.Field()
    Promotion = scrapy.Field(default=Promotion())

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Property(scrapy.Item):
    SubdivisionProperty = scrapy.Field(default=SubdivisionProperty())

class Subdivision(scrapy.Item):
    SubdivisionName = scrapy.Field()
    SubdivisionStateCode = scrapy.Field()
    SubdivisionCityName = scrapy.Field()
    SubdivisionNumber = scrapy.Field(default="")
    CommunityStatusTypeCode = scrapy.Field()
    CommunityMinPrice = scrapy.Field(default="")
    CommunityMaxPrice = scrapy.Field(default="")
    SubdivisionZip = scrapy.Field()
    SubdivisionAddress = scrapy.Field()
    BuilderBrandName = scrapy.Field(default=os.getenv('BUILDER_BRAND_NAME'))
    SubdivisionLatitude = scrapy.Field()
    SubdivisionLongitude = scrapy.Field()
    SubdivisionContact1Name = scrapy.Field(default=os.getenv('SUBDIVISION_CONTACT1_NAME'))
    SubdivisionContact1Phone = scrapy.Field(default=os.getenv('SUBDIVISION_CONTACT1_PHONE'))
    SubdivisionContact1PhoneAlt = scrapy.Field(default="")
    SubdivisionContact2Name = scrapy.Field(default="")
    SubdivisionContact2Phone = scrapy.Field(default="")
    SubdivisionContact2PhoneAlt = scrapy.Field(default="")
    SubdivisionContactEmail = scrapy.Field(default=os.getenv('SUBDIVISION_CONTACT_EMAIL'))
    SubdivisionDescription = scrapy.Field(default="")
    SubdivisionShowDirections = scrapy.Field(default="")
    SubdivisionDrivingDirections = scrapy.Field(default="")
    SubdivisionPropertyTypeId = scrapy.Field()
    SubdivisionCommunityTypeId = scrapy.Field(default=os.getenv('SUBDIVISION_COMMUNITY_TYPE_ID'))
    SubdivisionSchoolDistrictLeaid = scrapy.Field(default=["",""])
    SubdivisionSchoolsNcesid = scrapy.Field(default=["",""])
    SubdivisionSchoolComments = scrapy.Field(default="")
    SubdivisionHasHoa = scrapy.Field(default=os.getenv('SUBDIVISION_HAS_HOA'))
    SubdivisionHoaFee = scrapy.Field(default="")
    SubdivisionHoaBillingPeriod = scrapy.Field(default="")
    SubdivisionNotes = scrapy.Field(default=os.getenv('SUBDIVISION_NOTES'))
    SubdivisionWebsite = scrapy.Field(default="")
    SubdivisionProperty_ = scrapy.Field()
    SubdivisionFlyer_ = scrapy.Field(default=Flyer())
    SubImage_ = scrapy.Field(default=Image())
    SubVideo_ = scrapy.Field(default=Video())
    Promotion = scrapy.Field(default=Promotion())

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Division(scrapy.Item):
    Subdivision = scrapy.Field(default=Subdivision())

class Builder(scrapy.Item):
    CoopRate = scrapy.Field(default=CoopRate())
    Subdivision_ = scrapy.Field()
    XmlnsP1 = scrapy.Field(default=os.getenv('XMLNS_P1'))
    XmlnsXsi = scrapy.Field(default=os.getenv('XMLNS_XSI'))

    def initialize_defaults(self):
        for field, metadata in self.fields.items():
            if 'default' in metadata:
                self.setdefault(field, metadata['default'])

class Welcome10(scrapy.Item):
    Builder = scrapy.Field()
