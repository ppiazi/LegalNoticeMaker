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
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(os.path.join(PATH, 'templates')))
        self.txt_maker = self.env.get_template('legal-notice-txt.template')
        self.oss_list = []
        self.oss_license_list = []
        self.info = {}
        self.info['sw'] = "Test SW"
        self.info['sw_year'] = "2015"
        self.info['company_name'] = "PPIAZI"
        self.info['company_email'] = "ppiazi@gmail.com"

        self.readCsv()
        self.make()

    def readCsv(self):
        fo = open("data.csv", "r")
        csv_reader = csv.reader(fo, delimiter=",")
        row_cnt = 0
        for row_data in csv_reader:
            if row_cnt == 0:
                row_cnt = row_cnt + 1
                continue
            row_cnt = row_cnt + 1

            temp_oss = {}
            temp_oss["oss"] = row_data[0]
            temp_oss["oss_url"] = row_data[1]
            temp_oss["oss_copyright"] = row_data[2]
            temp_oss["oss_license"] = row_data[3]
            temp_oss["oss_etc"] = row_data[4]

            temp_oss_license = {}
            temp_oss_license["oss_license"] = temp_oss["oss_license"]
            temp_oss_license["oss_license_notice"] = self.readLicenseNotice(temp_oss_license["oss_license"])
            self.oss_license_list.append(temp_oss_license)

            self.oss_list.append(temp_oss)

    def readLicenseNotice(self, oss_license):
        notice = ""

        return notice

    def make(self):
        fo = open("output.txt", "w")
        fo.write(self.txt_maker.render(info=self.info, oss_list=self.oss_list, oss_license_list=self.oss_license_list))
        fo.close()

if __name__ == "__main__":
	LNM = LegalNoticeMaker()
