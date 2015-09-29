"""Process requests

   @author: purity
   @created: 21-aug-2015

"""
import logging
from tabulate import tabulate
    

class Service(object):
    """Manages services to be tested
    
    """
    
    def __init__(self, protocol, test_data, expected_result=None, test=True):
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        
        self.protocol = protocol
        self.url = self.protocol.url
        self.method = self.protocol.method
        self.test_data = test_data
        self.expected_result = expected_result
        self.test = test
        
        # self.logger.debug(
        #    "Service: Method = %s, URL = %s, Test Data = %s, Expected Result = %s" % 
        #    (self.method, self.url, self.test_data.replace("\n", ", "), self.expected_result))

    def get_request_params(self, test_data):
        self.logger.debug("Raw test data: %s" % test_data)
        test_datas = test_data.split("\n")
        
        params = {}
        for data in test_datas:
            datas = data.strip().split("=")
            if len(datas) == 2:
                params[datas[0].strip()] = datas[1].strip()
            
        return params
    
    def run(self):
        params = None
        if self.test:
            params = self.get_request_params(self.test_data)
        else:
            params = self.test_data
            
        return self.protocol.perform_request(params)



class Processor(object):
    """Manages communication with endpoints of
      services to be tested
    
    """
    
    def __init__(self, cfg):
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.protocol_class = cfg.get_class(
            cfg.get_app_cfg().get("global", "protocol_class").strip())
        self.etl_url = cfg.get_app_cfg().get("global", "etl_url").strip()
        self.key = cfg.get_app_cfg().get("global", "protocol_key").strip()
        self.secret = cfg.get_app_cfg().get("global", "protocol_secret").strip()
        self.services_cfg = cfg.get_services_cfg()
        self.service_names = self.services_cfg.sections()
        
    def run(self):
        self.logger.info("Running service tests...")
        test_results = []
        for service_name in self.service_names:
            method = self.services_cfg.get(service_name, "method")
            endpoint = self.services_cfg.get(service_name, "endpoint")
            test_data = self.services_cfg.get(service_name, "test_data")
            expected_result = self.services_cfg.get(service_name, "expected_result")
            url = endpoint
            
            status_code, body = Service(
                self.protocol_class(method, url, self.key, self.secret),
                test_data, expected_result).run()
                
            self.logger.debug(
                "RESPONSE; Status Code: %s, Response Body: %s" % (status_code, body))
            
            # ## Now, submit to the ETL engine for processing 
            params = {"status_code": status_code, "body": body}
            Service(self.protocol_class("POST", self.etl_url, self.key, self.secret), 
                    params, 200,False).run()
                    
            # ## Append result to the result dictionary
            test_results.append((service_name.upper(), url, method.upper(), status_code))
            
        # ## Print out test results
        print "\n\n\n"
        print tabulate(test_results, headers=["SERVICE", "URL", "METHOD", "STATUS CODE"], tablefmt="orgtbl")
        print "\n\n\n"
            
        
