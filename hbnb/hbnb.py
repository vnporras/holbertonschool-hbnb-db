""" Another way to run the app"""

from src import create_app
from src.config import ProductionConfig

app = create_app(ProductionConfig)

if __name__ == "__main__":
    app.run()
