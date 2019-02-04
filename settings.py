import os

# TODO: DO SMTHNG
MONGO_URI = 'mongodb+srv://cloth:cloth@main-t0esf.mongodb.net/cloth'

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

RENDERERS = [
    'eve.render.JSONRenderer',
]

DOMAIN = {
    'stores': {
        'schema': {
            'name': {'type': 'string', 'required': True, 'unique': True, },
            'url': {'type': 'string', 'required': True, 'unique': True, },
        },
    },
    'items': {
        'schema': {
            'store': {'type': 'objectid', 'data_relation': {'resource': 'stores', 'field': '_id', 'embeddable': True}},
            'name': {'type': 'string', 'required': True, },
            'category': {'type': 'string', },
            'url': {'type': 'string', 'required': True, },
            'images': {'type': 'list', 'required': True, },
            'baseprice': {'type': 'float', 'required': True, },
            'salesprice': {'type': 'float', 'required': True, },
            'sex': {'type': 'string', 'minlength': 1, 'maxlength': 1, 'required': True, },
            'extra_info': {'type': 'dict'},
        },
    },
}
