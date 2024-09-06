from .jumia_scraper import scrape_jumia
from .konga_scraper import scrape_konga
from .amazon_scraper import scrape_amazon
from .ebay_scraper import scrape_ebay
from .aliexpress_scraper import scrape_aliexpress

def scrape_all_sites(query, limit=5):
    results = {
        "jumia": scrape_jumia(query)[:limit],
        "konga": scrape_konga(query)[:limit],
        "amazon": scrape_amazon(query)[:limit],
        "ebay": scrape_ebay(query)[:limit],
        "aliexpress": scrape_aliexpress(query)[:limit]
    }
    return results

#if __name__ == "__main__":
#    query = "laptop"
#    results = scrape_all_sites(query)
#    print(results)
