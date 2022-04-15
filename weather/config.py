import configparser

config = configparser.ConfigParser()
config.read('configurations.ini')
global apikey 
apikey = config['keys']['wapi']
