#  generate_metainfo.py - Generate XML for SMF Extension
#
#  Copyright (c) 2013 David Capron (drbluesman@yahoo.com)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
# Based on example by jan@biochemfusion.com
#
import os
cur_dir = os.getcwd()

# A unique ID for the extension.
addin_id = "com.smf.ticker.getinfo"
addin_version = "0.7.1"
addin_displayname = "Stock Market Function Extension."
addin_publisher_link = "https://github.com/madsailor/SMF-Extension"
addin_publisher_name = "David Capron"

# description.xml
desc_xml = open(cur_dir + '/SMF/description.xml', 'w')

desc_xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
desc_xml.write('<description\n')
desc_xml.write('xmlns="http://openoffice.org/extensions/description/2006"\n')
desc_xml.write('xmlns:d="http://openoffice.org/extensions/description/2006"\n')
desc_xml.write('xmlns:xlink="http://www.w3.org/1999/xlink">\n')
desc_xml.write('  <dependencies>\n')
desc_xml.write('    <OpenOffice.org-minimal-version value="2.4" d:name="OpenOffice.org 2.4"/>\n')
desc_xml.write('  </dependencies>\n')
desc_xml.write('  <identifier value="' + addin_id + '"/>\n')
desc_xml.write('  <version value="' + addin_version + '"/>\n')   
desc_xml.write('  <display-name>\n')
desc_xml.write('    <name lang="en">' + addin_displayname + '</name>\n')
desc_xml.write('  </display-name>\n')
desc_xml.write('  <publisher>\n')
desc_xml.write('    <name xlink:href="' + addin_publisher_link + '" lang="en">' + addin_publisher_name + '</name>\n')
desc_xml.write('  </publisher>\n')
desc_xml.write('  <extension-description>\n')
desc_xml.write('    <src xlink:href="description-en-US.txt" lang="en"/>\n')
desc_xml.write('  </extension-description>\n')
desc_xml.write('</description>\n')

desc_xml.close

# manifest.xml - A List of files reference in the .rdb and their types.
def add_manifest_entry(xml_file, file_type, file_name):
    xml_file.write('<manifest:file-entry manifest:media-type="application/vnd.sun.star.' + file_type + '"\n')
    xml_file.write('    manifest:full-path="' + file_name + '"/>\n')

manifest_xml = open(cur_dir + '/SMF/META-INF/manifest.xml', 'w')

manifest_xml.write('<manifest:manifest>\n');
add_manifest_entry(manifest_xml, 'uno-typelibrary;type=RDB', 'Xsmf.rdb')
add_manifest_entry(manifest_xml, 'configuration-data', 'SMF.xcu')
add_manifest_entry(manifest_xml, 'uno-component;type=Python', 'smf.py')
manifest_xml.write('</manifest:manifest>\n')

manifest_xml.close

# SMF.xcu - Configuration file for the extension
# The named UNO component instantiated by Python.
instance_id = "com.smf.ticker.getinfo.python.SmfImpl"
# Name of the Excel add-in if you want to share documents across OOo and Excel.
excel_addin_name = ""

def define_function(xml_file, function_name, description, parameters):
    xml_file.write('      <node oor:name="' + function_name + '" oor:op="replace">\n')
    xml_file.write('        <prop oor:name="DisplayName">\n')
    xml_file.write('          <value xml:lang="en">' + function_name + '</value>\n')
    xml_file.write('        </prop>\n')
    xml_file.write('        <prop oor:name="Description">\n')
    xml_file.write('          <value xml:lang="en">' + description + '</value>\n')
    xml_file.write('        </prop>\n')
    xml_file.write('        <prop oor:name="Category">\n')
    xml_file.write('          <value>Add-In</value>\n')
    xml_file.write('        </prop>\n')
    xml_file.write('        <prop oor:name="CompatibilityName">\n')
    xml_file.write('          <value xml:lang="en">AutoAddIn.XSmf.' + function_name + '</value>\n')
    xml_file.write('        </prop>\n')
    xml_file.write('        <node oor:name="Parameters">\n')

    for p, desc in parameters:
        # Optional parameters will have a displayname enclosed in square brackets.
        p_name = p.strip("[]")        
        xml_file.write('          <node oor:name="' + p_name + '" oor:op="replace">\n')
        xml_file.write('            <prop oor:name="DisplayName">\n')
        xml_file.write('              <value xml:lang="en">' + p_name + '</value>\n')
        xml_file.write('            </prop>\n')
        xml_file.write('            <prop oor:name="Description">\n')
        xml_file.write('              <value xml:lang="en">' + desc + '</value>\n')
        xml_file.write('            </prop>\n')
        xml_file.write('          </node>\n')

    xml_file.write('        </node>\n')
    xml_file.write('      </node>\n')

smf_xml = open(cur_dir + '/SMF/SMF.xcu', 'w')

smf_xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
smf_xml.write('<oor:component-data xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" oor:name="CalcAddIns" oor:package="org.openoffice.Office">\n')
smf_xml.write('<node oor:name="AddInInfo">\n')
smf_xml.write('  <node oor:name="' + instance_id + '" oor:op="replace">\n')
smf_xml.write('    <node oor:name="AddInFunctions">\n')

define_function(smf_xml, \
    'getYahoo', 'Fetches Yahoo Financial Data.  a = "TICKER", b = "DATACODE"', \
    [('a', 'The ticker symbol.'), ('b', 'The data code.')])
define_function(smf_xml, \
    'getMorningKey', \
    'Fetches Morningstar Key Ratios (11yr).  a = "TICKER", b = "DATACODE"', \
    [('a', 'The ticker symbol.'), ('b', 'The data code.')])
define_function(smf_xml, \
    'getMorningFin', \
    'Fetches Morningstar Financials (5yr).  a = "TICKER", b = "DATACODE"', \
    [('a', 'The ticker symbol.'), ('b', 'The data code.')])
define_function(smf_xml, \
    'getMorningQFin', \
    'Fetches Morningstar Quarterly Financials (5qtr).  a = "TICKER", b = "DATACODE"', \
    [('a', 'The ticker symbol.'), ('b', 'The data code.')])
define_function(smf_xml, \
    'getADVFN', 'Fetches ADVFN Financial Data.  a = "TICKER", b = "DATACODE"', \
    [('a', 'The ticker symbol.'), ('b', 'The data code."')])

smf_xml.write('    </node>\n')
smf_xml.write('  </node>\n')
smf_xml.write('</node>\n')
smf_xml.write('</oor:component-data>\n')

smf_xml.close
