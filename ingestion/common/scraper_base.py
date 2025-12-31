import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def scrape_table(
    url: str,
    days: int = 90,
) -> list[dict]:
    """
    Generic scraper for CGU table-based pages
    (Examination / Notice Board)
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table")

        if not table:
            raise ValueError("Expected table not found")

        cutoff = datetime.now() - timedelta(days=days)
        records = []

        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            try:
                date_obj = datetime.strptime(
                    cols[2].text.strip(), "%B %d, %Y"
                )
            except ValueError:
                continue

            if date_obj < cutoff:
                continue

            pdf_url = cols[3].a["href"]
            if not pdf_url.startswith("http"):
                pdf_url = f"https://cgu-odisha.ac.in{pdf_url}"

            records.append({
                "id": cols[0].text.strip(),
                "title": cols[1].text.strip(),
                "publish_date": cols[2].text.strip(),
                "pdf_url": pdf_url,
            })

        logger.info(f"Scraped {len(records)} records from {url}")
        return records

    except Exception:
        logger.exception(f"Failed scraping {url}")
        return []
