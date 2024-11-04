# a2d2_dataset/helpers/logging_helper.py

import logging

def configure_logging():
    """
    Configures global logging for the application.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
