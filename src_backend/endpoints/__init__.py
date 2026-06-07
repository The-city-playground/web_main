

# from .page_fileshare import render as render_fileshare
from .page_404 import render as render_404
from .page_403 import render as render_403
from .page_version import render as render_version

endpoints = {
    # '/': render_fileshare,
    404: render_404,
    403: render_403,
    '/version': render_version,
}
