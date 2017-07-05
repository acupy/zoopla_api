# Zoopla Python API

```python
import os

from zoopla import ZooplaQuery, ListingStatus

os.environ['ZOOPLA_API_KEY'] = os.environ['ZOOPLA_API_KEY'] or '[API_KEY_GOES_HERE]'

fields = ['listing_id', 'post_town', 'displayable_address', 'county', 'num_bathrooms', 'num_bedrooms', 'num_floors',
          'num_recepts', 'status', 'price', 'property_type', 'street_name', 'thumbnail_url', 'short_description',
          'details_url', 'last_published_date', 'latitude', 'longitude']

filters = {
   'minimum_beds': 2,
   'area': 'Manchester',
   'listing_status': ListingStatus.sale,
   'minimum_price': 100000,
   'maximum_price': 300000
}

for prop in ZooplaQuery.select(fields, **filters)['listings']:
    print "\n"
    for f in prop:
        print f, prop[f]
```

[Click here to see a bit more complex example](https://github.com/acupy/zoopla_api/blob/master/test.py)

**Note that your API key has the following rate limits: 100 calls per second and 100 calls per hour**

[Zoopla API official documentation](http://developer.zoopla.com/docs)
