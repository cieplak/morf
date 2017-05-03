====
morf
====

morf is a tool for transforming data in python


Illustrative Example
--------------------


.. code:: python

    from morf import Morphism


    nest_card = Morphism.compile(
        '/address_city            ->  /address/city',
        '/address_country         ->  /address/country',
        '/address_line1           ->  /address/line1',
        '/address_line2           ->  /address/line2',
        '/address_line1_check     ->  /address/checks/line1',
        '/address_state           ->  /address/state',
        '/address_zip             ->  /address/zip',
        '/address_zip_check       ->  /address/checks/zip',
        '/country                 ->  /address/country',
        '/brand                   ->  /brand',
        '/customer                ->  /customer',
        '/last4                   ->  /last_four',
        '/metadata                ->  /metadata',
        '/tokenization_method     ->  /metadata/tokenization_method',
        '/name                    ->  /holder_name',
        '/cvc_check               ->  cvc_bool                                  ->  /verified',
        '/exp_year -> /exp_month  ->  py::(lambda (x, y): "{}-{}".format(x, y)) ->  /expiration',

        ctx=dict(
            cvc_bool=(lambda x: x != "unchecked"),
        )
    )
    flat_card = {
        u'address_city': None,
        u'address_country': None,
        u'address_line1': None,
        u'address_line1_check': None,
        u'address_line2': None,
        u'address_state': None,
        u'address_zip': None,
        u'address_zip_check': None,
        u'brand': u'Visa',
        u'country': u'US',
        u'customer': None,
        u'cvc_check': u'unchecked',
        u'dynamic_last4': None,
        u'exp_month': 12,
        u'exp_year': 2016,
        u'funding': u'credit',
        u'id': u'card_16OzDH2eZvKYlo2C8Y1jwLRn',
        u'last4': u'4242',
        u'metadata': {},
        u'name': 'William III',
        u'object': u'card',
        u'tokenization_method': None
    }
    nested_card = {
        'address': {
            'checks': {
                'line1': None,
                'zip': None
            },
            'city': None,
            'country': u'US',
            'line1': None,
            'line2': None,
            'state': None,
            'zip': None
        },
        'brand': u'Visa',
        'customer': None,
        'expiration': '2016-12',
        'holder_name': 'William III',
        'last_four': '4242',
        'metadata': {'tokenization_method': None},
        'verified': False,
    }
    assert nest_card(flat_card) == nested_card



.. code:: python

    from morf import Morphism


    flatten_msg = Morphism.compile(
        '/headers  ->  /',
        '/body     ->  /body',
    )
    message = dict(
        headers=dict(
            sender='2PvSNshPmKvAuw2tcjY6C',
            receiver='t71mVtgKqWtUSj4k3fwQtK',
            salt='efVCYqSPeL7qxRm7MDB3jL',
            mac='diHN0NNRv452Y+ZbUv4ejJxo7nassw0npznOccjfWtA=',
        ),
        body='MXHgDEw2CwFNoj0akdmCIzM4TV6hXJwg+Zjlcz3yEMg=\n',
    )
    flat_message = dict(
        sender='2PvSNshPmKvAuw2tcjY6C',
        receiver='t71mVtgKqWtUSj4k3fwQtK',
        salt='efVCYqSPeL7qxRm7MDB3jL',
        mac='diHN0NNRv452Y+ZbUv4ejJxo7nassw0npznOccjfWtA=',
        body='MXHgDEw2CwFNoj0akdmCIzM4TV6hXJwg+Zjlcz3yEMg=\n',
    )
    assert flatten_msg(message) == flat_message



Development
-----------

.. code:: bash

    cd morf/
    python setup.py develop
    python setup.py test
