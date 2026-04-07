from bs4 import BeautifulSoup


def get_title(soup: BeautifulSoup) -> str | None:
    h1_tag = soup.select_one("div.col-sm-6.product_main > h1")
    return h1_tag.get_text(strip=True) if h1_tag else None


def get_price(soup: BeautifulSoup) -> float | None:
    p_tag = soup.select_one("div.col-sm-6.product_main > p.price_color")

    if not p_tag:
        return None

    price_text = p_tag.get_text(strip=True)

    try:
        return float(price_text[1:])  # remove currency symbol
    except (ValueError, IndexError):
        return None


def stock_status(soup: BeautifulSoup) -> str | None:
    p_tag = soup.select_one("div.col-sm-6.product_main > p.instock.availability")

    if not p_tag:
        return None

    status = p_tag.get_text(strip=True)
    return " ".join(status.split(" ")[:2])


def get_rating(soup: BeautifulSoup) -> str | None:
    p_tag = soup.select_one("div.col-sm-6.product_main > p.star-rating")

    if not p_tag:
        return None

    rating = p_tag.get("class")
    return rating[-1] if rating else None


def scrape_book(source_code):
    soup = BeautifulSoup(source_code, "lxml")

    title = get_title(soup)
    price = get_price(soup)
    stock = stock_status(soup)
    rating = get_rating(soup)

    return {"title": title, "price": price, "stock": stock, "rating": rating}
