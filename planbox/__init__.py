from util import HTTPClient,DotDict
import os,re, yaml

class PlanboxAPI():

    def __init__(self):
        '''Initializes a fetcher and uses planbox.yaml to populate a listing of endpoints'''
        self.fetcher = HTTPClient()
        path = re.sub("/[^/]+$",'/planbox.yaml',os.path.realpath(__file__))
        self.config = self.__loadconfig__(path,'planbox')

    def __endpoint__(self,endpoint,*args,**kwargs):
        '''Handles a request to a supplied endpoint'''
        raise NotImplementedError, "Endpoint requests have not been implemented"

    def __getattr__(self,key):
        '''Allows access to individual endpoints'''
        if key in self.config.endpoints.keys():
            def wrapper(*args,**kwargs):
                return self.__endpoint__(key,*args,**kwargs)
            return wrapper
        else:
            raise AttributeError,"No attribute %s could be found for the Planbox API" % key

    def __loadconfig__(self,path,root):
        '''Loads a configuration file for the API'''
        data = open(path).read()
        data = re.sub('None\n','!!python/none\n',data)
        config = yaml.load(data)
        endpoints = {}
        cfgep = config[root]['endpoints']
        for endpoint in cfgep:
            endpoints[endpoint['name']] = endpoint
        config[root]['endpoints'] = endpoints
        return DotDict(config[root])
    

if __name__ == '__main__':

    api = PlanboxAPI()
    api.login()