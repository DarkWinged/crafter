import argparse
import atexit
import signal
import sys
from flask import Flask
from flask_smorest import Api

from utils import ARCHIVE_PATH, HOST, PORT

from . import blueprints, core, __version__


def parse_args():
    """
    Parse command-line arguments for configuring the Flask server and OpenAPI.
    """
    parser = argparse.ArgumentParser(description="Launch the Crafter API server.")

    parser.add_argument("--host", type=str, default=HOST, help="Host to bind to")
    parser.add_argument("--port", type=int, default=PORT, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")
    parser.add_argument(
        "--archive", type=str, default=ARCHIVE_PATH, help="Path to archive on exit"
    )

    parser.add_argument(
        "--api-title", type=str, default="Crafter API", help="Title for the API"
    )
    parser.add_argument(
        "--base-url", type=str, default="/", help="Prefix for all API routes"
    )
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="Run server in production mode with Gunicorn",
    )

    return parser.parse_args()


def run_flask(args):
    base_url = args.base_url.rstrip("/")
    app = Flask(f"{args.host} {args.api_title}")
    app.logger.setLevel("DEBUG")
    app.config.update(
        API_TITLE=args.api_title,
        API_VERSION=f"v{__version__}",
        OPENAPI_VERSION="3.0.3",
        OPENAPI_JSON_PATH="openapi.json",
        OPENAPI_URL_PREFIX=f"{base_url}/api/v{__version__.split('.')[0]}",
        OPENAPI_SWAGGER_UI_PATH="/docs",
        OPENAPI_SWAGGER_UI_URL="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.25.0/",
    )
    atexit.register(core.init(args.archive))
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    api = Api(app)
    blueprints.init(api, app, base_url=base_url)
    app.run(host=args.host, port=args.port, debug=args.debug)


def main():
    args = parse_args()

    if args.deploy:
        print("Deployment mode not implemented yet.")
        sys.exit(0)
    else:
        run_flask(args)


if __name__ == "__main__":
    main()
