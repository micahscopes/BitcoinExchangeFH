from befh.instrument import Instrument
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

class SubscriptionManager:
    def __init__(self, config_path):
        """
        Constructor
        """
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_path)
        
    def get_instmt_ids(self):
        """
        Return all the instrument ids
        """
        return self.config.sections()
    
    def get_instrument(self, instmt_id):
        """
        Return the instrument object by instrument id
        :param instmt_id: Instrument ID
        :return Instrument object
        """
        exchange_name = self.config.get(instmt_id, 'exchange')
        instmt_name = self.config.get(instmt_id, 'instmt_name')
        instmt_code = self.config.get(instmt_id, 'instmt_code')
        enabled = int(self.config.get(instmt_id, 'enabled'))
        depth = 5
        try:
            depth = int(self.config.get(instmt_id, 'depth'))
        except:
            pass

        poll_interval = 5
        try:
            poll_interval = int(self.config.get(instmt_id, 'poll_interval'))
        except:
            pass
        params = dict(self.config.items(instmt_id))
        del params['exchange']
        del params['instmt_name']
        del params['instmt_code']
        del params['enabled']
        
        try:
            del params['depth']
        except:
            pass
        
        try:
            del params['poll_interval']
        except:
            pass
        if enabled == 1:
            return Instrument(exchange_name, instmt_name, instmt_code, depth, poll_interval, **params)
        else:
            return None
        
    def get_subscriptions(self):
        """
        Get all the subscriptions from the configuration file
        :return List of instrument objects
        """
        instmts = [self.get_instrument(inst) for inst in self.get_instmt_ids()]
        return [instmt for instmt in instmts if instmt is not None]
        
