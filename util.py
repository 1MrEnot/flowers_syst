USER_ID_COOKIE = 'user_id'


def dataclass_dict_factory(data):
    return dict(x for x in data if x[1] is not None)
