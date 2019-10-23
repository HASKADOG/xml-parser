import wget
import os
from lxml import etree


# https://base.kvartus.ru/reklama/xml/base/9995/yrl_bitrix.xml
# This is my first comercial python script

# returns string without {http://webmaster.yandex.ru/schemas/feed/realty/2010-06}
def my_print(string, shit):
    print(string.replace(shit, ''))


def del_y(string, shit):
    return string.replace(shit, '')


# return main dict. DO NOT CHANGE! CHANGES CAN KILL ALL THE PROGRAM!
def get_main_dict():
    offer = dict(
        offer_internal_id='None',
        type='None',
        category='None',
        commercial_type='None',
        url='None',
        payed_adv='None',
        location_country='None',
        location_region='None',
        location_district='None',
        location_locality_name='None',
        location_sub_locality_name='None',
        location_non_admin_sub_locality='None',
        location_address='None',
        location_latitude='None',
        location_longitude='None',
        sales_agent_name='None',
        sales_agent_email='None',
        price_currency='None',
        price_value='None',
        price_period='None',
        utilities_included='None',
        commission='None',
        room_furniture='None',
        water_supply='None',
        heating_supply='None',
        internet='None',
        area_value='None',
        area_unit='None',
        floor='None',
        floors_total='None',
        ceiling_height='None',
        phone='None',
        balcony='None',
        description='None',
        platnayaparkovka='None',
        komunalnieplategy='None',
        vhod='None',
        elektricheskayamoshnost='None',
        besplatnayaparkovka='None',
        municipalnayaparkovka='None',
        zapasnoyvhod='None',
        pandus='None',
        menedgerobekta='None',
        dostup24chasa='None',
        kondicioner='None',
        viddeyatelnosty='None',
        srokokupaemosty='None',
        dohodnost='None',
        takgepodhodit='None',
        podzemnayaparkovka='None',
        cenasnds='None',
        nazvanieobekta='None',
        BuildingClass='None',
        tipzdaniya='None',
        sostoyanie='None',
        visotapotolkov='None',
    )

    return offer


def get_attrs(roots):
    for root in roots.getchildren():
        rootattr = root.attrib
        print(rootattr.get('internal-id'))
        oldId = open('old-ids.txt', 'a')
        if str(rootattr.get('internal-id')) == "None":
            oldId.close()
        else:
            oldId.write(str(rootattr.get('internal-id')) + '\n')
            oldId.close()


# returns list of new ids
def get_new_ids(url):
    wget.download(url, 'C:\\Users\\Cplasplas\\PycharmProjects\\untitled\\urls.xml')  # new xml

    with open('urls.xml', 'rb') as fobj:
        xml = fobj.read()

    root = etree.fromstring(xml)
    new_ids = []
    i = 0
    for roots in root.getchildren():
        rootattr = roots.attrib
        if str(rootattr.get('internal-id')) == "None":
            continue
        else:
            new_ids.append(int(rootattr.get('internal-id')))

        i = i + 1

    os.remove('urls.xml')
    return new_ids


# returns list of old ids
def get_old_ids(url):
    file = open(url, 'r')
    old = file.readlines()
    old_ids = [int(old_id.replace('\n', '')) for old_id in old]
    return old_ids


# returns uniq ids. this function compares two sets of old and new ids
def ids_validation(xml, url):
    uniq_ids = list(set(get_old_ids(url)) ^ set(get_new_ids(xml)))

    return uniq_ids


