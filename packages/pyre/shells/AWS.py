# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import pyre
import collections
import configparser

# boto3 is useful, but not universally available
try:
    # get it
    import boto3
# if something goes wrong
except ImportError:
    # mark it as unavailable
    boto3 = None


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
        self._profiles = self._loadProfiles()
        # all done
        return

    # implementation details
    def _loadProfiles(self) -> dict:
        """
        Load the AWS credentials
        """
        # prime
        profiles = collections.defaultdict(dict)
        # locate the file with the shared credentials
        path = pyre.primitives.path(
            os.getenv("AWS_SHARED_CREDENTIALS_FILE", "~/.aws/credentials")
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
                profiles[section.lower()] = profile

        # now, look for individual values from the environment
        # first up, the default region
        key = os.getenv("AWS_DEFAULT_REGION", None)
        # if it's there
        if key is not None:
            # set the value
            profiles["default"]["region"] = key
        # it is overridden by an explicit setting of the region
        key = os.getenv("AWS_REGION", None)
        # if it's there
        if key is not None:
            # set the value
            profiles["default"]["region"] = key
        # next, check whether there an access key in the user environment
        key = os.getenv("AWS_ACCESS_KEY_ID", None)
        # if it's there
        if key is not None:
            # override the value in the default profile
            profiles["default"]["aws_access_key_id"] = key
        # next, whether there is a secret key in the environment
        key = os.getenv("AWS_SECRET_ACCESS_KEY", None)
        # if there
        if key is not None:
            # override the value in the default profile
            profiles["default"]["aws_secret_access_key"] = key
        # and finally whether there is a session token in the environment
        key = os.getenv("AWS_SESSION_TOKEN", None)
        # if there
        if key is not None:
            # override the value in the default profile
            profiles["default"]["aws_session_token"] = key

        # another source of credentials for the default profile is a token from a web identity
        # provider; to get that we need boto3
        if boto3:
            # get the role arn
            arn = os.getenv("AWS_ROLE_ARN")
            # initialize the token
            token = ""
            # and the path to the web token
            link = os.getenv("AWS_WEB_IDENTITY_TOKEN_FILE")
            # if it exists
            if link:
                # open it
                with open(link, mode="r") as stream:
                    # and extract the token
                    token = stream.read()
            # if we have both an arn and a token
            if arn and token:
                # talk to STS
                sts = boto3.client(service_name="sts")
                # assume the role
                role = sts.assume_role_with_web_identity(
                    RoleArn=arn, RoleSessionName="assume-role", WebIdentityToken=token
                )
                # extract the credentials
                auth = role["Credentials"]
                # and from there the signing parameters
                aws_access_key_id = auth["AccessKeyId"]
                aws_secret_access_key = auth["SecretAccessKey"]
                aws_session_token = auth["SessionToken"]
                # store them in the default profile
                profiles["default"]["aws_access_key_id"] = aws_access_key_id
                profiles["default"]["aws_secret_access_key"] = aws_secret_access_key
                profiles["default"]["aws_session_token"] = aws_session_token

        # NYI: there may be profile configurations in ~/.aws.config

        # all done
        return profiles


# end of file
