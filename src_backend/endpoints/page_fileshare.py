
from urllib.parse import urlparse, parse_qs
from datetime import datetime, UTC

from dataclasses import dataclass
from typing import Any


from .common_types import WebResponse

from .lib.htmltmpl.src import make_html
# from .read_vite_manifest import get_webapp_assets
from .common_types import HTTP404, HTTP403
from .lib.permissions_manager import verify_access_permissions
from .lib import userauth as auth_service

from .lib.encoder import decrypt_payload


@dataclass(frozen=True)
class ContextProcessingRequest:
    user: Any
    session_storage: Any
    visitor_storage: Any
    user_storage: Any




def is_valid(requested_params):
    if not isinstance(requested_params,dict):
        return False
    if 'useridentity' not in requested_params:
        return False
    if 'path' not in requested_params:
        return False
    if 'issued' not in requested_params:
        return False
    if 'expires' not in requested_params:
        return False
    return True

def assume_empty_request():
    return {
        'path': '/',
        'useridentity': None,
        'issued': datetime.now(UTC),
        'expires': datetime.fromisoformat('2099-12-31T23:59:59.99+00:00'),
    }



def render(request, msg = None):
    raise Exception('Not implemented')
    path_parsed = urlparse(request.path)
    #     ParseResult(
    #     scheme='',
    #     netloc='',
    #     path='/path/to/resource',
    #     params='',
    #     query='smp=99&user=me&requested=/hello',
    #     fragment=''
    # )
    path_params = parse_qs(path_parsed.query)
    # {
    #   'smp': ['99'],
    #   'user': ['me'],
    #   'requested': ['/hello']
    # }
    webapp_js_file, webapp_css_files = get_webapp_assets(config)
    request_token = None
    token_params = path_params.get('t',[])
    if len(token_params)==0:
        # raise HTTP403('Missing token value')
        request_token = None
    elif len(token_params)==1:
        request_token = token_params[0]
    else:
        raise HTTP403('Ambiguos token value')

    requested_params = None
    try:
        requested_params = decrypt_payload(request_token) if request_token else assume_empty_request()
    except Exception as e:
        raise HTTP403('Failed to parse access token')
    if not is_valid(requested_params):
        raise HTTP403('Request is invalid')

    user = auth_service.get_user()

    if not verify_access_permissions(requested_params,user):
        raise HTTP403('The content was moved, deleted, or you don\'t have permissions to see it')

    main_section = f'''
<div class="container"><div id="app"></div></div>
    '''
    response = make_html(
        title = 'Fileshare',
        page = 'Fileshare',
        h1 = 'Fileshare',
        meta = [],
        assets = [] + [('css-link',file,) for file in webapp_css_files] + [('js-link',webapp_js_file,),],
        cssclasses = ['page-fileshare'],
        banners = [],
        sections = [main_section],
    )
    return response, 'text/html'
