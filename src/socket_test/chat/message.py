# coding=utf-8
from ast import literal_eval

COMMAND_MSG_TYPE = 'Cmd'
MESSAGE_MSG_TYPE = 'Msg'


class Message(object):
    """
    The standard message exchange type for the simple chat server.
    """
    REQUIRED_FIELDS = {'Sender': int, 'Receivers': list, 'Type': str, 'Message': str}
    __fields = {}

    def __init__(self, fields):
        # type: (dict) -> None
        '''
        Args:
            fields:
            The fields of this message, the fields in Message.REQUIRED_FIELDS must be given in the correct type.
            
        To create a new message:
        >>> msg = Message({'Sender': 0, 'Receivers': [1,2,3], 'Type':MESSAGE_MSG_TYPE, 'Message': 'Hello', 'Custom_Fields': 'value'})
        To convert a string to a message:
        >>> s = "{'Sender': 0, 'Receivers': [1,2,3], 'Type':MESSAGE_MSG_TYPE, 'Message': 'Hello'}"
        >>> Message.parse_str(s)
        To get a text representation of a message for socket IO:
        >>> msg = Message({'Sender': 0, 'Receivers': [1,2,3], 'Type':MESSAGE_MSG_TYPE, 'Message': 'Hello'})
        >>> s = repr(msg)
        '''
        # Check required fields
        for field_name in Message.REQUIRED_FIELDS.keys():
            field = fields.get(field_name)
            if field is None:
                raise Message._Message_Argument_Error('\nRequired field not given:\n\'%s\':%s.'
                                                      % (field_name, str(
                    Message.REQUIRED_FIELDS.get(field_name))))
            else:
                if not isinstance(fields.get(field_name), Message.REQUIRED_FIELDS.get(field_name)):
                    raise Message._Message_Argument_Error(
                        '\nInappropriate field data type.\nType of field \'%s\' should be %s, but %s is given.' % (
                            field_name, Message.REQUIRED_FIELDS.get(field_name), str(type(
                                fields.get(field_name)))))
        self.__fields = fields

    def get_field(self, field_name, default=None):
        # type: (str, object) -> object
        # If the required field does not exist, return default.
        return self.__fields.get(field_name, default)

    def set_field(self, field_name, value):
        # type: (str, object) -> None
        # Check required fields
        if field_name in Message.REQUIRED_FIELDS.keys():
            if not isinstance(value, Message.REQUIRED_FIELDS.get(field_name)):
                raise Message._Message_Argument_Error(
                    '\nInappropriate field data type.\nType of field \'%s\' should be %s, but %s is given.' % (
                        field_name, Message.REQUIRED_FIELDS.get(field_name), str(type(
                            value))))
        self.__fields[field_name] = value

    def __repr__(self):
        return repr(self.__fields)

    def __str__(self):
        return '<%s object with fields:%s>' % (self.__class__.__name__, self.__fields)

    @staticmethod
    def parse_str(s):
        # type: (str) -> Message
        try:
            return Message(literal_eval(s))
        except Exception as e:
            raise Message._Message_Argument_Error(str(e))

    class _Message_Argument_Error(SyntaxError):
        msg = ''

        def __init__(self, msg):
            # type: (str) -> None
            self.msg = msg

        def __str__(self):
            return self.msg



# msg = Message.parse_str(repr(
#     Message({'Sender': 123, 'Message': 'hehe', 'Receivers': [1, 2, 3], 'Type': MESSAGE_MSG_TYPE})))
# print (msg)
