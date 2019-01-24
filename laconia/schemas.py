from marshmallow import Schema, fields, validate


class RedisConfigSchema(Schema):
    """
    Schema for redis-related config section.
    """

    host = fields.String(required=True)
    port = fields.Int(
        missing=6379, validate=validate.Range(min=1024, max=65535)  # noqa: Z432
    )


class ConfigSchema(Schema):
    """
    Schema for config validation and deserialization.
    """

    redis = fields.Nested(RedisConfigSchema, required=True)

    key_length = fields.Int(required=True)

    host = fields.String(required=True)
    port = fields.Integer(
        required=True, validate=validate.Range(min=1024, max=65535)  # noqa: Z432
    )
    enable_https = fields.Boolean(missing=False)


class CreateLinkSchema(Schema):
    """
    Schema to validate a link creation request data.
    """

    link = fields.Url(required=True)
