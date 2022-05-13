import configparser

class Config():

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

    
    def get_value(self, section, key):
        return self.config[section][key]



if __name__ == "__main__":
    
    c = Config()
    print(c.get_value('AZUREIMAGE','ENDPOINT'))

