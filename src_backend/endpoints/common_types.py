
# class HTTP404(Exception):
#     """For HTTP 404"""
#
# class HTTP403(Exception):
#     """For HTTP 404"""

class WebResponse:
    def __init__(
        self,
        status_code: int,
        content_type: str,
        body: str,
        headers: list[tuple[str,str]],
        # cookies, # can be passed in headers
    ):
        self.status_code = status_code
        self.content_type = content_type
        self.body = body
        self.headers = headers
