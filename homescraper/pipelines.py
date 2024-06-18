from itemadapter import ItemAdapter
import re
from lxml import etree as ET
from lxml.etree import Element, SubElement
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

        #function to format the phone numbers
        def reformat_phone_number(phone_number):
            digits = re.sub(r'\D', '', phone_number)
            formatted_phone_number = f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
            return formatted_phone_number
        

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

                if item['AddressMap']['City'] in item['Cities']:
                    Subdivision['SubdivisionWebsite'] = item['Cities'][item['AddressMap']['City']]
                Subdivision['SubdivisionName'] = item['AddressMap']['City']
                Subdivision['SubdivisionStateCode'] = item['AddressMap']['State']
                Subdivision['SubdivisionCityName'] = item['AddressMap']['City']
                Subdivision['SubdivisionZip'] = item['AddressMap']['Zip_Code']
                Subdivision['SubdivisionAddress'] = item['AddressMap']['Zip_Code'] + ' ' +item['AddressMap']["Street"]
                Subdivision['SubdivisionLatitude'] = item['AddressMap']['latitude']
                Subdivision['SubdivisionLongitude'] = item['AddressMap']['longitude']
                Subdivision['SubdivisionContact1Phone'] = reformat_phone_number(Subdivision['SubdivisionContact1Phone'])
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
            SubdivisionProperty['PropertyContact1Phone'] = reformat_phone_number(SubdivisionProperty['PropertyContact1Phone'])
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
            SubdivisionProperty['PropertyBaths'] = str(int(float(item['BasicDetails']["Bathrooms"])))
            if item['BasicDetails']["Bathrooms"].endswith('.5'):
                SubdivisionProperty['PropertyHalfBaths'] = '1'
            SubdivisionProperty['FloorPlanName'] = item['AddressMap']['address']
            SubdivisionProperty['FloorPlanNumber'] = item['AddressMap']['address']
            SubdivisionProperty['PropertyBeds'] = item['BasicDetails']["Bedrooms"]
            SubdivisionProperty['PropertyGarage'] = item['BasicDetails']["Garage"]
            SubdivisionProperty['PropertyClassCode'] = SubdivisionProperty['PropertyClassCode'].split(',')
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
            Builder = Element('Builder', nsmap= {
                'p1': builder['XmlnsP1'],
                'xsi': builder['XmlnsXsi']
            })
            
            CoopRate = SubElement(Builder, 'CoopRate')
            cooprate = builder['CoopRate']
            HonorsCoopRate = SubElement(CoopRate, 'HonorsCoopRate')
            HonorsCoopRate.text = ET.CDATA(cooprate['HonorsCoopRate'])
            
            CoopRatePct = SubElement(CoopRate, 'CoopRatePct')
            CoopRatePct.text = ET.CDATA(cooprate['CoopRatePct'])
            for subdivision in builder['Subdivision']:
                Subdivision = SubElement(Builder, 'Subdivision')
                SubdivisionName = SubElement(Subdivision, 'SubdivisionName')
                SubdivisionName.text = ET.CDATA(subdivision['SubdivisionName'])
                SubdivisionStateCode = SubElement(Subdivision, 'SubdivisionStateCode')
                SubdivisionStateCode.text = ET.CDATA(subdivision['SubdivisionStateCode'])
                SubdivisionCityName = SubElement(Subdivision, 'SubdivisionCityName')
                SubdivisionCityName.text = ET.CDATA(subdivision['SubdivisionCityName'])
                SubdivisionNumber = SubElement(Subdivision, 'SubdivisionNumber')
                SubdivisionNumber.text = ET.CDATA(subdivision['SubdivisionNumber'])
                CommunityStatusTypeCode = SubElement(Subdivision, 'CommunityStatusTypeCode')
                CommunityStatusTypeCode.text = ET.CDATA(subdivision['CommunityStatusTypeCode'])
                CommunityMinPrice = SubElement(Subdivision, 'CommunityMinPrice')
                CommunityMinPrice.text = ET.CDATA(subdivision['CommunityMinPrice'])
                CommunityMaxPrice = SubElement(Subdivision, 'CommunityMaxPrice')
                CommunityMaxPrice.text = ET.CDATA(subdivision['CommunityMaxPrice'])
                SubdivisionZip = SubElement(Subdivision, 'SubdivisionZip')
                SubdivisionZip.text = ET.CDATA(subdivision['SubdivisionZip'])
                SubdivisionAddress = SubElement(Subdivision, 'SubdivisionAddress')
                SubdivisionAddress.text = ET.CDATA(subdivision['SubdivisionAddress'])
                BuilderBrandName = SubElement(Subdivision, 'BuilderBrandName')
                BuilderBrandName.text = ET.CDATA(subdivision['BuilderBrandName'])
                SubdivisionLatitude = SubElement(Subdivision, 'SubdivisionLatitude')
                SubdivisionLatitude.text = ET.CDATA(str(subdivision['SubdivisionLatitude']))
                SubdivisionLongitude = SubElement(Subdivision, 'SubdivisionLongitude')
                SubdivisionLongitude.text = ET.CDATA(str(subdivision['SubdivisionLongitude']))
                SubdivisionContact1Name = SubElement(Subdivision, 'SubdivisionContact1Name')
                SubdivisionContact1Name.text = ET.CDATA(subdivision['SubdivisionContact1Name'])
                SubdivisionContact1Phone = SubElement(Subdivision, 'SubdivisionContact1Phone')
                SubdivisionContact1Phone.text = ET.CDATA(subdivision['SubdivisionContact1Phone'])
                SubdivisionContact1PhoneAlt = SubElement(Subdivision, 'SubdivisionContact1PhoneAlt')
                SubdivisionContact1PhoneAlt.text = ET.CDATA(subdivision['SubdivisionContact1PhoneAlt'])
                SubdivisionContact2Name = SubElement(Subdivision, 'SubdivisionContact2Name')
                SubdivisionContact2Name.text = ET.CDATA(subdivision['SubdivisionContact2Name'])
                SubdivisionContact2Phone = SubElement(Subdivision, 'SubdivisionContact2Phone')
                SubdivisionContact2Phone.text = ET.CDATA(subdivision['SubdivisionContact2Phone'])
                SubdivisionContact2PhoneAlt = SubElement(Subdivision, 'SubdivisionContact2PhoneAlt')
                SubdivisionContact2PhoneAlt.text = ET.CDATA(subdivision['SubdivisionContact2PhoneAlt'])
                SubdivisionContactEmail = SubElement(Subdivision, 'SubdivisionContactEmail')
                SubdivisionContactEmail.text = ET.CDATA(subdivision['SubdivisionContactEmail'])
                SubdivisionDescription = SubElement(Subdivision, 'SubdivisionDescription')
                SubdivisionDescription.text = ET.CDATA(subdivision['SubdivisionDescription'])
                SubdivisionShowDirections = SubElement(Subdivision, 'SubdivisionShowDirections')
                SubdivisionShowDirections.text = ET.CDATA(subdivision['SubdivisionShowDirections'])
                SubdivisionDrivingDirections = SubElement(Subdivision, 'SubdivisionDrivingDirections')
                SubdivisionDrivingDirections.text = ET.CDATA(subdivision['SubdivisionDrivingDirections'])
                SubdivisionPropertyTypeId = SubElement(Subdivision, 'SubdivisionPropertyTypeId')
                SubdivisionPropertyTypeId.text = ET.CDATA(str(subdivision['SubdivisionPropertyTypeId']))
                SubdivisionCommunityTypeId = SubElement(Subdivision, 'SubdivisionCommunityTypeId')
                SubdivisionCommunityTypeId.text = ET.CDATA(str(subdivision['SubdivisionCommunityTypeId']))
                for SubdivisionSchoolDistrictLeaid in subdivision['SubdivisionSchoolDistrictLeaid']:
                    SubdivisionSchoolDistrictLeaid1 = SubElement(Subdivision, 'SubdivisionSchoolDistrictLeaid')
                    SubdivisionSchoolDistrictLeaid1.text = ET.CDATA(SubdivisionSchoolDistrictLeaid)
                for SubdivisionSchoolsNcesid in subdivision['SubdivisionSchoolsNcesid']:
                    SubdivisionSchoolsNcesid1 = SubElement(Subdivision, 'SubdivisionSchoolsNcesid')
                    SubdivisionSchoolsNcesid1.text = ET.CDATA(SubdivisionSchoolsNcesid)
                SubdivisionSchoolComments = SubElement(Subdivision, 'SubdivisionSchoolComments')
                SubdivisionSchoolComments.text = ET.CDATA(subdivision['SubdivisionSchoolComments'])
                SubdivisionHasHoa = SubElement(Subdivision, 'SubdivisionHasHoa')
                SubdivisionHasHoa.text = ET.CDATA(subdivision['SubdivisionHasHoa'])
                SubdivisionHoaFee = SubElement(Subdivision, 'SubdivisionHoaFee')
                SubdivisionHoaFee.text = ET.CDATA(subdivision['SubdivisionHoaFee'])
                SubdivisionHoaBillingPeriod = SubElement(Subdivision, 'SubdivisionHoaBillingPeriod')
                SubdivisionHoaBillingPeriod.text = ET.CDATA(subdivision['SubdivisionHoaBillingPeriod'])
                SubdivisionNotes = SubElement(Subdivision, 'SubdivisionNotes')
                SubdivisionNotes.text = ET.CDATA(subdivision['SubdivisionNotes'])
                SubdivisionWebsite = SubElement(Subdivision, 'SubdivisionWebsite')
                SubdivisionWebsite.text = ET.CDATA(subdivision['SubdivisionWebsite'])
                for subdivisionProperty in subdivision['SubdivisionProperty']:
                    for class_code in subdivisionProperty['PropertyClassCode']:
                        SubdivisionProperty = SubElement(Subdivision, 'SubdivisionProperty')
                        PropertyId = SubElement(SubdivisionProperty, 'PropertyId')
                        PropertyId.text = ET.CDATA(subdivisionProperty['PropertyId'])
                        PropertyAddress = SubElement(SubdivisionProperty, 'PropertyAddress')
                        PropertyAddress.text = ET.CDATA(subdivisionProperty['PropertyAddress'])
                        PropertyZip = SubElement(SubdivisionProperty, 'PropertyZip')
                        PropertyZip.text = ET.CDATA(subdivisionProperty['PropertyZip'])
                        PropertyPrice = SubElement(SubdivisionProperty, 'PropertyPrice')
                        PropertyPrice.text = ET.CDATA(subdivisionProperty['PropertyPrice'])
                        PropertyLatitude = SubElement(SubdivisionProperty, 'PropertyLatitude')
                        PropertyLatitude.text = ET.CDATA(str(subdivisionProperty['PropertyLatitude']))
                        PropertyLongitude = SubElement(SubdivisionProperty, 'PropertyLongitude')
                        PropertyLongitude.text = ET.CDATA(str(subdivisionProperty['PropertyLongitude']))
                        PropertyClassCode = SubElement(SubdivisionProperty, 'PropertyClassCode')
                        PropertyClassCode.text = ET.CDATA(class_code)
                        PropertyStatusId = SubElement(SubdivisionProperty, 'PropertyStatusId')
                        PropertyStatusId.text = ET.CDATA(subdivisionProperty['PropertyStatusId'])
                        PropertyStageId = SubElement(SubdivisionProperty, 'PropertyStageId')
                        PropertyStageId.text = ET.CDATA(subdivisionProperty['PropertyStageId'])
                        CompletionDate = SubElement(SubdivisionProperty, 'CompletionDate')
                        CompletionDate.text = ET.CDATA(subdivisionProperty['CompletionDate'])
                        PropertyTypeId = SubElement(SubdivisionProperty, 'PropertyTypeId')
                        PropertyTypeId.text = ET.CDATA(str(subdivisionProperty['PropertyTypeId']))
                        PropertyRemarks = SubElement(SubdivisionProperty, 'PropertyRemarks')
                        PropertyRemarks.text = ET.CDATA(subdivisionProperty['PropertyRemarks'])
                        PropertyShowDirections = SubElement(SubdivisionProperty, 'PropertyShowDirections')
                        PropertyShowDirections.text = ET.CDATA(subdivisionProperty['PropertyShowDirections'])
                        PropertyContact1Name = SubElement(SubdivisionProperty, 'PropertyContact1Name')
                        PropertyContact1Name.text = ET.CDATA(subdivisionProperty['PropertyContact1Name'])
                        PropertyContact1Phone = SubElement(SubdivisionProperty, 'PropertyContact1Phone')
                        PropertyContact1Phone.text = ET.CDATA(subdivisionProperty['PropertyContact1Phone'])
                        PropertyContact1PhoneAlt = SubElement(SubdivisionProperty, 'PropertyContact1PhoneAlt')
                        PropertyContact1PhoneAlt.text = ET.CDATA(subdivisionProperty['PropertyContact1PhoneAlt'])
                        PropertyContact2Name = SubElement(SubdivisionProperty, 'PropertyContact2Name')
                        PropertyContact2Name.text = ET.CDATA(subdivisionProperty['PropertyContact2Name'])
                        PropertyContact2Phone = SubElement(SubdivisionProperty, 'PropertyContact2Phone')
                        PropertyContact2Phone.text = ET.CDATA(subdivisionProperty['PropertyContact2Phone'])
                        PropertyContact2PhoneAlt = SubElement(SubdivisionProperty, 'PropertyContact2PhoneAlt')
                        PropertyContact2PhoneAlt.text = ET.CDATA(subdivisionProperty['PropertyContact2PhoneAlt'])
                        PropertyContactEmail = SubElement(SubdivisionProperty, 'PropertyContactEmail')
                        PropertyContactEmail.text = ET.CDATA(subdivisionProperty['PropertyContactEmail'])
                        PropertyDrivingDirections = SubElement(SubdivisionProperty, 'PropertyDrivingDirections')
                        PropertyDrivingDirections.text = ET.CDATA(subdivisionProperty['PropertyDrivingDirections'])
                        PropertyBaths = SubElement(SubdivisionProperty, 'PropertyBaths')
                        PropertyBaths.text = ET.CDATA(subdivisionProperty['PropertyBaths'])
                        PropertyHalfBaths = SubElement(SubdivisionProperty, 'PropertyHalfBaths')
                        PropertyHalfBaths.text = ET.CDATA(subdivisionProperty['PropertyHalfBaths'])
                        PropertyBeds = SubElement(SubdivisionProperty, 'PropertyBeds')
                        PropertyBeds.text = ET.CDATA(subdivisionProperty['PropertyBeds'])
                        PropertyLiving = SubElement(SubdivisionProperty, 'PropertyLiving')
                        PropertyLiving.text = ET.CDATA(subdivisionProperty['PropertyLiving'])
                        PropertyDining = SubElement(SubdivisionProperty, 'PropertyDining')
                        PropertyDining.text = ET.CDATA(subdivisionProperty['PropertyDining'])
                        PropertyOtherRooms = SubElement(SubdivisionProperty, 'PropertyOtherRooms')
                        PropertyOtherRooms.text = ET.CDATA(subdivisionProperty['PropertyOtherRooms'])
                        PropertyStories = SubElement(SubdivisionProperty, 'PropertyStories')
                        PropertyStories.text = ET.CDATA(subdivisionProperty['PropertyStories'])
                        PropertyMaster = SubElement(SubdivisionProperty, 'PropertyMaster')
                        PropertyMaster.text = ET.CDATA(subdivisionProperty['PropertyMaster'])
                        PropertyGarage = SubElement(SubdivisionProperty, 'PropertyGarage')
                        PropertyGarage.text = ET.CDATA(subdivisionProperty['PropertyGarage'])
                        for PropertySchoolDistrictLEAID in subdivisionProperty['PropertySchoolDistrictLeaid']:
                            PropertySchoolDistrictLEAID1 = SubElement(SubdivisionProperty, 'PropertySchoolDistrictLEAID')
                            PropertySchoolDistrictLEAID1.text = ET.CDATA(PropertySchoolDistrictLEAID)
                        for PropertySchoolsNCESID in subdivisionProperty['PropertySchoolsNcesid']:
                            PropertySchoolsNCESID1 = SubElement(SubdivisionProperty, 'PropertySchoolsNCESID')
                            PropertySchoolsNCESID1.text = ET.CDATA(PropertySchoolsNCESID)
                        PropertySquareFeet = SubElement(SubdivisionProperty,'PropertySquareFeet')
                        PropertySquareFeet.text = ET.CDATA(subdivisionProperty['PropertySquareFeet'])
                        LotSize = SubElement(SubdivisionProperty,'LotSize')
                        LotSize.text = ET.CDATA(subdivisionProperty['LotSize'])
                        LotDescription = SubElement(SubdivisionProperty,'LotDescription')
                        LotDescription.text = ET.CDATA(subdivisionProperty['LotDescription'])
                        FloorPlanNumber = SubElement(SubdivisionProperty,'FloorPlanNumber')
                        FloorPlanNumber.text = ET.CDATA(subdivisionProperty['FloorPlanNumber'])
                        FloorPlanName = SubElement(SubdivisionProperty,'FloorPlanName')
                        FloorPlanName.text = ET.CDATA(subdivisionProperty['FloorPlanName'])
                        PropertyCommunityTypeId = SubElement(SubdivisionProperty,'PropertyCommunityTypeId')
                        PropertyCommunityTypeId.text = ET.CDATA(str(subdivisionProperty['PropertyCommunityTypeId']))
                        PropertyVirtualTour = SubElement(SubdivisionProperty,'PropertyVirtualTour')
                        PropertyVirtualTour.text = ET.CDATA(subdivisionProperty['PropertyVirtualTour'])
                        PropertyPlanViewUrl = SubElement(SubdivisionProperty,'PropertyPlanViewUrl')
                        PropertyPlanViewUrl.text = ET.CDATA(subdivisionProperty['PropertyPlanViewUrl'])
                        PropertySchoolComments = SubElement(SubdivisionProperty,'PropertySchoolComments')
                        PropertySchoolComments.text = ET.CDATA(subdivisionProperty['PropertySchoolComments'])
                        PropertyHasHoa = SubElement(SubdivisionProperty,'PropertyHasHoa')
                        PropertyHasHoa.text = ET.CDATA(subdivisionProperty['PropertyHasHoa'])
                        PropertyHoaFee = SubElement(SubdivisionProperty,'PropertyHoaFee')
                        PropertyHoaFee.text = ET.CDATA(subdivisionProperty['PropertyHoaFee'])
                        PropertyHoaBillingPeriod = SubElement(SubdivisionProperty,'PropertyHoaBillingPeriod')
                        PropertyHoaBillingPeriod.text = ET.CDATA(subdivisionProperty['PropertyHoaBillingPeriod'])
                        for propertyFloorPlanImage in subdivisionProperty['PropertyFloorPlanImage']:
                            PropertyFloorPlanImage = SubElement(SubdivisionProperty, 'PropertyFloorPlanImage')
                            PropertyFloorPlanImageURL = SubElement(PropertyFloorPlanImage, 'PropertyFloorPlanImageURL')
                            PropertyFloorPlanImageURL.text = ET.CDATA(propertyFloorPlanImage['PropertyFloorPlanImageUrl'])
                            PropertyFloorPlanImageDescription = SubElement(PropertyFloorPlanImage, 'PropertyFloorPlanImageDescription')
                            PropertyFloorPlanImageDescription.text = ET.CDATA(propertyFloorPlanImage['PropertyFloorPlanImageDescription'])

                        for propertyElevationImage in subdivisionProperty['PropertyElevationImage']:
                            PropertyElevationImage = SubElement(SubdivisionProperty, 'PropertyElevationImage')
                            PropertyElevationImageURL = SubElement(PropertyElevationImage, 'PropertyElevationImageURL')
                            PropertyElevationImageURL.text = ET.CDATA(propertyElevationImage['PropertyElevationImageUrl'])
                            PropertyElevationImageDescription = SubElement(PropertyElevationImage, 'PropertyElevationImageDescription')
                            PropertyElevationImageDescription.text = ET.CDATA(propertyElevationImage['PropertyElevationImageDescription'])

                        for propertyExteriorInteriorImage in subdivisionProperty['PropertyExteriorInteriorImage']:
                            PropertyExteriorInteriorImage = SubElement(SubdivisionProperty, 'PropertyExteriorInteriorImage')
                            PropertyInteriorImageURL = SubElement(PropertyExteriorInteriorImage, 'PropertyInteriorImageURL')
                            PropertyInteriorImageURL.text = ET.CDATA(propertyExteriorInteriorImage['PropertyInteriorImageUrl'])
                            PropertyInteriorImageDescription = SubElement(PropertyExteriorInteriorImage, 'PropertyInteriorImageDescription')
                            PropertyInteriorImageDescription.text = ET.CDATA(propertyExteriorInteriorImage['PropertyInteriorImageDescription'])

                        Promotion = SubElement(SubdivisionProperty, 'Promotion')
                        promotion = subdivisionProperty['Promotion']
                        PromoId = SubElement(Promotion,'PromoId')
                        PromoId.text = ET.CDATA(promotion['PromoId'])
                        PromoType = SubElement(Promotion,'PromoType')
                        PromoType.text = ET.CDATA(promotion['PromoType'])
                        PromoHeadline = SubElement(Promotion,'PromoHeadline')
                        PromoHeadline.text = ET.CDATA(promotion['PromoHeadline'])
                        PromoDescription = SubElement(Promotion,'PromoDescription')
                        PromoDescription.text = ET.CDATA(promotion['PromoDescription'])
                        PromoURL = SubElement(Promotion,'PromoURL')
                        PromoURL.text = ET.CDATA(promotion['PromoUrl'])
                        PromoStartDate = SubElement(Promotion,'PromoStartDate')
                        PromoStartDate.text = ET.CDATA(promotion['PromoStartDate'])
                        PromoEndDate = SubElement(Promotion,'PromoEndDate')
                        PromoEndDate.text = ET.CDATA(promotion['PromoEndDate'])

                for subdivisionFlyer in subdivision['SubdivisionFlyer']:
                    SubdivisionFlyer = SubElement(Subdivision,'SubdivisionFlyer')
                    SubdivisionFlyerImageURL = SubElement(SubdivisionFlyer,'SubdivisionFlyerImageURL')
                    SubdivisionFlyerImageURL.text = ET.CDATA(subdivisionFlyer['SubdivisionFlyerImageUrl'])
                    SubdivisionFlyerDescription = SubElement(SubdivisionFlyer,'SubdivisionFlyerDescription')
                    SubdivisionFlyerDescription.text = ET.CDATA(subdivisionFlyer['SubdivisionFlyerDescription'])

                for subImage in subdivision['SubImage']:
                    SubImage = SubElement(Subdivision,'SubImage')
                    SubImageUrl = SubElement(SubImage,'SubImageURL')
                    SubImageUrl.text = ET.CDATA(subImage['SubImageUrl'])
                    SubImageCaption = SubElement(SubImage,'SubImageCaption')
                    SubImageCaption.text = ET.CDATA(subImage['SubImageCaption'])
                    SubImageURLContentType = SubElement(SubImage,'SubImageURLContentType')
                    SubImageURLContentType.text = ET.CDATA(subImage['SubImageUrlContentType'])
                    SubImageOrderBy = SubElement(SubImage,'SubImageOrderBy')
                    SubImageOrderBy.text = ET.CDATA(subImage['SubImageOrderBy'])
                    MainFlag = SubElement(SubImage,'MainFlag')
                    MainFlag.text = ET.CDATA(subImage['MainFlag'])

                for subVideo in subdivision['SubVideo']:
                    SubVideo = SubElement(Subdivision,'SubVideo')
                    SubVideoURL = SubElement(SubVideo,'SubVideoURL')
                    SubVideoURL.text = ET.CDATA(subVideo['SubVideoUrl'])
                    SubVideoCaption = SubElement(SubVideo,'SubVideoCaption')
                    SubVideoCaption.text = ET.CDATA(subVideo['SubVideoCaption'])
                    SubVideoUrlContentType = SubElement(SubVideo,'SubVideoUrlContentType')
                    SubVideoUrlContentType.text = ET.CDATA(subVideo['SubVideoUrlContentType'])
                    SubVideoOrderBy = SubElement(SubVideo,'SubVideoOrderBy')
                    SubVideoOrderBy.text = ET.CDATA(subVideo['SubVideoOrderBy'])
                    MainFlag = SubElement(SubVideo,'MainFlag')
                    MainFlag.text = ET.CDATA(subVideo['MainFlag'])
                
                Promotion = SubElement(Subdivision, 'Promotion')
                promotion = subdivision['Promotion']
                PromoId = SubElement(Promotion,'PromoId')
                PromoId.text = ET.CDATA(promotion['PromoId'])
                PromoType = SubElement(Promotion,'PromoType')
                PromoType.text = ET.CDATA(promotion['PromoType'])
                PromoHeadline = SubElement(Promotion,'PromoHeadline')
                PromoHeadline.text = ET.CDATA(promotion['PromoHeadline'])
                PromoDescription = SubElement(Promotion,'PromoDescription')
                PromoDescription.text = ET.CDATA(promotion['PromoDescription'])
                PromoURL = SubElement(Promotion,'PromoURL')
                PromoURL.text = ET.CDATA(promotion['PromoUrl'])
                PromoStartDate = SubElement(Promotion,'PromoStartDate')
                PromoStartDate.text = ET.CDATA(promotion['PromoStartDate'])
                PromoEndDate = SubElement(Promotion,'PromoEndDate')
                PromoEndDate.text = ET.CDATA(promotion['PromoEndDate'])

            tree = ET.ElementTree(Builder)
            tree.write('final.xml', encoding='utf-8', xml_declaration=True)

        create_builder_xml(welcome)

        
