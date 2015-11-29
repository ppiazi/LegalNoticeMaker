# -*- coding: utf-8 -*-
"""
Copyright 2015 Joohyun Lee(ppiazi@gmail.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys
import os
import getopt
import csv
from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))

class LegalNoticeMaker:
    def __init__(self, swinfo_file="swinfo.csv", ossinfo_file="data.csv"):
        self.env = Environment(loader=FileSystemLoader(os.path.join(PATH, 'templates')))
        self.txt_maker = self.env.get_template('legal-notice-txt.template')
        self.oss_list = []
        self.oss_license_list = []
        self.oss_license_dict = {}
        self.info = {}
        self.swinfo_file = swinfo_file
        self.ossinfo_file = ossinfo_file

        self.readSwData()
        self.readOssInfo()
        self.makeLegalNotice()

    def readSwData(self):
        fo = open(self.swinfo_file, "r")
        csv_reader = csv.reader(fo, delimiter=",")

        row_cnt = 0
        for row_data in csv_reader:
            if row_cnt == 0:
                row_cnt = row_cnt + 1
                continue
            self.info['sw'] = row_data[0]
            self.info['sw_year'] = row_data[1]
            self.info['company_name'] = row_data[2]
            self.info['company_email'] = row_data[3]
            break
        fo.close()

    def readOssInfo(self):
        fo = open(self.ossinfo_file, "r")
        csv_reader = csv.reader(fo, delimiter=",")

        row_cnt = 0
        for row_data in csv_reader:
            if row_cnt == 0:
                row_cnt = row_cnt + 1
                continue
            row_cnt = row_cnt + 1

            # temporary oss entity
            temp_oss = {}
            temp_oss["oss"] = row_data[0]
            temp_oss["oss_url"] = row_data[1]
            temp_oss["oss_copyright"] = row_data[2]
            temp_oss["oss_license"] = row_data[3]
            temp_oss["oss_etc"] = row_data[4]
            self.oss_list.append(temp_oss)

            # temporary oss entity
            temp_oss_license = {}
            temp_oss_license["oss_license"] = temp_oss["oss_license"]
            temp_oss_license["oss_license_notice"] = self.readLicenseNotice(temp_oss_license["oss_license"])
            self.oss_license_dict[temp_oss_license["oss_license"]] = temp_oss_license

        # sort oss_license_dict by key
        for t_key in sorted(self.oss_license_dict):
            self.oss_license_list.append(self.oss_license_dict[t_key])
        fo.close()

    def readLicenseNotice(self, oss_license):
        notice = ""

        license_file = "..\\license-list\\" + oss_license + ".txt"

        try:
            fo = open(license_file, "r")
            notice = fo.read()
            fo.close()
        except:
            notice = "ERROR : %s" % (license_file)

        return notice

    def makeLegalNotice(self):
        fo = open("output.txt", "w")
        fo.write(self.txt_maker.render(info=self.info, oss_list=self.oss_list, oss_license_list=self.oss_license_list))
        fo.close()

def printUsage():
    print("LegalNoticeMaker.py [-s <swinfo file>] [-d <ossdata file>]")

if __name__ == "__main__":
    optlist, args = getopt.getopt(sys.argv[1:], "s:d:o:")

    p_swinfo = None
    p_ossinfo = None

    for op, p in optlist:
        if op == "-s":
            p_swinfo = p
        elif op == "-d":
            p_ossinfo = p
        else:
            print("Invalid Argument : %s / %s" % (op, p))
            os._exit(1)

    if p_swinfo == None or p_ossinfo == None:
        printUsage()
        os._exit(1)

    LNM = LegalNoticeMaker(p_swinfo, p_ossinfo)



