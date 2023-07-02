# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# externals
import os
import pyre
import collections
import configparser


# declaration
class AWS(pyre.component):
    """
    Access to the user's AWS credentials
    """

    # interface
    def credentials(self, profile: str = "default"):
        """
        Get the pair of access keys from the named {profile}
        """
        # get my profiles
        profiles = self._profiles
        # get the id
        id = profiles[profile].get("aws_access_key_id", "")
        # the secret
        secret = profiles[profile].get("aws_secret_access_key", "")
        # and the session token
        token = profiles[profile].get("aws_session_token", "")
        # pass them on
        return id, secret, token

    def profile(self, name: str = "default"):
        """
        Access the contents of the named profile
        """
        # look up the profile
        profile = self._profiles[name]
        # and hand it off
        return profile

    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the cache for aws credentials
        self._profiles = self._loadCredentials()
        # all done
        return

    # implementation details
    def _loadCredentials(self) -> dict:
        """
        Load the AWS credentials
        """
        # prime
        credentials = collections.defaultdict(dict)
        # locate the file with the shared credentials
        path = pyre.primitives.path(
            os.environ.get("AWS_SHARED_CREDENTIALS_FILE", "~/.aws/credentials")
        )
        # if it's there
        if path.exists():
            # make an {ini} parser
            cfg = configparser.ConfigParser()
            # and parse the file
            cfg.read(path)
            # go through the sections
            for section, keys in cfg.items():
                # prime the profile
                profile = {}
                # go through the keys
                for key in keys:
                    # extract the value
                    value = cfg.get(section=section, option=key)
                    # and set it
                    profile[key.lower()] = value
                # attach the profile to the pile
                credentials[section.lower()] = profile
        # check whether there an access key in the user environment
        key = os.environ.get("AWS_ACCESS_KEY_ID", None)
        # if it's there
        if key is not None:
            # override the value in the default profile
            credentials["default"]["aws_access_key_id"] = key
        # check whether there is a secret key in the environment
        key = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
        # if there
        if key is not None:
            # override the value in the default profile
            credentials["default"]["aws_secret_access_key"] = key
        # check whether there is a session token in the environment
        key = os.environ.get("AWS_SESSION_TOKEN", None)
        # if there
        if key is not None:
            # override the value in the default profile
            credentials["default"]["aws_session_token"] = key

        # NYI: there may be profile configurations in ~/.aws.config

        # all done
        return credentials


# end of file
