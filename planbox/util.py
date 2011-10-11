import cookielib, urllib, urllib2, urlparse, json

class HTTPClient():
    '''HTTP Client library, allows the four REST methods and uses a cookie handler'''

    __methods__ = 'GET','POST','PUT','DELETE'

    def __init__(self):
        '''Generates a new local cookie jar and url opener'''
        self.cookies = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies),urllib2.HTTPHandler)

    def __getattr__(self,key):
        '''Allows for calling of any HTTP method in __methods__ as client.METHOD or client.do_METHOD'''

        key = key[3:] if key.startswith('do_') else key

        if key in self.__methods__ or key in map(lambda m: 'do_%s' % m, self.__methods__):
            def request(*args,**kwargs):
                return self.__request__(key,*args,**kwargs)
            return request

    def __request__(self,method,url,params=None,data=None,contenttype='text/plain',timeout=30):
        '''Perform a http request with the supplied method returns a tuple of headers,response'''
        # Parse and append supplied params to the url
        if params and type(params) is dict: 
            # Retrieve params already in the url
            resource = urlparse.urlparse(url)
            # Use a generator to convert these to url-friendly data
            urlparams = dict((key,','.join(value)) for key,value in urlparse.parse_qs(resource.query).iteritems())
            # Update these with the supplied params (assume supplied params are more significant)
            urlparams.update(params)
            # Generate the url
            url = "http://%s?%s" % (resource.netloc,urllib.urlencode(urlparams))

        # Check the type of data being provided
        if type(data) is dict:
            if contenttype is 'application/json':
                # Assume a dictionary needs to be cast to JSON, and set the content type
                data = json.dumps(data)
            else:
                data = urllib.urlencode(data)
                contenttype = 'application/x-www-form-urlencoded'

        # Formulate a request object
        request = urllib2.Request(url, data=data)
        # Add headers and method
        request.add_header('Content-Type', contenttype)
        request.get_method = lambda: method
        # Open with the requested timeout
        response = self.opener.open(request,timeout=timeout)

        info = response.info()
        data = response.read()
        
        # Attempt to load JSON
        try:    data = json.loads(data)
        except: pass

        # Return response headers and body
        return info,data


class DotDict(dict):
    '''Dict subclass to allow dot access to dictionary items'''
    __getattr__= dict.__getitem__
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__    


if __name__ == '__main__':

    client = HTTPClient()

    client.do_GET("http://www.tryllo.com?key=something&butt=face",{'key': 'value'})
