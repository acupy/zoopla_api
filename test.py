import os

from zooplapi import ZooplaQuery

os.environ['ZOOPLA_API_KEY'] = '[API_KEY_GOES_HERE]'

fields = ['listing_id', 'post_town', 'displayable_address', 'county', 'num_bathrooms', 'num_bedrooms', 'num_floors',
          'num_recepts', 'status', 'price', 'property_type', 'street_name', 'thumbnail_url', 'short_description',
          'details_url', 'last_published_date', 'latitude', 'longitude']

filters = {
    'minimum_beds': 2,
    'area': 'Manchester',
    'listing_status':'sale',
    'minimum_price': 100000,
    'maximum_price': 300000
}

for prop in ZooplaQuery.select(fields, filters):
    print "\n"
    for f in prop:
        print f, prop[f]