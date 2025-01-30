import configparser

config = configparser.ConfigParser()

# Add the structure to the file we will create
config.add_section('path')
config.set('path', 'base_path', r'C:\Users\prashant.bhosale\my project\advance_web_scraping')

with open(r"C:\Users\prashant.bhosale\my project\advance_web_scraping\config.ini", 'w') as configfile:
    config.write(configfile)