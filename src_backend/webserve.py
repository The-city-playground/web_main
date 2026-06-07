
import argparse
import traceback, sys
from dotenv import load_dotenv
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import html
import re



_VERSION = '0.000.000'
try:
    if __name__ == '__main__':
        # run as a program
        from GENERATED._VERSION import _VERSION
    elif '.' in __name__:
        # package
        from .GENERATED._VERSION import _VERSION
    else:
        # included with no parent package
        from GENERATED._VERSION import _VERSION
except ImportError:
    _VERSION = '0.000.000'

frontend_webapp_manifest_string = ''
try:
    if __name__ == '__main__':
        # run as a program
        from GENERATED._WEBAPP_VITE_MANIFEST import _WEBAPP_FRONT_VITE_MANIFEST as frontend_webapp_manifest_string
    elif '.' in __name__:
        # package
        from .GENERATED._WEBAPP_VITE_MANIFEST import _WEBAPP_FRONT_VITE_MANIFEST as frontend_webapp_manifest_string
    else:
        # included with no parent package
        from GENERATED._WEBAPP_VITE_MANIFEST import _WEBAPP_FRONT_VITE_MANIFEST as frontend_webapp_manifest_string
except ImportError:
    frontend_webapp_manifest_string = ''


if __name__ == '__main__':
    # run as a program
    from endpoints import endpoints
    from lib.webserve import Webserver, WebResponse, HTTP404, HTTP403
elif '.' in __name__:
    # package
    from .endpoints import endpoints
    from .lib.webserve import Webserver, WebResponse, HTTP404, HTTP403
else:
    # included with no parent package
    from endpoints import endpoints
    from lib.webserve import Webserver, WebResponse, HTTP404, HTTP403






# STDOUT_COLOR_RED = "\033[91m"
STDOUT_COLOR_RED = "\033[31m"
STDOUT_COLOR_RESET = "\033[0m"
STDOUT_COLOR_GREEN = "\033[32m"







load_dotenv()
PORT_NUM = os.getenv("PORT_NUM", "0")
BIND_HOST = os.getenv("BIND_HOST", "0.0.0.0")

STATIC_PATH = os.getenv("ASSET_BASE_URL", "")






def entry_point(*argcs,**kwargs):
    try:
        time_start = datetime.now()
        script_name = 'webserve'

        parser = argparse.ArgumentParser(
            description="Webserve",
            prog='webserve --program webserve'
        )
        parser.add_argument(
            '--port',
            help='port number',
            type=int,
            required=False
        )
        parser.add_argument(
            '--bind-host',
            help='bind host, something like 0.0.0.0',
            type=str,
            required=False
        )
        # args = None
        # args_rest = None
        # if( ('arglist_strict' in config) and (not config['arglist_strict']) ):
        #     args, args_rest = parser.parse_known_args()
        # else:
        args = None
        try:
            args = parser.parse_args(*argcs,**kwargs)
        except SystemExit as e:
            print(f'{STDOUT_COLOR_RED}Error: Invalid command-line arguments{STDOUT_COLOR_RESET}',file=sys.stderr)
            raise e

        port_num = PORT_NUM
        if args.port:
            port_num = args.port
            try:
                port_num = int(port_num)
            except Exception as e:
                raise Exception(f'Can\'t parse port_num param: {port_num}') from e

        bind_host = BIND_HOST

        config = {
            'script_start_time': time_start,
            'script_name': script_name,
            'script_arguments': args,
            'port': port_num,
            'bind_host': bind_host,
            'static_file_location': STATIC_PATH, # TODO: ignored for now - make it possible to pass to html_templater
            'version': _VERSION,
            'frontend_webapp_manifest_string': frontend_webapp_manifest_string,
        }

        result = Webserver().setup({'bind_host':'0.0.0.0','port':port_num}).assign_handlers(endpoints).run()

        time_finish = datetime.now()
        print('{script_name}: finished at {dt} (elapsed {duration})'.format(dt=time_finish,duration=time_finish-time_start,script_name=script_name))
    except Exception as e:
        # the program is designed to be user-friendly
        # that's why we reformat error messages a little bit
        # stack trace is still printed (I even made it longer to 20 steps!)
        # but the error message itself is separated and printed as the last message again

        # for example, I don't write "print('File Not Found!');exit(1);", I just write "raise FileNotFoundErro()"
        print('',file=sys.stderr)
        print('Stack trace:',file=sys.stderr)
        print('',file=sys.stderr)
        traceback.print_exception(e,limit=20)
        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('Error:',file=sys.stderr)
        print('',file=sys.stderr)
        print(f'{STDOUT_COLOR_RED}{e}{STDOUT_COLOR_RESET}',file=sys.stderr)
        print('',file=sys.stderr)
        exit(1)

if __name__ == '__main__':
    entry_point()
