# 📚 Book Price Tracker

A Python automation tool that monitors book prices on [Books to Scrape](https://books.toscrape.com), sends email alerts when prices drop below your threshold, and logs historical price data to CSV — all running automatically every 6 hours.

---

## Features

- Scrapes book title, price, stock status, and rating
- Detects price drops against a user-defined threshold
- Sends email alerts via Gmail (plain text + HTML)
- Saves price history to CSV with timestamps
- Runs on a schedule automatically every 6 hours
- Retry logic for network failures with exponential backoff
- Rate limiting between requests to avoid server bans
- Structured logging to both console and file

---

## Project Structure

```
price-tracker/
├── main.py          # Entry point — scheduler and orchestration
├── fetch_urls.py    # HTTP requests with retry and rate limiting
├── scrapper.py      # BeautifulSoup HTML parsing
├── storage.py       # CSV storage and price drop detection
├── notifier.py      # Email alerts via smtplib
├── logger_setup.py  # Logging configuration
├── .env             # Credentials (never committed)
├── .env.example     # Template for credentials
├── .gitignore
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/price-tracker.git
cd price-tracker
```

### 2. Install dependencies

This project uses [uv](https://github.com/astral-sh/uv) for package management.

```bash
uv sync
```

Or with pip:

```bash
pip install -r requirements.txt
```

### 3. Configure credentials

Copy the example env file and fill in your details:

```bash
cp .env.example .env
```

Open `.env` and add your Gmail credentials:

```
EMAIL=your_email@gmail.com
APP_PASSWORD=your_16_character_app_password
```

> **Important:** Use a Gmail App Password, not your real Gmail password. See [how to generate one](https://support.google.com/accounts/answer/185833).

### 4. Run

```bash
python main.py
```

You will be prompted for:
- The book URL from Books to Scrape (e.g. `https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html`)
- The file name to save results (e.g. `results` — saves as `results.csv`)
- Your price threshold in GBP (e.g. `15.00`)

The tracker runs immediately on start, then every 6 hours. Press `Ctrl+C` to stop.

---

## Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP requests |
| `beautifulsoup4` | HTML parsing |
| `lxml` | HTML parser backend |
| `apscheduler` | Job scheduling |
| `python-dotenv` | Credentials from `.env` |

---

## Example Output

**CSV (`results.csv`):**

```
timestamp,title,price,stock,rating
2024-01-15 09:00:00,A Light in the Attic,51.77,In Stock,Three
2024-01-15 15:00:00,A Light in the Attic,49.99,In Stock,Three
```

**Email alert:**

> **Price Alert: A Light in the Attic**
>
> A Light in the Attic is now £49.99, below your threshold of £50.00

---

## Notes

- This project scrapes [Books to Scrape](https://books.toscrape.com) — a sandbox site built for web scraping practice. It is not affiliated with any real bookstore.
- Email alerts require a Gmail account with 2-Step Verification enabled.