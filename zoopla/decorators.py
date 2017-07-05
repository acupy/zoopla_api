from zoopla import ZooplaError
from config import supported_fields, supported_filters

def validate(f):
    def func_wrapper(cls, fields=None, **kwargs):
        """
        Validate the fields and the filters
        :param fields: list
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

        return f(cls, fields=fields, **kwargs)

    return func_wrapper
