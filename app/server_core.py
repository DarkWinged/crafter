import argparse
import atexit
import signal
import sys
from flask import Flask
from flask_smorest import Api

from app.utils.envs import API_MAJOR_VERSION

from .server import blueprints, core
from .utils import API_VERSION, ARCHIVE_PATH, HOST, PORT


def parse_args():
    """
    Parse command-line arguments for configuring the Flask server and OpenAPI.
    """
    parser = argparse.ArgumentParser(description="Launch the Crafter API server.")

    parser.add_argument("--host", type=str, default=HOST, help="Host to bind to")
    parser.add_argument("--port", type=int, default=PORT, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")
    parser.add_argument(
        "--archive-path", type=str, default=ARCHIVE_PATH, help="Path to archive on exit"
    )

    parser.add_argument(
        "--api-title", type=str, default="Crafter API", help="Title for the API"
    )
    parser.add_argument(
        "--url-prefix", type=str, default="/", help="Prefix for all API routes"
    )
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="Run server in production mode with Gunicorn",
    )

    return parser.parse_args()


def run_flask(args):
    app = Flask(f"{args.host} {args.api_title}")
    app.logger.setLevel("DEBUG")
    app.config.update(
        API_TITLE=args.api_title,
        API_VERSION=f"v{API_VERSION}",
        OPENAPI_VERSION="3.0.3",
        OPENAPI_JSON_PATH="openapi.json",
        OPENAPI_URL_PREFIX=f"{args.url_prefix}/api/v{API_MAJOR_VERSION}",
        OPENAPI_SWAGGER_UI_PATH="/docs",
        OPENAPI_SWAGGER_UI_URL="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.25.0/",
    )
    atexit.register(core.init(args.archive_path))
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    api = Api(app)
    blueprints.init(api, app, url_prefix=args.url_prefix)
    app.run(host=args.host, port=args.port, debug=args.debug)


def main():
    args = parse_args()

    if args.deploy:
        print("Deployment mode not implemented yet.")
        exit(0)
    else:
        run_flask(args)


if __name__ == "__main__":
    main()
