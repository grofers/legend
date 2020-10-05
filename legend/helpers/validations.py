from cerberus import Validator


def validate_input(schema, input_file):
    v = Validator()
    v.schema = schema
    if not v.validate(input_file):
        raise Exception("Error in input file: ", v.errors)
    return v.document
