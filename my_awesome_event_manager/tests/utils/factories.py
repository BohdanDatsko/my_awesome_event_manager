import binascii
import json
import os
from datetime import datetime

import factory
from dj_rest_auth.models import TokenModel
from factory.django import DjangoModelFactory

from my_awesome_event_manager.tests.users.factories import UserFactory


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class TokenFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    created = factory.LazyFunction(datetime.now)
    key = binascii.hexlify(os.urandom(20)).decode()

    class Meta:
        model = TokenModel

    # ---------------------------------------------------------- #
    # ---------------------------------------------------------- #


class JSONFactory(factory.DictFactory):
    """
    Use with factory.Dict to make JSON strings.
    """

    @classmethod
    def _generate(cls, create, attrs):
        obj = super()._generate(create, attrs)
        return json.dumps(obj)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
