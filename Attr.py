import wget
import os
from lxml import etree
import re
from mechanize import Browser

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
def get_new_ids():
      # new xml

    with open('urls.xml', 'rb') as fobj:
        xml = fobj.read()

    root = etree.fromstring(xml)
    new_ids = []
    i = 0
    for roots in root.getchildren():
        rootattr = roots.attrib
        if rootattr.get('internal-id'):
            new_ids.append(rootattr.get('internal-id'))

        i = i + 1


    return new_ids


# returns list of old ids
def get_old_ids(url):
    file = open(url, 'r')
    old = file.readlines()
    old_ids = [old_id.replace('\n', '') for old_id in old]
    return old_ids


# returns uniq ids. this function compares two sets of old and new ids
def ids_validation(old_ids):
    uniq_ids = list(set(get_old_ids(old_ids)) ^ set(get_new_ids()))

    return uniq_ids


# returns dictionary with the all required data
def get_offer_by_id(id):
    history = open('old-ids.txt', 'a')
    with open('urls.xml', 'rb') as fobj:
        xml = fobj.read()

    root = etree.XML(xml)
    offer = get_main_dict()
    shit = root.tag.replace('realty-feed', '')  # getting the yandex-attr i cant track.

    for offered in root.getchildren():
        if offered.attrib.get('internal-id') == str(id):
            offer['offer_internal_id'] = offered.attrib.get('internal-id')
            history.write(str(offered.attrib.get('internal-id')) + "\n")
            history.close()
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
                        if location.tag == shit + 'country' and location.text:
                            offer['location_country'] = location.text.replace(shit, '')

                        if location.tag == shit + 'region' and location.text:
                            offer['location_region'] = location.text.replace(shit, '')

                        if location.tag == shit + 'district' and location.text:
                            offer['location_district'] = location.text.replace(shit, '')

                        if location.tag == shit + 'locality-name' and location.text:
                            offer['location_locality_name'] = location.text.replace(shit, '')

                        if location.tag == shit + 'sub-locality-name' and location.text:
                            offer['location_sub_locality_name'] = location.text.replace(shit, '')

                        if location.tag == shit + 'non-admin-sub-locality' and location.text:
                            offer['location_non_admin_sub_locality'] = location.text.replace(shit, '')

                        if location.tag == shit + 'address' and location.text:
                            offer['location_address'] = location.text.replace(shit, '')

                        if location.tag == shit + 'latitude' and location.text:
                            offer['location_latitude'] = location.text.replace(shit, '')

                        if location.tag == shit + 'longitude' and location.text:
                            offer['location_longitude'] = location.text.replace(shit, '')

                if offer_body.tag == shit + 'sales-agent':
                    for sales_agent in offer_body.getchildren():
                        if sales_agent.tag == shit + 'name' and sales_agent.text:
                            offer['sales_agent_name'] = sales_agent.text.replace(shit, '')

                        if sales_agent.tag == shit + 'email' and sales_agent.text:
                            offer['sales_agent_email'] = sales_agent.text.replace(shit, '')

                if offer_body.tag == shit + 'price':
                    for price in offer_body.getchildren():
                        if price.tag == shit + 'currency' and price.text:
                            offer['price_currency'] = price.text.replace(shit, '')

                        if price.tag == shit + 'value' and price.text:
                            offer['price_value'] = price.text.replace(shit, '')

                        if price.tag == shit + 'period' and price.text:
                            offer['price_period'] = price.text.replace(shit, '')

                if offer_body.tag == shit + 'utilities-included' and offer_body.text:
                    offer['utilities_included'] = offer_body.text

                if offer_body.tag == shit + 'commission' and offer_body.text:
                    offer['commission'] = offer_body.text

                if offer_body.tag == shit + 'room-furniture' and offer_body.text:
                    offer['room_furniture'] = offer_body.text

                if offer_body.tag == shit + 'water-supply' and offer_body.text:
                    offer['water_supply'] = offer_body.text

                if offer_body.tag == shit + 'heating-supply' and offer_body.text:
                    offer['heating_supply'] = offer_body.text

                if offer_body.tag == shit + 'internet' and offer_body.text:
                    offer['internet'] = offer_body.text

                if offer_body.tag == shit + 'area':
                    for area in offer_body.getchildren():
                        if area.tag == shit + 'value' and area.text:
                            offer['area_value'] = area.text

                        if area.tag == shit + 'unit' and area.text:
                            offer['area_unit'] = area.text

                if offer_body.tag == shit + 'floor' and offer_body.text:
                    offer['floor'] = offer_body.text

                if offer_body.tag == shit + 'floors-total' and offer_body.text:
                    offer['floors_total'] = offer_body.text

                if offer_body.tag == shit + 'ceiling-height' and offer_body.text:
                    offer['ceiling_height'] = offer_body.text

                if offer_body.tag == shit + 'phone' and offer_body.text:
                    offer['phone'] = offer_body.text

                if offer_body.tag == shit + 'balcony' and offer_body.text:
                    offer['balcony'] = offer_body.text

                if offer_body.tag == shit + 'description' and offer_body.text:
                    offer['description'] = offer_body.text

                if offer_body.tag == shit + 'platnayaparkovka' and offer_body.text:
                    offer['platnayaparkovka'] = offer_body.text

                if offer_body.tag == shit + 'komunalnieplategy' and offer_body.text:
                    offer['komunalnieplategy'] = offer_body.text

                if offer_body.tag == shit + 'vhod' and offer_body.text:
                    offer['vhod'] = offer_body.text

                if offer_body.tag == shit + 'elektricheskayamoshnost' and offer_body.text:
                    offer['elektricheskayamoshnost'] = offer_body.text

                if offer_body.tag == shit + 'besplatnayaparkovka' and offer_body.text:
                    offer['besplatnayaparkovka'] = offer_body.text

                if offer_body.tag == shit + 'municipalnayaparkovka' and offer_body.text:
                    offer['municipalnayaparkovka'] = offer_body.text

                if offer_body.tag == shit + 'zapasnoyvhod' and offer_body.text:
                    offer['zapasnoyvhod'] = offer_body.text

                if offer_body.tag == shit + 'pandus' and offer_body.text:
                    offer['pandus'] = offer_body.text

                if offer_body.tag == shit + 'menedgerobekta' and offer_body.text:
                    offer['menedgerobekta'] = offer_body.text

                if offer_body.tag == shit + 'dostup24chasa' and offer_body.text:
                    offer['dostup24chasa'] = offer_body.text

                if offer_body.tag == shit + 'kondicioner' and offer_body.text:
                    offer['kondicioner'] = offer_body.text

                if offer_body.tag == shit + 'viddeyatelnosty' and offer_body.text:
                    offer['viddeyatelnosty'] = offer_body.text

                if offer_body.tag == shit + 'srokokupaemosty' and offer_body.text:
                    offer['srokokupaemosty'] = offer_body.text

                if offer_body.tag == shit + 'dohodnost' and offer_body.text:
                    offer['dohodnost'] = offer_body.text

                if offer_body.tag == shit + 'takgepodhodit' and offer_body.text:
                    offer['takgepodhodit'] = offer_body.text

                if offer_body.tag == shit + 'podzemnayaparkovka' and offer_body.text:
                    offer['podzemnayaparkovka'] = offer_body.text

                if offer_body.tag == shit + 'cenasnds' and offer_body.text:
                    offer['cenasnds'] = offer_body.text

                if offer_body.tag == shit + 'nazvanieobekta' and offer_body.text:
                    offer['nazvanieobekta'] = offer_body.text

                if offer_body.tag == shit + 'BuildingClass' and offer_body.text:
                    offer['BuildingClass'] = offer_body.text

                if offer_body.tag == shit + 'tipzdaniya' and offer_body.text:
                    offer['tipzdaniya'] = offer_body.text

                if offer_body.tag == shit + 'sostoyanie' and offer_body.text:
                    offer['sostoyanie'] = offer_body.text

                if offer_body.tag == shit + 'visotapotolkov' and offer_body.text:
                    offer['visotapotolkov'] = offer_body.text


    return offer

