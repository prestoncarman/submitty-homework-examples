# See solution for assignment supplied `hello_world`
#
# This version of `hello_world` is used for testing to allow for alternate return text
return_value = ""


def set_return_value(value):
    global return_value
    return_value = value


def hello_world():
    global return_value
    return return_value
