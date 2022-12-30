import yaml

class Config:

    CONG_NAME='congregationName'
    COORDINATOR_TEXT='coordinatorText'
    PLACE='place'
    
    def __init__(self, configFilePath):
        file = open(configFilePath, 'r')
        self.content = yaml.load(file, Loader=yaml.SafeLoader)

    def get(self, key, required: bool = True):
        if required == True and key not in self.content:
            raise Exception("Key {key} missing in config file!")
        data = self.content[key]
        if required == True and data is None:
            raise Exception("Key {key} is empty in config file!")
        return data