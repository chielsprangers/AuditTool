import enum

class loginauthmethod(enum.Enum):
    NONE = "None"
    FORM_BASED_AUTHENTICATION = "formBasedAuthentication"
    SCRIPT_BASED_AUTHENTICATION = "scriptBasedAuthentication"
    HTTP_AUTHENTICATION = "httpAuthentication"