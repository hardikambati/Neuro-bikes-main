from rest_framework.response import Response


class SuccessResponse():

    """
        formats success response
    """

    def __init__(self, message, status=200):
        self.message = message
        self.status = status

    def response(self):
        return Response({
            "error": False,
            "message": self.message,
            "status": self.status
        })


class FailureResponse():

    """
        formats success response
    """
    
    def __init__(self, message, status=200):
        self.message = message
        self.status = status

    def response(self):
        return Response({
            "error": True,
            "message": self.message,
            "status": self.status
        })