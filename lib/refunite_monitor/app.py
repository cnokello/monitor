"""Assembles and starts the application

   @author: purity
   @created: 21-aug-2015

"""
import logging
import logging.config
from refunite_monitor.cfg import Cfg
from refunite_monitor.services_processor import Processor


class App(object):
    
    def __init__(self, cfg_file_path):
        self.cfg = Cfg(cfg_file_path)
        
        # ## Logging configuration and setup
        try:
            logging.config.fileConfig(
                self.cfg.get_app_cfg().get("logging", "cfg_file").strip())
        except Exception:
            raise Exception(
                "Error loading logging configuration. Please confirm that \
                logging configuration is correct")
            
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.logger.info("Starting application...")
        
        Processor(self.cfg).run()