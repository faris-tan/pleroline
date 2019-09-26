"""Module to handle mastodon authentication."""
import mastodon

class Auth():
    """Object used to handle all auth-related API calls.

    This class is intentionally left as dumb and simple as possible, because
    security and authentication are icky.
    """

    def __init__(self, instance):
        if not instance.startswith('https://'):
            if instance.startswith('http://'):
                instance = instance.replace('http://', 'https://', 1)
            else:
                instance = 'https://' + instance
        self.instance = instance
        self.scopes = ['read', 'write', 'follow']

    def get_app_credentials(self):
        """Queries the instance to create a new app and obtain its creds.

        Returns:
            A tuple of strings (id, secret).
        """
        return mastodon.Mastodon.create_app('pleroline',
                                            scopes=self.scopes,
                                            api_base_url=self.instance)

    def log_in_user(self, email, password, app_creds):
        """Log in a user to the instance.

        Args:
            email: str, the user's registration email.
            password: str, the user's password.
            app_creds: (str, str), the pair of id + secret assigned to the app.

        Returns:
            str, the user's secret OAuth token.
        """
        (app_id, secret) = app_creds
        api = mastodon.Mastodon(app_id, secret, api_base_url=self.instance)
        return api.log_in(email, password, scopes=self.scopes)

    def get_api_client(self, user_token, app_creds):
        """Obtain the final pleroma/mastodon API client.

        Args:
            user_token: str, the user's OAuth access token.
            app_creds: (str, str), the pair of id + secret assigned to the app.

        Returns:
            A properly authenticated Mastodon Object.
        """
        (app_id, secret) = app_creds
        return mastodon.Mastodon(app_id,
                                 secret,
                                 user_token,
                                 api_base_url=self.instance)
