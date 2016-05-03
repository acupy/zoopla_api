# Zoopla Python API

```python
import os

from zoopla.api import ZooplaQuery, ListingStatus

os.environ['ZOOPLA_API_KEY'] = '[API_KEY_GOES_HERE]'

fields = ['listing_id', 'num_bedrooms', 'price', 'property_type', 'street_name', 'short_description']

for prop in ZooplaQuery.select(fields, minimum_beds=2, area='Manchester', listing_status=ListingStatus.sale):
    for f in prop:
        print f, prop[f]
    print '\n'
```

[Zoopla API official documentation](http://developer.zoopla.com/docs)