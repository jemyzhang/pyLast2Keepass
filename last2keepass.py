# -*- coding: UTF-8 -*-
__author__ = 'jemyzhang'

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
#from xml.etree.ElementTree import dump
#from xml.etree.ElementTree import Comment
#from xml.etree.ElementTree import tostring
import sys
import datetime


def parse_lastpass_cvs(filename):
    ret = list()
    try:
        fcvs = open(filename, 'r')
        l = fcvs.readline().replace('\n', '').replace('"', '')
        #readout title
        if len(l) == 0:
            return ret
        title = l.split(',')
        while True:
            l = fcvs.readline().replace('\n', '').replace('"', '')
            if len(l) == 0:
                break
            e = l.split(',')
            if len(e) < len(title):
                l += '\n'
                l += fcvs.readline().replace('\n', '').replace('"', '')
                e = l.split(',')
            ret.append(dict(zip(title, e)))
    except IOError:
        print('open %s error', filename)
    finally:
        return ret


def add_group(group, item):
    if isinstance(group, list):
        if not item in group:
            group.append(item)

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    return elem

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('usage:\n'
              '%s [input lastpass cvs] [ouput keepass xml]', sys.argv[0])
    else:
        dictcvs = parse_lastpass_cvs(sys.argv[1])
        dictgroup = list()
        for i in dictcvs:
            if isinstance(i, dict):
                if i.get('grouping') == '':
                    i['grouping'] = 'undefined'
                add_group(dictgroup, i.get('grouping'))
            #create xml book
        book = ElementTree() # '!DOCTYPE KEEPASSX_DATABASE')
        database = Element('database')
        book._setroot(database)
        item = Element('group')
        database.append(item)

        SubElement(item, 'title').text = 'Internet'
        SubElement(item, 'icon').text = '1'

        for i in dictgroup:
            subgroup = Element('group')
            item.append(subgroup)
            SubElement(subgroup, 'title').text = i.decode('UTF-8')
            SubElement(subgroup, 'icon').text = '19'
            for e in dictcvs:
                if isinstance(e, dict):
                    if e.get('grouping') == i:
                        entry = Element('entry')
                        subgroup.append(entry)
                        SubElement(entry, 'title').text = e.get('name').decode('UTF-8')
                        SubElement(entry, 'username').text = e.get('username').decode('UTF-8')
                        SubElement(entry, 'password').text = e.get('password')
                        SubElement(entry, 'url').text = e.get('url')
                        SubElement(entry, 'comment').text = e.get('extra').decode('UTF-8')
                        SubElement(entry, 'icon').text = '19'
                        SubElement(entry, 'creation').text = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                        SubElement(entry, 'lastaccess').text = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                        SubElement(entry, 'lastmod').text = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                        SubElement(entry, 'expire').text = u'Never'


        #SubElement(database, 'group', {'title': 'Internet', 'icon': '1'})
        #dump(indent(database))
        indent(database)
        book.write(sys.argv[2], encoding='utf-8')