# returns dictionary with the all required data
def get_offer_by_id(xmlFile, id):
    wget.download(xmlFile, 'C:\\Users\\Cplasplas\\PycharmProjects\\untitled\\urls.xml')
    with open('urls.xml', 'rb') as fobj:
        xml = fobj.read()

    root = etree.XML(xml)
    offer = get_main_dict()
    shit = root.tag.replace('realty-feed', '')  # getting the yandex-attr i cant track.

    for offered in root.getchildren():
        if offered.attrib.get('internal-id') == str(id):
            offer['offer_internal_id'] = offered.attrib.get('internal-id')
            for offer_body in offered.getchildren():

                if offer_body.tag == shit + 'type':
                    offer['type'] = offer_body.text

                if offer_body.tag == shit + 'category':
                    offer['category'] = offer_body.text

                if offer_body.tag == shit + 'commercial-type':
                    offer['commercial_type'] = offer_body.text

                if offer_body.tag == shit + 'url':
                    offer['url'] = offer_body.text

                if offer_body.tag == shit + 'payed-adv':
                    offer['payed_adv'] = offer_body.text

                if offer_body.tag == shit + 'location':
                    for location in offer_body.getchildren():
                        if location.tag == shit + 'country':
                            offer['location_country'] = location.text.replace(shit, '')

                        if location.tag == shit + 'region':
                            offer['location_region'] = location.text.replace(shit, '')

                        if location.tag == shit + 'district':
                            offer['location_district'] = location.text.replace(shit, '')

                        if location.tag == shit + 'locality-name':
                            offer['location_locality_name'] = location.text.replace(shit, '')

                        if location.tag == shit + 'sub-locality-name':
                            offer['location_sub_locality_name'] = location.text.replace(shit, '')

                        if location.tag == shit + 'non-admin-sub-locality':
                            offer['location_non_admin_sub_locality'] = location.text.replace(shit, '')

                        if location.tag == shit + 'address':
                            offer['location_address'] = location.text.replace(shit, '')

                        if location.tag == shit + 'latitude':
                            offer['location_latitude'] = location.text.replace(shit, '')

                        if location.tag == shit + 'longitude':
                            offer['location_longitude'] = location.text.replace(shit, '')

                if offer_body.tag == shit + 'sales-agent':
                    for sales_agent in offer_body.getchildren():
                        if sales_agent.tag == shit + 'name':
                            offer['sales_agent_name'] = sales_agent.text.replace(shit, '')

                        if sales_agent.tag == shit + 'email':
                            offer['sales_agent_email'] = sales_agent.text.replace(shit, '')

                if offer_body.tag == shit + 'price':
                    for price in offer_body.getchildren():
                        if price.tag == shit + 'currency':
                            offer['price_currency'] = price.text.replace(shit, '')

                        if price.tag == shit + 'value':
                            offer['price_value'] = price.text.replace(shit, '')

                        if price.tag == shit + 'period':
                            offer['price_period'] = price.text.replace(shit, '')

                if offer_body.tag == shit + 'utilities-included':
                    offer['utilities_included'] = offer_body.text

                if offer_body.tag == shit + 'commission':
                    offer['commission'] = offer_body.text

                if offer_body.tag == shit + 'room-furniture':
                    offer['room_furniture'] = offer_body.text

                if offer_body.tag == shit + 'water-supply':
                    offer['water_supply'] = offer_body.text

                if offer_body.tag == shit + 'heating-supply':
                    offer['heating_supply'] = offer_body.text

                if offer_body.tag == shit + 'internet':
                    offer['internet'] = offer_body.text

                if offer_body.tag == shit + 'area':
                    for area in offer_body.getchildren():
                        if area.tag == shit + 'value':
                            offer['area_value'] = area.text

                        if area.tag == shit + 'unit':
                            offer['area_unit'] = area.text

                if offer_body.tag == shit + 'floor':
                    offer['floor'] = offer_body.text

                if offer_body.tag == shit + 'floors-total':
                    offer['floors_total'] = offer_body.text

                if offer_body.tag == shit + 'ceiling-height':
                    offer['ceiling_height'] = offer_body.text

                if offer_body.tag == shit + 'phone':
                    offer['phone'] = offer_body.text

                if offer_body.tag == shit + 'balcony':
                    offer['balcony'] = offer_body.text

                if offer_body.tag == shit + 'description':
                    offer['description'] = offer_body.text

                if offer_body.tag == shit + 'platnayaparkovka':
                    offer['platnayaparkovka'] = offer_body.text

                if offer_body.tag == shit + 'komunalnieplategy':
                    offer['komunalnieplategy'] = offer_body.text

                if offer_body.tag == shit + 'vhod':
                    offer['vhod'] = offer_body.text

                if offer_body.tag == shit + 'komunalnieplategy':
                    offer['komunalnieplategy'] = offer_body.text

                if offer_body.tag == shit + 'elektricheskayamoshnost':
                    offer['elektricheskayamoshnost'] = offer_body.text

                if offer_body.tag == shit + 'besplatnayaparkovka':
                    offer['besplatnayaparkovka'] = offer_body.text

                if offer_body.tag == shit + 'municipalnayaparkovka':
                    offer['municipalnayaparkovka'] = offer_body.text

                if offer_body.tag == shit + 'zapasnoyvhod':
                    offer['zapasnoyvhod'] = offer_body.text

                if offer_body.tag == shit + 'pandus':
                    offer['pandus'] = offer_body.text

                if offer_body.tag == shit + 'menedgerobekta':
                    offer['menedgerobekta'] = offer_body.text

                if offer_body.tag == shit + 'dostup24chasa':
                    offer['dostup24chasa'] = offer_body.text

                if offer_body.tag == shit + 'kondicioner':
                    offer['kondicioner'] = offer_body.text

                if offer_body.tag == shit + 'viddeyatelnosty':
                    offer['viddeyatelnosty'] = offer_body.text

                if offer_body.tag == shit + 'srokokupaemosty':
                    offer['srokokupaemosty'] = offer_body.text

                if offer_body.tag == shit + 'dohodnost':
                    offer['dohodnost'] = offer_body.text

                if offer_body.tag == shit + 'takgepodhodit':
                    offer['takgepodhodit'] = offer_body.text

                if offer_body.tag == shit + 'podzemnayaparkovka':
                    offer['podzemnayaparkovka'] = offer_body.text

                if offer_body.tag == shit + 'cenasnds':
                    offer['cenasnds'] = offer_body.text

                if offer_body.tag == shit + 'nazvanieobekta':
                    offer['nazvanieobekta'] = offer_body.text

                if offer_body.tag == shit + 'BuildingClass':
                    offer['BuildingClass'] = offer_body.text

                if offer_body.tag == shit + 'tipzdaniya':
                    offer['tipzdaniya'] = offer_body.text

                if offer_body.tag == shit + 'sostoyanie':
                    offer['sostoyanie'] = offer_body.text

                if offer_body.tag == shit + 'visotapotolkov':
                    offer['visotapotolkov'] = offer_body.text

    os.remove('urls.xml')
    return offer


if __name__ == "__main__":
    offer = get_offer_by_id('https://base.kvartus.ru/reklama/xml/base/9995/yrl_bitrix.xml', 889283)

    print(offer)
