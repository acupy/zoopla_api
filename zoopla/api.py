import urllib2
import lxml.etree
import os

from zoopla import validate, ZooplaError


URL = "http://api.zoopla.co.uk/api/v1/property_listings"


class ListingStatus(object):
    sale = 'sale'
    rent = 'rent'


class ZooplaQuery(object):

    @classmethod
    @validate
    def select(cls, fields=None, number_of_items=10, **kwargs):
        """
        Return the requested properties
        :param fields: list of fields as a string
        :param filters: dict, key: field, value: the value
        :return: list of properties
        """

        if not fields:
            fields = ['listing_id']

        kwargs['api_key'] = ZooplaQuery.__get_api_key()
        kwargs['page_size'] = number_of_items if number_of_items < 100 else 100
        the_request_url = ZooplaQuery.__get_request(kwargs)

        return ZooplaQuery.__get_result(the_request_url, fields)

    @staticmethod
    def __get_result(the_request_url, fields):
        """
        Return the data as json
        :param the_request_url: the url with filters
        :param fields: the attributes to return
        :return: list of dicts
        """
        try:
            request = urllib2.Request(the_request_url, headers={"Accept": "application/xml"})
            response = urllib2.urlopen(request)
            tree = lxml.etree.fromstring(response.read())
        except urllib2.HTTPError as ex:
            raise ZooplaError('The API has not been set. Set the following environ variable: ZOOPLA_API_KEY')
        items = []
        for listing in tree.iter('listing'):
            listing_item = {}
            for p in listing:
                if p.tag in fields:
                    if p.tag in ['listing_id', 'num_bathrooms', 'num_bedrooms', 'num_floors', 'num_recepts', 'price']:
                        listing_item[p.tag] = int(p.text) if p.text else 0
                    elif p.tag in ['last_published_date']:
                        listing_item[p.tag] = p.text[:10]
                    elif p.tag in ['latitude', 'longitude']:
                        listing_item[p.tag] = float(p.text)
                    else:
                        listing_item[p.tag] = p.text
            if 'latitude' in listing_item and 'longitude' in listing_item:
                listing_item['location'] = '{0}, {1}'.format(listing_item['latitude'], listing_item['longitude'])
            items.append(listing_item)
        return items

    @staticmethod
    def __get_api_key():
        """
        Return the API key from the environment
        :return: string
        """

        if 'ZOOPLA_API_KEY' in os.environ:
            return os.environ['ZOOPLA_API_KEY']
        else:
            raise ZooplaError('The API has not been set. Set the following environ variable: ZOOPLA_API_KEY')

    @staticmethod
    def __get_request(filters):
        """
        Return the request url with filters
        :param filters: dict of filters
        :return: string
        """

        filters = ['{0}={1}'.format(the_key, the_value) for the_key, the_value in filters.items()]
        return '{url}?{filters}&summarised=yes'.format(url=URL, filters='&'.join(filters))


