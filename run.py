import os
from dotenv import load_dotenv

load_dotenv()

from app.server import create_app, start_scheduler


def main() -> None:
    app = create_app()
    start_scheduler(app)
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()

