import logging
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from fetch_urls import fetch_url
from logger_setup import setup_logging
from notifier import send_alert
from scrapper import scrape_book
from storage import check_price_drop, save_to_csv

setup_logging("price_tracker.log")

logger = logging.getLogger(__name__)


def check_price(url: str, file_path: str, threshold: float):
    logger.info("Scraping started!")

    try:
        response = fetch_url(url)
    except Exception as e:
        logger.error("Failed to fetch URL: %s", e)
        return

    html_code: str = response.text

    book: dict = scrape_book(html_code)
    logger.debug(book)
    logger.info("Finished Scraping!")

    try:
        if check_price_drop(book, threshold):
            logger.warning(
                "Book's price %.2f is below threshold %.2f", book["price"], threshold
            )

            subject = f"Price Alert: {book['title']}"
            plain_body = f"{book['title']} is now £{book['price']}, below your threshold of £{threshold}"
            html_body = f"<p><b>{book['title']}</b> is now <b>£{book['price']}</b>, below your threshold of <b>£{threshold}</b></p>"
            send_alert(subject=subject, plain=plain_body, html_text=html_body)

    except Exception as e:
        logger.error("Unable to sent the email. Cause:- %s", e)

    logger.info("saving the book data in your file: %s", file_path)
    save_to_csv(book, file_path)
    logger.info("Finished saving. you can check your data from %s", file_path)


def main():
    url: str = input("Please input the url:- ")
    file_path: str = input("Please input where you want to save your result:- ")
    try:
        threshold = float(input("Please input your budget: "))
    except ValueError:
        logger.error("Invalid threshold input. Please enter a number.")
        return

    scheduler = BlockingScheduler()

    scheduler.add_job(
        func=check_price,
        trigger="interval",
        hours=6,
        args=[url, file_path, threshold],
        next_run_time=datetime.now(),
    )

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.warning("Scheduler stopped. Was checking every 6 hours.")


if __name__ == "__main__":
    main()
