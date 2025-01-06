from marshmallow import Schema, fields, ValidationError, validates_schema
from marshmallow.validate import Length

class UserSchema(Schema):
    nome = fields.Str(required=True, validate=Length(max=255))
    cognome = fields.Str(required=True, validate=Length(max=255))
    email = fields.Email(required=True, validate=Length(max=255))
    password = fields.Str(required=True, validate=Length(min=6, max=12))
    confermaPassword = fields.Str(required=True)

    # Validazione a livello di schema
    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data.get("password") != data.get("confermaPassword"):
            raise ValidationError("Le password non corrispondono.", field_name="message")

user_schema = UserSchema()