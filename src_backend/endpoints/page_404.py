
import html
from urllib.parse import urlparse, parse_qs

from .common_types import WebResponse

from .lib.htmltmpl.src import make_html #, wrap_div


def render(request, msg = None):
    path = f'{urlparse(request.path).path}'
    msg = f'{msg}' if msg is not None else f'{path} was not found on this server'
    main_section = f'''
<div class="container">
{html.escape(msg)}
</div>
    '''
    response = make_html(
        title = '404 not found',
        page = 'Fileshare',
        h1 = '404 not found',
        meta = [],
        assets = [],
        cssclasses = ['page-error','page-error-404'],
        banners = [],
        sections = [main_section],
    )
    return WebResponse(
        status_code = None,
        content_type = 'text/html',
        body = response,
        headers = [],
    )
