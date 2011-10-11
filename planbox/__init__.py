from util import HTTPClient,DotDict
import os,re, yaml
from pprint import PrettyPrinter

class PlanboxAPI():

    def __init__(self):
        '''Initializes a fetcher and uses planbox.yaml to populate a listing of endpoints'''
        self.fetcher = HTTPClient()
        path = re.sub("/[^/]+$",'/planbox.yaml',os.path.realpath(__file__))
        self.config = self.__loadconfig__(path,'planbox')

    def __endpoint__(self,endpoint,*args,**kwargs):
        '''Handles a request to a supplied endpoint'''
        params = {}
        if not endpoint.params is None:
            for param,description in endpoint.params.iteritems():
                if not param in kwargs and not param.startswith('Optional'):
                    raise MissingParameterError,'Missing parameter "%s": %s' % (param,description)
                params[param] = kwargs[param]
        url = ''.join([self.config.uri,endpoint.path])
        headers,data = self.fetcher.do_POST(url,data=params)
        return data

    def __getattr__(self,key):
        '''Allows access to individual endpoints'''
        if key in self.config.endpoints.keys():
            def wrapper(*args,**kwargs):
                return self.__endpoint__(DotDict(self.config.endpoints[key]),*args,**kwargs)
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

    def help(self,endpoint=None):
        '''Basic info about the package/endpoints'''
        if not endpoint:
            print "Planbox API Methods"
            for key,endpoint in self.config.endpoints.iteritems():
                print '\t%s: %s'  % (key,endpoint['description'])
                if not endpoint['params'] is None: 
                    for param,description in endpoint['params'].iteritems():
                        print '\t\t%s: %s' % (param,description)
                else:
                    print "\t\tNo params"
        else:
            p = PrettyPrinter()
            p.pprint(self.config.endpoints[endpoint])

class MissingParameterError(Exception): pass

if __name__ == '__main__':

    api = PlanboxAPI()
    api.login(email='<email>',password='<password>')
    data = api.get_logged_resource()
    PrettyPrinter().pprint(data)
    api.logout()