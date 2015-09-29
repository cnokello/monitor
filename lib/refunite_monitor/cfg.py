"""Manages configurations:
    Global and services configurations

   @author: purity
   @created: 21-aug-2015

"""
import ConfigParser


class Cfg(object):
    
    def __init__(self, app_cfg_file_path):
        # ## Load global application configuration
        self.app_cfg = ConfigParser.ConfigParser()
        
        try:
            self.app_cfg.read(app_cfg_file_path)
        except Exception:
            raise Exception("Error loading global configuration")
        
        # ## Load services configuration
        services_cfg_file_path = self.app_cfg.get("global", "services_file").strip()
        self.services_cfg = ConfigParser.ConfigParser()
        
        try:
            self.services_cfg.read(services_cfg_file_path)
        except Exception:
            raise Exception("Error loading services configuration")
        
    def get_app_cfg(self):
        return self.app_cfg
    
    def get_services_cfg(self):
        return self.services_cfg
    
    def get_module(self, name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
            
        return mod

    def get_class(self, class_fqn):
        comps = class_fqn.split(".")
                    
        class_name = comps[-1]
        module_name = class_fqn.rstrip(class_name).rstrip(".")
        
        module = self.get_module(module_name)
        _class = getattr(module, class_name)
        
        return _class
        