# /usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import os
from bs4 import BeautifulSoup
import requests
import json
import re


class PageScraper():
    def __init__(self):
        self.test_vars = self.load_configuration()
        self.project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'projects',
                                         self.test_vars.get('project_dir'))
        self.data_folder = os.path.join(self.project_root, 'input_data')
        self.template_folder = os.path.join(self.project_root, 'templates')
        self.output_folder = os.path.join(self.project_root, 'output')
        self.template_file_name = self.test_vars.get('template_file_name')
        self.data_expression = self.test_vars.get('data_expression')

        self.site_url = self.test_vars.get('page_url')
        self.soup = BeautifulSoup(requests.get(self.site_url).text)
        self.elements_collected = []

    def load_configuration(self):
        """ loads configuration variables from .properties file """
        config = ConfigParser.ConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.properties')
        config.read(config_file)
        return dict(config.defaults())

    def collect_id(self, element):
        self.elements_collected.append(
            {"name": element.name + '_' + element['id'],
             "id_method": "ID",
             "locator": element['id'],
             "unique": True})

    def collect_link(self, element):
        if element.name == 'a':
            self.elements_collected.append(
                {"name": element.name + '_' + re.sub(r'\'|\"|\n', '', element.text[:10].lower().replace(' ', '')),
                 "id_method": "LINK_TEXT",
                 "locator": re.sub(r'\n', '', element.text.replace('\'', '\\\'')).strip(),
                 "unique": True})

    def collect_input(self, element):
        if element.name == 'input':
            if element.has_attr('class'):
                selector_value = element.name + self.get_css_selector(element['class'])
                self.elements_collected.append(
                    {"name": element.name + '_' + selector_value,
                     "id_method": "CSS_SELECTOR",
                     "locator": selector_value,
                     "unique": True})

    def get_css_selector(self, class_value):
        return '.' + str(class_value).replace(' ', '.')

    def get_page_name_value(self, page_title):
        return page_title.lower().replace(' ', '_')

    def get_scraped_elements(self):
        element_list = self.soup.find_all()
        print len(element_list)
        for element in element_list:
            if element.has_attr('id'):
                self.collect_id(element)
            else:
                self.collect_link(element)
                self.collect_input(element)
        return self.elements_collected

    def run(self):
        output_json = {
            "pages": [
                {
                    "name": self.get_page_name_value(self.soup.title.text),
                    "comment": "",
                    "locators": self.get_scraped_elements()
                }
            ]
        }

        self.save_output_json_file(output_json)

    def save_output_json_file(self, data):
        """ saves result data into the file """
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        file_name = os.path.join(self.data_folder, 'pages.json')
        if os.path.isfile(file_name):
            os.remove(file_name)
        f = open(file_name, 'w')
        f.write(json.dumps(data).encode('utf8'))
        f.close()