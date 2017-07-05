import os
import math

from zoopla import ZooplaQuery, ListingStatus, PropertyType

os.environ['ZOOPLA_API_KEY'] = os.environ['ZOOPLA_API_KEY'] or '[API_KEY_GOES_HERE]'

fields = ['listing_id', 'post_town', 'displayable_address', 'county',
          'num_bathrooms', 'num_bedrooms', 'num_floors',
          'num_recepts', 'status', 'price', 'property_type',
          'street_name', 'thumbnail_url', 'short_description',
          'details_url', 'last_published_date', 'latitude', 'longitude']

# COVENTRY AND 50mi RADIUS
filters = {
   'minimum_beds': 2,
   'radius': 50,
   'latitude': 52.407799,
   'longitude': -1.5119305,
   'listing_status': ListingStatus.sale,
   'minimum_price': 100000,
   'maximum_price': 300000,
   'page_size': 100,
   'page_number': 1
}

query_result = ZooplaQuery.select(fields, **filters)

listings = query_result['listings']
total_number_of_listings = int(query_result['result_count'])
total_number_of_pages = -(-total_number_of_listings // 100)
start_from_page = 2

# Fetch pages
for page_index in xrange(start_from_page, total_number_of_pages + 1):
    print 'fetching page [{0}/{1}]...'.format(page_index, total_number_of_pages)
    filters['page_number'] = page_index
    query_result = ZooplaQuery.select(fields, **filters)
    listings.extend(query_result['listings'])

## Write data to disk
with open('./properties.csv', 'w') as the_file:
    print 'saving data on disk...'
    headers_to_write = map(lambda i: '"{0}"'.format(i), fields)
    the_file.write(','.join(headers_to_write) + '\n')
    for listing in listings:
        listing_values = []
        for attribute in fields:
            value = '"{0}"'.format(listing[attribute]) if attribute in listing else '""'
            listing_values.append(value)
        the_file.write(','.join(listing_values) + '\n')
