"""Performs HTTP requests

   @author: purity
   @created: 21-aug-2015

"""
import logging
import json
import requests
from requests.auth import HTTPDigestAuth


class HTTP(object):
    """Performs HTTP requests.
    
    """
    
    def __init__(self, method, url, key, secret):
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.method = method
        self.url = url
        self.key = key
        self.secret = secret
        
        
    def perform_request(self, params):
        """Calls the specified 'url'.
           @param params: The request params as a dictionary
           @return:
              status_code: Status code in the response
              body: Body of the response. 
        
        """
        self.logger.info(
            "Performing request; URL: %s, Method: %s, Params: %s" %
            (self.url, self.method, params))
        status_code = None
        body = None
        
        try:
            response = requests.request(
            self.method, self.url, data=json.dumps(params),
                auth=HTTPDigestAuth(self.key, self.secret))
        
            status_code = response.status_code
            body = response.json() 
            
        except Exception:
            status_code = "REQUEST FAILED"
            
               
        return status_code, body
        
        