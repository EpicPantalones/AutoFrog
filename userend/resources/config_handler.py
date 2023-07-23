import configparser

class ConfigHandler:
    def __init__(self, config_file='settings.conf'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self._load_config()

    def _load_config(self):
        self.config.read(self.config_file)

    def get_param(self, param_name, default_value):
        try:
            return self.config.getint('Settings', param_name)
        except (configparser.NoOptionError, configparser.NoSectionError, ValueError):
            try:
                return self.config.getfloat('Settings', param_name)
            except (configparser.NoOptionError, configparser.NoSectionError, ValueError):
                try:
                    return self.config.getboolean('Settings', param_name)
                except (configparser.NoOptionError, configparser.NoSectionError, ValueError):
                    self.set_param(param_name, default_value)
                    return default_value

    def set_param(self, param_name, value):
        if not self.config.has_section('Settings'):
            self.config.add_section('Settings')
        self.config.set('Settings', param_name, str(value))

    def save_config(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
