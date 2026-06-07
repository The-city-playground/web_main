
import html, json

from .common_types import WebResponse

from .lib.htmltmpl.src import make_html #, wrap_div


def render(request,config, msg = None):
    version_str = None
    try:
        version_str = config.get('version','???')
    except Exception as e:
        version_str = f'{e}'

    is_api = (request.headers.get("Accept",None) == "application/json")

    if is_api:

        response = json.dumps({'version':version_str})
        return WebResponse(
            status_code = None,
            content_type = 'application/json',
            body = response,
            headers = [],
        )

    else:

        main_section = f'''
<div class="container">
{html.escape(f"Version: {version_str}")}
</div>
'''
        response = make_html(
            title = 'App version number',
            page = 'Fileshare',
            h1 = 'App version number',
            meta = [],
            assets = [],
            cssclasses = ['page-version'],
            banners = [],
            sections = [main_section],
        )
        return WebResponse(
            status_code = None,
            content_type = 'text/html',
            body = response,
            headers = [],
        )
