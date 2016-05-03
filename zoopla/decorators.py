from zoopla import ZooplaError, supported_fields, supported_filters

def validate(f):
    def func_wrapper(cls, fields=None, number_of_items=10, **kwargs):
        """
        Validate the fields and the filters
        :param fields: list
        :param number_of_items: int
        :param kwargs: filters
        :return:
        """

        if 'area' not in kwargs and 'radius' not in kwargs:
            raise ZooplaError('The area or radius has to be specified in the fields.')

        invalid_fields = list(set(fields) - set(supported_fields))
        if invalid_fields:
            raise ZooplaError('Invalid fields: {0}'.format(', '.join(invalid_fields)))

        invalid_filters = list(set(kwargs.keys()) - set(supported_filters))
        if invalid_filters:
            raise ZooplaError('Invalid filters: {0}'.format(', '.join(invalid_filters)))

        return f(cls, fields=fields, number_of_items=number_of_items, **kwargs)

    return func_wrapper