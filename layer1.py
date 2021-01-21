import boto
import boto.jsonresponse
from boto.compat import json
from boto.regioninfo import RegionInfo
from boto.connection import AWSQueryConnection


class Layer1(AWSQueryConnection):

    APIVersion = '2010-12-01'
    DefaultRegionName = 'us-east-1'
    DefaultRegionEndpoint = 'elasticbeanstalk.us-east-1.amazonaws.com'

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None,
                 is_secure=True, port=None,
                 proxy=None, proxy_port=None,
                 proxy_user=None, proxy_pass=None, debug=0,
                 https_connection_factory=None, region=None, path='/',
                 api_version=None, security_token=None, profile_name=None):
        if not region:
            region = RegionInfo(self, self.DefaultRegionName,
                                self.DefaultRegionEndpoint)
        self.region = region
        super(Layer1, self).__init__(aws_access_key_id,
                                    aws_secret_access_key,
                                    is_secure, port, proxy, proxy_port,
                                    proxy_user, proxy_pass,
                                    self.region.endpoint, debug,
                                    https_connection_factory, path,
                                    security_token, profile_name=profile_name)

    def _required_auth_capability(self):
        return ['hmac-v4']

    def _encode_bool(self, v):
        v = bool(v)
        return {True: "true", False: "false"}[v]

    def _get_response(self, action, params, path='/', verb='GET'):
        params['ContentType'] = 'JSON'
        response = self.make_request(action, params, path, verb)
        body = response.read().decode('utf-8')
        boto.log.debug(body)
        if response.status == 200:
            return json.loads(body)
        else:
            raise self.ResponseError(response.status, response.reason, body)

    def check_dns_availability(self, cname_prefix):
        """Checks if the specified CNAME is available.
        :type cname_prefix: string
        :param cname_prefix: The prefix used when this CNAME is
            reserved.
        """
        params = {'CNAMEPrefix': cname_prefix}
        return self._get_response('CheckDNSAvailability', params)
