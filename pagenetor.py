# /usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import os
import glob
import json

from jinja2 import Environment, FileSystemLoader


class PageGenerator():
    def __init__(self):
        self.test_vars = self.load_configuration()
        self.project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'projects',
                                         self.test_vars.get('project_dir'))
        self.data_folder = os.path.join(self.project_root, 'input_data')
        self.template_folder = os.path.join(self.project_root, 'templates')
        self.output_folder = os.path.join(self.project_root, 'output')
        self.template_file_name = self.test_vars.get('template_file_name')
        self.data_expression = self.test_vars.get('data_expression')

    def load_configuration(self):
        """ loads configuration variables from .properties file """
        config = ConfigParser.ConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.properties')
        config.read(config_file)
        return dict(config.defaults())

    def run(self):
        """ runs page object generation """
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        for entry in glob.glob(os.path.join(self.data_folder, self.data_expression)):
            f = open(entry)
            text = json.loads(f.read())
            f.close()
            self.create_page_objects(text)

    def create_page_objects(self, data):
        """ initiates page object generation for each entry in json array """
        for page in data['pages']:
            self.create_page(page)

    def create_page(self, data):
        """ generates one page object file """
        env = Environment(loader=FileSystemLoader(self.template_folder), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(self.template_file_name)
        template_vars = {'class_name': self.get_class_name(data['name']), 'page': data}
        output = template.render(template_vars)
        formatted_output = output.encode('utf8').strip()
        file_name = data['name'] + self.get_output_file_type()
        result_html = open(os.path.join(self.output_folder, file_name), 'w')
        result_html.write(formatted_output)
        result_html.close()

    def get_output_file_type(self):
        """ returns file type of output page object files """
        file_name = '.' + self.template_file_name.split('.')[-2]
        return file_name

    def get_class_name(self, name):
        """ converts file name to class name (camel-case) """
        name_list = name.split('_')
        file_name = ''
        for item in name_list:
            file_name += item.capitalize()
        return file_name