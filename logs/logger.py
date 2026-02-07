import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("https").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
