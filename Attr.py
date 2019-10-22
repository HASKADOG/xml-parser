import wget
import os
from lxml import etree

#https://base.kvartus.ru/reklama/xml/base/9995/yrl_bitrix.xml
#This is my first comercial python script

#returns string without {http://webmaster.yandex.ru/schemas/feed/realty/2010-06}
def my_print(string, shit):
    print(string.replace(shit,''))

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


def get_offer_by_id(xmlFile, id):
    wget.download(xmlFile, 'C:\\Users\\Cplasplas\\PycharmProjects\\untitled\\urls.xml')
    with open('urls.xml', 'rb') as fobj:
        xml = fobj.read()

    root = etree.XML(xml)

    shit = root.tag.replace('realty-feed','') # getting the yandex-attr i cant track.

    for offer in root.getchildren():
        if offer.attrib.get('internal-id') == str(id):
            print(offer)
            '''
            for trololo in pepe.getchildren():
                suchka = trololo.tag
                if trololo.tag != shit + 'image':
                    my_print(trololo.tag, shit)
            '''


    os.remove('urls.xml')


if __name__ == "__main__":
   get_offer_by_id('https://base.kvartus.ru/reklama/xml/base/9995/yrl_bitrix.xml', 889283)
