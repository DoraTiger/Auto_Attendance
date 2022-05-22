import yaml

def loadConfig(filename,configname=''):
    config = ""
    with open(filename, "r", encoding='utf-8') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    if(configname != ''):
        return config[configname]
    else:
        return config


# def loadStudent():
#     studentList = ""
#     with open("config.yaml", "r", encoding='utf-8') as config_file:
#         studentList = yaml.load(config_file, Loader=yaml.FullLoader)['student']
#     return studentList