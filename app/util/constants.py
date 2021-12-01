class Constants:
    RESPONSES = {
        200: "Success",
        400: "Bad Request",
        401: "Unauthorized resources has been accessed",
        403: "Authenticated clients access unauthorized resources",
        404: "Resource Not Found",
        500: "Internal Server Error",
    }

    SPECIAL_CHARACTERS = ' !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    SMS_TYPE_REG = 'REGISTER'
    SMS_TYPE_LOGIN = 'LOGIN'
    SMS_TYPE_PASSWORD = 'FIND_PASSWORD'


# Exception constant
template = "An exception of type {0} occurred. Arguments:\n{1!r}"