def download_file(url):
    wget.download(url, 'C:\\Users\\Cplasplas\\PycharmProjects\\untitled\\urls.xml')


def send_offer(offer):
    br = Browser()
    br.set_handle_robots(False)
    br.open("http://test-parser-bit/")
    br.select_form(id="bxform")
    br.form['DEAL_UF_CRM_1571131808'] = offer['offer_internal_id']
    br.form['DEAL_UF_CRM_1571131826'] = offer['type']
    br.form['DEAL_UF_CRM_1571131838'] = offer['category']
    br.form['DEAL_UF_CRM_1571131851'] = offer['commercial_type']
    br.form['DEAL_UF_CRM_1571131867'] = offer['url']
    br.form['DEAL_UF_CRM_1571131899'] = offer['payed_adv']
    br.form['DEAL_UF_CRM_1571132280'] = offer['location_country']
    br.form['DEAL_UF_CRM_1571132300'] = offer['location_region']
    br.form['DEAL_TITLE'] = offer['location_district']
    br.form['DEAL_TITLE'] = offer['location_locality_name']
    br.form['DEAL_TITLE'] = offer['location_sub_locality_name']
    br.form['DEAL_TITLE'] = offer['location_non_admin_sub_locality']
    br.form['DEAL_TITLE'] = offer['location_address']
    br.form['DEAL_TITLE'] = offer['location_latitude']
    br.form['DEAL_TITLE'] = offer['location_longitude']
    br.form['DEAL_TITLE'] = offer['sales_agent_name']
    br.form['DEAL_TITLE'] = offer['sales_agent_email']
    br.form['DEAL_TITLE'] = offer['price_currency']
    br.form['DEAL_TITLE'] = offer['price_value']
    br.form['DEAL_TITLE'] = offer['price_period']
    br.form['DEAL_TITLE'] = offer['utilities_included']
    br.form['DEAL_TITLE'] = offer['commission']
    br.form['DEAL_TITLE'] = offer['room_furniture']
    br.form['DEAL_TITLE'] = offer['water_supply']
    br.form['DEAL_TITLE'] = offer['heating_supply']
    br.form['DEAL_TITLE'] = offer['internet']
    br.form['DEAL_TITLE'] = offer['area_value']
    br.form['DEAL_TITLE'] = offer['area_unit']
    br.form['DEAL_TITLE'] = offer['floor']
    br.form['DEAL_TITLE'] = offer['floors_total']
    br.form['DEAL_TITLE'] = offer['ceiling_height']
    br.form['DEAL_TITLE'] = offer['phone']
    br.form['DEAL_TITLE'] = offer['balcony']
    br.form['DEAL_TITLE'] = offer['description']
    br.form['DEAL_TITLE'] = offer['platnayaparkovka']
    br.form['DEAL_TITLE'] = offer['komunalnieplategy']
    br.form['DEAL_TITLE'] = offer['vhod']
    br.form['DEAL_TITLE'] = offer['elektricheskayamoshnost']
    br.form['DEAL_TITLE'] = offer['besplatnayaparkovka']
    br.form['DEAL_TITLE'] = offer['municipalnayaparkovka']
    br.form['DEAL_TITLE'] = offer['zapasnoyvhod']
    br.form['DEAL_TITLE'] = offer['pandus']
    br.form['DEAL_TITLE'] = offer['menedgerobekta']
    br.form['DEAL_TITLE'] = offer['dostup24chasa']
    br.form['DEAL_TITLE'] = offer['kondicioner']
    br.form['DEAL_TITLE'] = offer['viddeyatelnosty']
    br.form['DEAL_TITLE'] = offer['srokokupaemosty']
    br.form['DEAL_TITLE'] = offer['dohodnost']
    br.form['DEAL_TITLE'] = offer['takgepodhodit']
    br.form['DEAL_TITLE'] = offer['podzemnayaparkovka']
    br.form['DEAL_TITLE'] = offer['cenasnds']
    br.form['DEAL_TITLE'] = offer['nazvanieobekta']
    br.form['DEAL_TITLE'] = offer['BuildingClass']
    br.form['DEAL_TITLE'] = offer['tipzdaniya']
    br.form['DEAL_TITLE'] = offer['sostoyanie']
    br.form['DEAL_TITLE'] = offer['visotapotolkov']

    br.submit()


if __name__ == "__main__":
    download_file('https://base.kvartus.ru/reklama/xml/base/9995/yrl_bitrix.xml')
    for fff in ids_validation('old-ids.txt'):
        print(get_offer_by_id(fff))
        send_offer(get_offer_by_id(fff))
    #print(get_offer_by_id('https://base.kvartus.ru/reklama/xml/base/9995/yrl_bitrix.xml', 2949158))
    os.remove('urls.xml')


