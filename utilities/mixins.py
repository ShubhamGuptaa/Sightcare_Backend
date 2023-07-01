from rest_framework.response import Response
from rest_framework import status

Content_Type_JSON = "application/json"

class ResponseViewMixin(object):

    @classmethod
    def response(cls, code, message=None, data = None):
        return Response(headers={'status':getattr(status, code)},
                        status=getattr(status, code),
                        data={
                            'message': message,
                            'status':getattr(status, code),
                            'data' : data
                        },
                        content_type=Content_Type_JSON
                        )

    @classmethod
    def success_response(cls, code='HTTP_200_OK', message=None, data = None):
        return cls.response(code, message, data)

    @classmethod
    def error_response(cls, code='HTTP_500_INTERNAL_SERVER_ERROR', message=None, data = None):
        return cls.response(code, message, data)