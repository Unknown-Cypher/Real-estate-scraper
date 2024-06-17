from itemadapter import ItemAdapter
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
import copy
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
        Builder['Subdivision'] = []
        for item in self.items:
            i=0
            for subdivision in Builder['Subdivision']:
                if item['AddressMap']['City'] == subdivision['SubdivisionName']:
                    i = 1
                    break
            if i == 0:
                Subdivision = homescraper.items.Subdivision()
                Subdivision.initialize_defaults()
                SubdivisionFlyer = homescraper.items.SubdivisionFlyer()
                SubdivisionFlyer.initialize_defaults()
                SubImage = homescraper.items.SubImage()
                SubImage.initialize_defaults()
                SubVideo = homescraper.items.SubVideo()
                SubVideo.initialize_defaults()
                Promotion = homescraper.items.Promotion()
                Promotion.initialize_defaults()
                Subdivision['SubdivisionFlyer'] = []
                Subdivision['SubdivisionFlyer'].append(SubdivisionFlyer)
                Subdivision['SubImage'] = []
                Subdivision['SubImage'].append(SubImage)
                Subdivision['SubVideo'] = []
                Subdivision['SubVideo'].append(SubVideo)
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
                    Subdivision['SubdivisionPropertyTypeId'] = '2'
                elif item["BasicDetails"]['Property_Type'] == 'Single Family':
                    Subdivision['SubdivisionPropertyTypeId'] = '1'
                else:
                    Subdivision['SubdivisionPropertyTypeId'] = '23'
                Subdivision['SubdivisionProperty'] = []
                Builder['Subdivision'].append(Subdivision)
            else:
                i=0
        
        for item in self.items:
            SubdivisionProperty = homescraper.items.SubdivisionProperty()
            SubdivisionProperty.initialize_defaults()
            PropertyFloorPlanImage = homescraper.items.PropertyFloorPlanImage()
            PropertyFloorPlanImage.initialize_defaults()
            PropertyFloorPlanImage['PropertyFloorPlanImageUrl'] = item['Blueprint'][0]
            PropertyElevationImage = homescraper.items.PropertyElevationImage()
            PropertyElevationImage.initialize_defaults()
            Promotion = homescraper.items.Promotion()
            Promotion.initialize_defaults()
            SubdivisionProperty['Promotion'] = Promotion
            SubdivisionProperty['PropertyFloorPlanImage'] = []
            SubdivisionProperty['PropertyFloorPlanImage'].append(PropertyFloorPlanImage)
            SubdivisionProperty['PropertyElevationImage'] = []
            SubdivisionProperty['PropertyElevationImage'].append(PropertyElevationImage)

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
                    SubdivisionProperty['PropertyTypeId'] = '2'
            elif item['BasicDetails']['Property_Type'] == 'Single Family':
                    SubdivisionProperty['PropertyTypeId'] = '1'
            else:
                    SubdivisionProperty['PropertyTypeId'] = '23'
            SubdivisionProperty['PropertyRemarks'] = '. '.join(item["Features"])
            SubdivisionProperty['PropertyBaths'] = item['BasicDetails']["Bathrooms"]
            SubdivisionProperty['PropertyBeds'] = item['BasicDetails']["Bedrooms"]
            SubdivisionProperty['PropertyGarage'] = item['BasicDetails']["Garage"]
            SubdivisionProperty['PropertySquareFeet'] = item['BasicDetails']["Square_Footage"].replace(',','')
            if item['VideoLink'] is not None:
                SubdivisionProperty['PropertyVirtualTour'] =item['VideoLink']
            else:
                SubdivisionProperty['PropertyVirtualTour'] = ""
            SubdivisionProperty['PropertyExteriorInteriorImage'] = []
            for image in item['Images']:
               Image =  homescraper.items.PropertyExteriorInteriorImage()
               Image.initialize_defaults()
               Image['PropertyInteriorImageUrl'] =image
               SubdivisionProperty['PropertyExteriorInteriorImage'].append(Image)
            for subdivision in Builder['Subdivision']:
                 if item['AddressMap']['City'] == subdivision['SubdivisionName']:
                    subdivision['SubdivisionProperty'].append(SubdivisionProperty)
                    break
        welcome = homescraper.items.Welcome10()
        welcome['Builder'] = Builder

        # converts python object to xml
        def create_builder_xml(welcome):
            builder = welcome['Builder']
            Builder = Element('Builder', {
                'xmlns:p1': builder['XmlnsP1'],
                'xmlns:xsi': builder['XmlnsXsi']
            })
            
            CoopRate = SubElement(Builder, 'CoopRate')
            cooprate = builder['CoopRate']
            HonorsCoopRate = SubElement(CoopRate, 'HonorsCoopRate')
            HonorsCoopRate.text = cooprate['HonorsCoopRate']
            
            CoopRatePct = SubElement(CoopRate, 'CoopRatePct')
            CoopRatePct.text = cooprate['CoopRatePct']
            for subdivision in builder['Subdivision']:
                Subdivision = SubElement(Builder, 'Subdivision')
                SubdivisionName = SubElement(Subdivision, 'SubdivisionName')
                SubdivisionName.text = subdivision['SubdivisionName']
                SubdivisionStateCode = SubElement(Subdivision, 'SubdivisionStateCode')
                SubdivisionStateCode.text = subdivision['SubdivisionStateCode']
                SubdivisionCityName = SubElement(Subdivision, 'SubdivisionCityName')
                SubdivisionCityName.text = subdivision['SubdivisionCityName']
                SubdivisionNumber = SubElement(Subdivision, 'SubdivisionNumber')
                SubdivisionNumber.text = subdivision['SubdivisionNumber']
                CommunityStatusTypeCode = SubElement(Subdivision, 'CommunityStatusTypeCode')
                CommunityStatusTypeCode.text = subdivision['CommunityStatusTypeCode']
                CommunityMinPrice = SubElement(Subdivision, 'CommunityMinPrice')
                CommunityMinPrice.text = subdivision['CommunityMinPrice']
                CommunityMaxPrice = SubElement(Subdivision, 'CommunityMaxPrice')
                CommunityMaxPrice.text = subdivision['CommunityMaxPrice']
                SubdivisionZip = SubElement(Subdivision, 'SubdivisionZip')
                SubdivisionZip.text = subdivision['SubdivisionZip']
                SubdivisionAddress = SubElement(Subdivision, 'SubdivisionAddress')
                SubdivisionAddress.text = subdivision['SubdivisionAddress']
                BuilderBrandName = SubElement(Subdivision, 'BuilderBrandName')
                BuilderBrandName.text = subdivision['BuilderBrandName']
                SubdivisionLatitude = SubElement(Subdivision, 'SubdivisionLatitude')
                SubdivisionLatitude.text = str(subdivision['SubdivisionLatitude'])
                SubdivisionLongitude = SubElement(Subdivision, 'SubdivisionLongitude')
                SubdivisionLongitude.text = str(subdivision['SubdivisionLongitude'])
                SubdivisionContact1Name = SubElement(Subdivision, 'SubdivisionContact1Name')
                SubdivisionContact1Name.text = subdivision['SubdivisionContact1Name']
                SubdivisionContact1Phone = SubElement(Subdivision, 'SubdivisionContact1Phone')
                SubdivisionContact1Phone.text = subdivision['SubdivisionContact1Phone']
                SubdivisionContact1PhoneAlt = SubElement(Subdivision, 'SubdivisionContact1PhoneAlt')
                SubdivisionContact1PhoneAlt.text = subdivision['SubdivisionContact1PhoneAlt']
                SubdivisionContact2Name = SubElement(Subdivision, 'SubdivisionContact2Name')
                SubdivisionContact2Name.text = subdivision['SubdivisionContact2Name']
                SubdivisionContact2Phone = SubElement(Subdivision, 'SubdivisionContact2Phone')
                SubdivisionContact2Phone.text = subdivision['SubdivisionContact2Phone']
                SubdivisionContact2PhoneAlt = SubElement(Subdivision, 'SubdivisionContact2PhoneAlt')
                SubdivisionContact2PhoneAlt.text = subdivision['SubdivisionContact2PhoneAlt']
                SubdivisionContactEmail = SubElement(Subdivision, 'SubdivisionContactEmail')
                SubdivisionContactEmail.text = subdivision['SubdivisionContactEmail']
                SubdivisionDescription = SubElement(Subdivision, 'SubdivisionDescription')
                SubdivisionDescription.text = subdivision['SubdivisionDescription']
                SubdivisionShowDirections = SubElement(Subdivision, 'SubdivisionShowDirections')
                SubdivisionShowDirections.text = subdivision['SubdivisionShowDirections']
                SubdivisionDrivingDirections = SubElement(Subdivision, 'SubdivisionDrivingDirections')
                SubdivisionDrivingDirections.text = subdivision['SubdivisionDrivingDirections']
                SubdivisionPropertyTypeId = SubElement(Subdivision, 'SubdivisionPropertyTypeId')
                SubdivisionPropertyTypeId.text = str(subdivision['SubdivisionPropertyTypeId'])
                SubdivisionCommunityTypeId = SubElement(Subdivision, 'SubdivisionCommunityTypeId')
                SubdivisionCommunityTypeId.text = str(subdivision['SubdivisionCommunityTypeId'])
                for SubdivisionSchoolDistrictLeaid in subdivision['SubdivisionSchoolDistrictLeaid']:
                    SubdivisionSchoolDistrictLeaid1 = SubElement(Subdivision, 'SubdivisionSchoolDistrictLeaid')
                    SubdivisionSchoolDistrictLeaid1.text = SubdivisionSchoolDistrictLeaid
                for SubdivisionSchoolsNcesid in subdivision['SubdivisionSchoolsNcesid']:
                    SubdivisionSchoolsNcesid1 = SubElement(Subdivision, 'SubdivisionSchoolsNcesid')
                    SubdivisionSchoolsNcesid1.text = SubdivisionSchoolsNcesid
                SubdivisionSchoolComments = SubElement(Subdivision, 'SubdivisionSchoolComments')
                SubdivisionSchoolComments.text = subdivision['SubdivisionSchoolComments']
                SubdivisionHasHoa = SubElement(Subdivision, 'SubdivisionHasHoa')
                SubdivisionHasHoa.text = subdivision['SubdivisionHasHoa']
                SubdivisionHoaFee = SubElement(Subdivision, 'SubdivisionHoaFee')
                SubdivisionHoaFee.text = subdivision['SubdivisionHoaFee']
                SubdivisionHoaBillingPeriod = SubElement(Subdivision, 'SubdivisionHoaBillingPeriod')
                SubdivisionHoaBillingPeriod.text = subdivision['SubdivisionHoaBillingPeriod']
                SubdivisionNotes = SubElement(Subdivision, 'SubdivisionNotes')
                SubdivisionNotes.text = subdivision['SubdivisionNotes']
                SubdivisionWebsite = SubElement(Subdivision, 'SubdivisionWebsite')
                SubdivisionWebsite.text = subdivision['SubdivisionWebsite']
                for subdivisionProperty in subdivision['SubdivisionProperty']:
                    SubdivisionProperty = SubElement(Subdivision, 'SubdivisionProperty')
                    PropertyId = SubElement(SubdivisionProperty, 'PropertyId')
                    PropertyId.text = subdivisionProperty['PropertyId']
                    PropertyAddress = SubElement(SubdivisionProperty, 'PropertyAddress')
                    PropertyAddress.text = subdivisionProperty['PropertyAddress']
                    PropertyZip = SubElement(SubdivisionProperty, 'PropertyZip')
                    PropertyZip.text = subdivisionProperty['PropertyZip']
                    PropertyPrice = SubElement(SubdivisionProperty, 'PropertyPrice')
                    PropertyPrice.text = subdivisionProperty['PropertyPrice']
                    PropertyLatitude = SubElement(SubdivisionProperty, 'PropertyLatitude')
                    PropertyLatitude.text = str(subdivisionProperty['PropertyLatitude'])
                    PropertyLongitude = SubElement(SubdivisionProperty, 'PropertyLongitude')
                    PropertyLongitude.text = str(subdivisionProperty['PropertyLongitude'])
                    PropertyClassCode = SubElement(SubdivisionProperty, 'PropertyClassCode')
                    PropertyClassCode.text = subdivisionProperty['PropertyClassCode']
                    PropertyStatusId = SubElement(SubdivisionProperty, 'PropertyStatusId')
                    PropertyStatusId.text = subdivisionProperty['PropertyStatusId']
                    PropertyStageId = SubElement(SubdivisionProperty, 'PropertyStageId')
                    PropertyStageId.text = subdivisionProperty['PropertyStageId']
                    CompletionDate = SubElement(SubdivisionProperty, 'CompletionDate')
                    CompletionDate.text = subdivisionProperty['CompletionDate']
                    PropertyTypeId = SubElement(SubdivisionProperty, 'PropertyTypeId')
                    PropertyTypeId.text = str(subdivisionProperty['PropertyTypeId'])
                    PropertyRemarks = SubElement(SubdivisionProperty, 'PropertyRemarks')
                    PropertyRemarks.text = subdivisionProperty['PropertyRemarks']
                    PropertyShowDirections = SubElement(SubdivisionProperty, 'PropertyShowDirections')
                    PropertyShowDirections.text = subdivisionProperty['PropertyShowDirections']
                    PropertyContact1Name = SubElement(SubdivisionProperty, 'PropertyContact1Name')
                    PropertyContact1Name.text = subdivisionProperty['PropertyContact1Name']
                    PropertyContact1Phone = SubElement(SubdivisionProperty, 'PropertyContact1Phone')
                    PropertyContact1Phone.text = subdivisionProperty['PropertyContact1Phone']
                    PropertyContact1PhoneAlt = SubElement(SubdivisionProperty, 'PropertyContact1PhoneAlt')
                    PropertyContact1PhoneAlt.text = subdivisionProperty['PropertyContact1PhoneAlt']
                    PropertyContact2Name = SubElement(SubdivisionProperty, 'PropertyContact2Name')
                    PropertyContact2Name.text = subdivisionProperty['PropertyContact2Name']
                    PropertyContact2Phone = SubElement(SubdivisionProperty, 'PropertyContact2Phone')
                    PropertyContact2Phone.text = subdivisionProperty['PropertyContact2Phone']
                    PropertyContact2PhoneAlt = SubElement(SubdivisionProperty, 'PropertyContact2PhoneAlt')
                    PropertyContact2PhoneAlt.text = subdivisionProperty['PropertyContact2PhoneAlt']
                    PropertyContactEmail = SubElement(SubdivisionProperty, 'PropertyContactEmail')
                    PropertyContactEmail.text = subdivisionProperty['PropertyContactEmail']
                    PropertyDrivingDirections = SubElement(SubdivisionProperty, 'PropertyDrivingDirections')
                    PropertyDrivingDirections.text = subdivisionProperty['PropertyDrivingDirections']
                    PropertyBaths = SubElement(SubdivisionProperty, 'PropertyBaths')
                    PropertyBaths.text = subdivisionProperty['PropertyBaths']
                    PropertyHalfBaths = SubElement(SubdivisionProperty, 'PropertyHalfBaths')
                    PropertyHalfBaths.text = subdivisionProperty['PropertyHalfBaths']
                    PropertyBeds = SubElement(SubdivisionProperty, 'PropertyBeds')
                    PropertyBeds.text = subdivisionProperty['PropertyBeds']
                    PropertyLiving = SubElement(SubdivisionProperty, 'PropertyLiving')
                    PropertyLiving.text = subdivisionProperty['PropertyLiving']
                    PropertyDining = SubElement(SubdivisionProperty, 'PropertyDining')
                    PropertyDining.text = subdivisionProperty['PropertyDining']
                    PropertyOtherRooms = SubElement(SubdivisionProperty, 'PropertyOtherRooms')
                    PropertyOtherRooms.text = subdivisionProperty['PropertyOtherRooms']
                    PropertyStories = SubElement(SubdivisionProperty, 'PropertyStories')
                    PropertyStories.text = subdivisionProperty['PropertyStories']
                    PropertyMaster = SubElement(SubdivisionProperty, 'PropertyMaster')
                    PropertyMaster.text = subdivisionProperty['PropertyMaster']
                    PropertyGarage = SubElement(SubdivisionProperty, 'PropertyGarage')
                    PropertyGarage.text = subdivisionProperty['PropertyGarage']
                    for PropertySchoolDistrictLEAID in subdivisionProperty['PropertySchoolDistrictLeaid']:
                        PropertySchoolDistrictLEAID1 = SubElement(SubdivisionProperty, 'PropertySchoolDistrictLEAID')
                        PropertySchoolDistrictLEAID1.text = PropertySchoolDistrictLEAID
                    for PropertySchoolsNCESID in subdivisionProperty['PropertySchoolsNcesid']:
                        PropertySchoolsNCESID1 = SubElement(SubdivisionProperty, 'PropertySchoolsNCESID')
                        PropertySchoolsNCESID1.text = PropertySchoolsNCESID
                    PropertySquareFeet = SubElement(SubdivisionProperty,'PropertySquareFeet')
                    PropertySquareFeet.text = subdivisionProperty['PropertySquareFeet']
                    LotSize = SubElement(SubdivisionProperty,'LotSize')
                    LotSize.text = subdivisionProperty['LotSize']
                    LotDescription = SubElement(SubdivisionProperty,'LotDescription')
                    LotDescription.text = subdivisionProperty['LotDescription']
                    FloorPlanNumber = SubElement(SubdivisionProperty,'FloorPlanNumber')
                    FloorPlanNumber.text = subdivisionProperty['FloorPlanNumber']
                    FloorPlanName = SubElement(SubdivisionProperty,'FloorPlanName')
                    FloorPlanName.text = subdivisionProperty['FloorPlanName']
                    PropertyCommunityTypeId = SubElement(SubdivisionProperty,'PropertyCommunityTypeId')
                    PropertyCommunityTypeId.text = str(subdivisionProperty['PropertyCommunityTypeId'])
                    PropertyVirtualTour = SubElement(SubdivisionProperty,'PropertyVirtualTour')
                    PropertyVirtualTour.text = subdivisionProperty['PropertyVirtualTour']
                    PropertyPlanViewUrl = SubElement(SubdivisionProperty,'PropertyPlanViewUrl')
                    PropertyPlanViewUrl.text = subdivisionProperty['PropertyPlanViewUrl']
                    PropertySchoolComments = SubElement(SubdivisionProperty,'PropertySchoolComments')
                    PropertySchoolComments.text = subdivisionProperty['PropertySchoolComments']
                    PropertyHasHoa = SubElement(SubdivisionProperty,'PropertyHasHoa')
                    PropertyHasHoa.text = subdivisionProperty['PropertyHasHoa']
                    PropertyHoaFee = SubElement(SubdivisionProperty,'PropertyHoaFee')
                    PropertyHoaFee.text = subdivisionProperty['PropertyHoaFee']
                    PropertyHoaBillingPeriod = SubElement(SubdivisionProperty,'PropertyHoaBillingPeriod')
                    PropertyHoaBillingPeriod.text = subdivisionProperty['PropertyHoaBillingPeriod']
                    for propertyFloorPlanImage in subdivisionProperty['PropertyFloorPlanImage']:
                        PropertyFloorPlanImage = SubElement(SubdivisionProperty, 'PropertyFloorPlanImage')
                        PropertyFloorPlanImageURL = SubElement(PropertyFloorPlanImage, 'PropertyFloorPlanImageURL')
                        PropertyFloorPlanImageURL.text = propertyFloorPlanImage['PropertyFloorPlanImageUrl']
                        PropertyFloorPlanImageDescription = SubElement(PropertyFloorPlanImage, 'PropertyFloorPlanImageDescription')
                        PropertyFloorPlanImageDescription.text = propertyFloorPlanImage['PropertyFloorPlanImageDescription']

                    for propertyElevationImage in subdivisionProperty['PropertyElevationImage']:
                        PropertyElevationImage = SubElement(SubdivisionProperty, 'PropertyElevationImage')
                        PropertyElevationImageURL = SubElement(PropertyElevationImage, 'PropertyElevationImageURL')
                        PropertyElevationImageURL.text = propertyElevationImage['PropertyElevationImageUrl']
                        PropertyElevationImageDescription = SubElement(PropertyElevationImage, 'PropertyElevationImageDescription')
                        PropertyElevationImageDescription.text = propertyElevationImage['PropertyElevationImageDescription']

                    for propertyExteriorInteriorImage in subdivisionProperty['PropertyExteriorInteriorImage']:
                        PropertyExteriorInteriorImage = SubElement(SubdivisionProperty, 'PropertyExteriorInteriorImage')
                        PropertyInteriorImageURL = SubElement(PropertyExteriorInteriorImage, 'PropertyInteriorImageURL')
                        PropertyInteriorImageURL.text = propertyExteriorInteriorImage['PropertyInteriorImageUrl']
                        PropertyInteriorImageDescription = SubElement(PropertyExteriorInteriorImage, 'PropertyInteriorImageDescription')
                        PropertyInteriorImageDescription.text = propertyExteriorInteriorImage['PropertyInteriorImageDescription']

                    Promotion = SubElement(SubdivisionProperty, 'Promotion')
                    promotion = subdivisionProperty['Promotion']
                    PromoId = SubElement(Promotion,'PromoId')
                    PromoId.text = promotion['PromoId']
                    PromoType = SubElement(Promotion,'PromoType')
                    PromoType.text = promotion['PromoType']
                    PromoHeadline = SubElement(Promotion,'PromoHeadline')
                    PromoHeadline.text = promotion['PromoHeadline']
                    PromoDescription = SubElement(Promotion,'PromoDescription')
                    PromoDescription.text = promotion['PromoDescription']
                    PromoURL = SubElement(Promotion,'PromoURL')
                    PromoURL.text = promotion['PromoUrl']
                    PromoStartDate = SubElement(Promotion,'PromoStartDate')
                    PromoStartDate.text = promotion['PromoStartDate']
                    PromoEndDate = SubElement(Promotion,'PromoEndDate')
                    PromoEndDate.text = promotion['PromoEndDate']

                for subdivisionFlyer in subdivision['SubdivisionFlyer']:
                    SubdivisionFlyer = SubElement(Subdivision,'SubdivisionFlyer')
                    SubdivisionFlyerImageURL = SubElement(SubdivisionFlyer,'SubdivisionFlyerImageURL')
                    SubdivisionFlyerImageURL.text = subdivisionFlyer['SubdivisionFlyerImageUrl']
                    SubdivisionFlyerDescription = SubElement(SubdivisionFlyer,'SubdivisionFlyerDescription')
                    SubdivisionFlyerDescription.text = subdivisionFlyer['SubdivisionFlyerDescription']

                for subImage in subdivision['SubImage']:
                    SubImage = SubElement(Subdivision,'SubImage')
                    SubImageUrl = SubElement(SubImage,'SubImageURL')
                    SubImageUrl.text = subImage['SubImageUrl']
                    SubImageCaption = SubElement(SubImage,'SubImageCaption')
                    SubImageCaption.text = subImage['SubImageCaption']
                    SubImageURLContentType = SubElement(SubImage,'SubImageURLContentType')
                    SubImageURLContentType.text = subImage['SubImageUrlContentType']
                    SubImageOrderBy = SubElement(SubImage,'SubImageOrderBy')
                    SubImageOrderBy.text = subImage['SubImageOrderBy']
                    MainFlag = SubElement(SubImage,'MainFlag')
                    MainFlag.text = subImage['MainFlag']

                for subVideo in subdivision['SubVideo']:
                    SubVideo = SubElement(Subdivision,'SubVideo')
                    SubVideoURL = SubElement(SubVideo,'SubVideoURL')
                    SubVideoURL.text = subVideo['SubVideoUrl']
                    SubVideoCaption = SubElement(SubVideo,'SubVideoCaption')
                    SubVideoCaption.text = subVideo['SubVideoCaption']
                    SubVideoUrlContentType = SubElement(SubVideo,'SubVideoUrlContentType')
                    SubVideoUrlContentType.text = subVideo['SubVideoUrlContentType']
                    SubVideoOrderBy = SubElement(SubVideo,'SubVideoOrderBy')
                    SubVideoOrderBy.text = subVideo['SubVideoOrderBy']
                    MainFlag = SubElement(SubVideo,'MainFlag')
                    MainFlag.text = subVideo['MainFlag']
                
                Promotion = SubElement(Subdivision, 'Promotion')
                promotion = subdivision['Promotion']
                PromoId = SubElement(Promotion,'PromoId')
                PromoId.text = promotion['PromoId']
                PromoType = SubElement(Promotion,'PromoType')
                PromoType.text = promotion['PromoType']
                PromoHeadline = SubElement(Promotion,'PromoHeadline')
                PromoHeadline.text = promotion['PromoHeadline']
                PromoDescription = SubElement(Promotion,'PromoDescription')
                PromoDescription.text = promotion['PromoDescription']
                PromoURL = SubElement(Promotion,'PromoURL')
                PromoURL.text = promotion['PromoUrl']
                PromoStartDate = SubElement(Promotion,'PromoStartDate')
                PromoStartDate.text = promotion['PromoStartDate']
                PromoEndDate = SubElement(Promotion,'PromoEndDate')
                PromoEndDate.text = promotion['PromoEndDate']


            xml = ET.tostring(Builder, encoding='unicode')
            with open('final.xml','w') as f:
                f.write('<?xml version="1.0" ?>\n' + xml)


        create_builder_xml(welcome)

        
