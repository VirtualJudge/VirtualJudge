from json import JSONDecoder, JSONEncoder
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
            self._json = JSONDecoder().decode(self._text)
        except JSONDecodeError:
            self._json = None
        print(self._json)

    def _validate(self):
        try:
            if self._json is None:
                raise JsonValidationError("Parse Request Data Error")
            for name in dir(self):
                obj = self.__getattribute__(name)
                if isinstance(obj, BaseField):
                    if self._json.get(name):
                        obj.validate(JSONEncoder().encode(self._json[name]))
                    else:
                        raise JsonValidationError(name + ' field required, but not exist')
        except JsonValidationError as err:
            self._errors = str(err)

    def cleaned_data(self, name):
        return JSONEncoder().encode(self._json[name])

    def is_valid(self):
        self._validate()
        return self._errors is None

    @property
    def errors(self):
        return self._errors
