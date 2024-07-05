from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
from rest_framework import serializers

# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class CustomRelatedField(serializers.RelatedField):
    """
    A read-write field that represents the target of the relationship
    by a unique 'to_field' attribute.
    """

    default_error_messages = {
        "does_not_exist": "Object with {to_field}={value} does not exist.",
        "invalid": "Invalid value.",
    }

    def __init__(self, to_field=None, display_fields=None, **kwargs):
        assert to_field is not None, "The `to_field` argument is required."
        self.to_field = to_field
        self.display_fields = display_fields
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.to_field: data})
        except ObjectDoesNotExist:
            self.fail("does_not_exist", to_field=self.to_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail("invalid")

    def to_representation(self, obj):
        if self.display_fields:
            res_obj = {}
            for field in self.display_fields:
                res_obj[field] = getattr(obj, field)
            return res_obj
        return getattr(obj, self.to_field)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
