"""Configuration module."""
import configparser
import os


class MissingUserAuthFile(Exception):
    """Exception thrown when no user credentials file is found."""
    pass


class MissingAppAuthFile(Exception):
    """Exception thrown when no app credentials file is found."""
    pass


class Config(object):
    """Configuration handler object."""

    # Normal config file name.
    CONFIG_FILE = 'pleroline.cfg'
    # App-related tokens
    APP_CREDENTIALS = 'pleroline_app.cred'
    # User auth tokens and credentials. Keep secret!
    USER_CREDENTIALS = 'pleroline_user.cred'

    def __init__(self, base_dir):
        """Constructor.

        Args:
            home_dir: str, the base directory where the settings are located.
        """
        self.plero_dir = os.path.join(base_dir, '.pleroline')
        if not os.path.exists(self.plero_dir):
            os.mkdir(self.plero_dir)
        self.configs = {}

    def is_first_run(self):
        """Whether or not this is the first run."""
        return (
            not os.path.exists(os.path.join(self.plero_dir,
                                            self.CONFIG_FILE)))

    def save_config(self):
        """Saves the current config to file, replacing the old one if any."""
        config = configparser.ConfigParser()
        config['DEFAULT'] = self.configs
        with open(os.path.join(self.plero_dir, self.CONFIG_FILE), 'w') as cfg:
            config.write(cfg)

    def load_config(self):
        """Loads the configs from the given default file."""
        config = configparser.ConfigParser()
        config.read(os.path.join(self.plero_dir, self.CONFIG_FILE))
        self.configs = {}
        for key in config['DEFAULT']:
            self.configs[key] = config['DEFAULT'][key]

    def save_app_cred(self, app_id, secret):
        """Saves the app id and secret to the app credentials file.

        Args:
            app_id: str, the app's id returned by the mastodon api.
            secret: str, the app's secret returned bythe mastodon api."""
        config = configparser.ConfigParser()
        config['APP'] = {'id': app_id, 'secret': secret}
        with open(os.path.join(self.plero_dir, self.APP_CREDENTIALS),
                  'w') as app_cfg:
            config.write(app_cfg)

    def load_app_cred(self):
        """Loads the app id and secret from the app credentials file."""
        config = configparser.ConfigParser()
        config.read(os.path.join(self.plero_dir, self.APP_CREDENTIALS))
        try:
            app_id = config.get('APP', 'id')
            secret = config.get('APP', 'secret')
        except (configparser.NoSectionError, configparser.NoOptionError):
            raise MissingAppAuthFile()
        return (app_id, secret)

    def save_user_cred(self, token):
        """Saves the user's access token.

        Args:
            token: str, the user's OAuth access token.
        """
        config = configparser.ConfigParser()
        config['USER'] = {'token': token}
        with open(os.path.join(self.plero_dir, self.USER_CREDENTIALS),
                  'w') as user_cfg:
            config.write(user_cfg)

    def load_user_cred(self):
        """Loads the user's access token."""
        config = configparser.ConfigParser()
        config.read(os.path.join(self.plero_dir, self.USER_CREDENTIALS))
        try:
            token = config.get('USER', 'token')
        except (configparser.NoSectionError, configparser.NoOptionError):
            raise MissingUserAuthFile()
        return token
