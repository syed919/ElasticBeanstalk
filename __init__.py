from boto.regioninfo import RegionInfo, get_regions
from boto.regioninfo import connect


def regions():
    """
    Get all available regions for the AWS Elastic Beanstalk service.
    :rtype: list
    :return: A list of :class:`boto.regioninfo.RegionInfo`
    """
    from boto.beanstalk.layer1 import Layer1
    return get_regions(
        'elasticbeanstalk',
        connection_cls=Layer1
    )


def connect_to_region(region_name, **kw_params):
    from boto.beanstalk.layer1 import Layer1
    return connect('elasticbeanstalk', region_name, connection_cls=Layer1,
                   **kw_params)
