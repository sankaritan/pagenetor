Pagenetor - selenium webdriver page object generator
============

Script generating page-object files from JSON data object.

### How to use

1. create project folder under projects
1. create "input_data" and  "templates" folders in project folder
1. add json file(s) with locator data (see example file)
1. add template file to template folder, make sure the file format is: "[name_of_template].[file_extension].[tmpl]" (see example template files)
1. set correct values in "config.properties" configuration files
1. run "pagenerator.py"
1. verify page object files have been created under project folder > "output" folder

### Required libraries

* ```pip install Jinja2```

### Future enhancements

* enhance existing templates and JSON files to support generation of more complex structures
* connect with some tool that would automatically parse locator information from pages generating output JSON file (which this script could use as input value)