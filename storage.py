import csv
import logging
from datetime import datetime
from pathlib import Path

logger: logging.Logger = logging.getLogger(__name__)
root_folder: Path = Path(__file__).parent


def save_to_csv(book: dict, file_name: str):
    csv_file: Path = root_folder / f"{file_name}.csv"
    file_exists: bool = csv_file.is_file()

    row: dict = {**book, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    with open(csv_file, "a", encoding="utf-8", newline="") as wf:
        writer = csv.DictWriter(
            wf,
            fieldnames=["timestamp", "title", "price", "stock", "rating"],
            restval="N/A",
            extrasaction="ignore",
        )

        if not file_exists:
            writer.writeheader()
            logger.info("Created new CSV file: %s", csv_file)

        writer.writerow(row)
        logger.debug("Saved row: %s", row)


def check_price_drop(book: dict, threshold):
    price = book.get("price")

    if price is None:
        logger.error("No valid book price to compare.")
        return False

    return price < threshold
