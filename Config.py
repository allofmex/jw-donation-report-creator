import yaml
import string

class Config:

    CONG_NAME='congregationName'
    COORDINATOR_TEXT='coordinatorText'
    PLACE='place'
    
    FIX_OVERVIEW_SUM_FIELD_NAME='customSumField1'
    FIX_LIST_SUM_FIELD_NAME='customSumField2'
    
    def __init__(self, configFilePath):
        file = open(configFilePath, 'r')
        self.content = yaml.load(file, Loader=yaml.SafeLoader)

    def get(self, key, required: bool = True):
        if key not in self.content:
            if required == True: 
                raise Exception("Key {key} missing in config file!")
            else: 
                return None
        data = self.content[key]
        if required == True and data is None:
            raise Exception("Key {key} is empty in config file!")
        return data