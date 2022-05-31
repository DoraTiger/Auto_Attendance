import yaml

def loadConfig(filename, configname=''):
    config = ""
    with open(filename, "r", encoding='utf-8') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    if(configname != ''):
        return config[configname]
    else:
        return config


def getProxies():
    proxyConfig = loadConfig("config.yaml", "config")["proxy"]
    enablePrxies = proxyConfig.get('enable', False)
    protocol = proxyConfig.get('protocol', 'http')
    addr = proxyConfig.get('addr', '')
    proxies = {
        'http': None,
        'https': None
    }
    if(enablePrxies and addr != ''):
        proxies['http'] = protocol+'://'+addr
        proxies['https'] = protocol+'://'+addr

    return proxies