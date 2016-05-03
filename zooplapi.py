import urllib2
import lxml.etree
import os

URL = "http://api.zoopla.co.uk/api/v1/property_listings"

class ZooplaError(Exception):
    pass


class ZooplaQuery(object):
    supported_fields = ['listing_id', 'outcode', 'post_town', 'displayable_address', 'county',
                        'country', 'num_bathrooms', 'num_bedrooms', 'num_floors', 'num_recepts',
                        'listing_status', 'status', 'price', 'price_modifier', 'price_change',
                        'property_type', 'street_name', 'thumbnail_url', 'image_url', 'image_caption',
                        'floor_plan', 'description', 'short_description', 'details_url', 'new_home',
                        'latitude', 'longitude', 'first_published_date', 'last_published_date',
                        'agent_name', 'agent_logo', 'agent_phone']

    supported_filters = ['radius', 'area', 'order_by', 'ordering', 'listing_status', 'include_sold',
                         'include_rented', 'minimum_price', 'maximum_price', 'minimum_beds',
                         'maximum_beds', 'furnished', 'property_type', 'new_homes', 'chain_free',
                         'keywords', 'listing_id', 'branch_id', 'page_number', 'page_size', 'summarised']
    @classmethod
    def select(cls, fields, filters, number_of_items=10):
        """
        Return the requested properties
        :param fields: list of fields as a string
        :param filters: dict, key: field, value: the value
        :return: list of properties
        """
        ZooplaQuery.__validate(fields, filters)

        filters['api_key'] = ZooplaQuery.__get_api_key()
        filters['page_size'] = number_of_items if number_of_items < 100 else 100
        the_request_url = ZooplaQuery.__get_request(filters)

        return ZooplaQuery.__get_result(the_request_url, fields)

    @staticmethod
    def __get_result(the_request_url, fields):
        request = urllib2.Request(the_request_url, headers={"Accept": "application/xml"})
        response = urllib2.urlopen(request)
        tree = lxml.etree.fromstring(response.read())
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

        if 'ZOOPLA_API_KEY' in os.environ:
            return os.environ['ZOOPLA_API_KEY']
        else:
            raise ZooplaError('The API has not been set. Set the following environ variable: ZOOPLA_API_KEY')

    @staticmethod
    def __get_request(filters):
        filters = ['{0}={1}'.format(the_key, the_value) for the_key, the_value in filters.items()]
        return '{url}?{filters}&summarised=yes'.format(url=URL, filters='&'.join(filters))

    @classmethod
    def __validate(cls, fields, filters):
        if 'area' not in filters and 'radius' not in filters:
            raise ZooplaError('The area or radius has to be specified in the fields.')

        invalid_fields = list(set(fields) - set(cls.supported_fields))
        if invalid_fields:
            raise ZooplaError('Invalid fields: {0}'.format(', '.join(invalid_fields)))

        invalid_filters = list(set(filters.keys()) - set(cls.supported_filters))
        if invalid_filters:
            raise ZooplaError('Invalid filters: {0}'.format(', '.join(invalid_filters)))

