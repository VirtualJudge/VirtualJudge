import json
from json import JSONDecodeError


class JsonValidationError(Exception):
    def __init__(self, err="Json Validate Error"):
        Exception.__init__(self, err)


class BaseField(object):
    def validate(self, value):
        return True


class Body(object):
    def __init__(self, value):
        if not isinstance(value, bytes):
            raise ValueError("Expect type 'bytes', but got '" + str(type(value)) + "'")
        self._errors = None
        self._text = bytes.decode(value)
        try:
            print(self._text)
            self._json = json.loads(self._text)
        except JSONDecodeError:
            self._json = None

    def _validate(self):
        try:
            if self._json is None:
                raise JsonValidationError("Parse Request Data Error")
            for name in dir(self):
                obj = self.__getattribute__(name)
                if isinstance(obj, BaseField):
                    if self._json.get(name):
                        obj.validate(str(self._json[name]))
                    else:
                        raise JsonValidationError(name + ' field not exist')
        except JsonValidationError as err:
            self._errors = str(err)

    @property
    def cleaned_data(self):
        return self._json

    def is_valid(self):
        self._validate()
        return self._errors is None

    @property
    def errors(self):
        return self._errors
