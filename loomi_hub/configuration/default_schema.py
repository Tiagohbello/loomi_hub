from collections import OrderedDict

from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import no_body


class Response:
    def get_fields(self):
        new_fields = OrderedDict()
        for fieldName, field in super().get_fields().items():
            if not field.write_only:
                new_fields[fieldName] = field
        return new_fields


class Request:
    def get_fields(self):
        new_fields = OrderedDict()
        for fieldName, field in super().get_fields().items():
            if not field.read_only:
                new_fields[fieldName] = field
        return new_fields


class BlankMeta:
    pass


class ReadWriteAutoSchema(SwaggerAutoSchema):
    def get_view_serializer(self):
        return self._convert_serializer(Request)

    def get_default_response_serializer(self):
        body_override = self._get_request_body_override()
        if body_override and body_override is not no_body:
            return body_override

        return self._convert_serializer(Response)

    def _convert_serializer(self, new_class):
        serializer = super().get_view_serializer()

        if not serializer:
            return serializer

        class CustomSerializer(new_class, serializer.__class__):
            class Meta(getattr(serializer.__class__, 'Meta', BlankMeta)):
                ref_name = new_class.__name__ + serializer.__class__.__name__

            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                for fieldName, field in dict(self.fields).copy().items():
                    if fieldName not in dict(self.get_fields()):
                        self.fields.pop(fieldName)

        new_serializer = CustomSerializer(data=serializer.data)
        return new_serializer
