import hashlib
import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()
APP_ID = os.getenv("SHOPEE_APP_ID")
SECRET = os.getenv("SHOPEE_SECRET")
SHOPEE_API_URL = "https://open-api.affiliate.shopee.com.br/graphql"

OFFERS_QUERY = """
query ($keyword: String, $limit: Int) {
  productOfferV2(keyword: $keyword, limit: $limit) {
    nodes {
      productName
      priceMin
      priceDiscountRate
      offerLink
    }
  }
}
"""


def search_shopee_offers(keyword, limit=3):
    payload = json.dumps({"query": OFFERS_QUERY, "variables": {"keyword": keyword, "limit": limit}})
    timestamp = int(time.time())
    text_to_sign = f"{APP_ID}{timestamp}{payload}{SECRET}"
    signature = hashlib.sha256(text_to_sign.encode()).hexdigest()
    headers = {
        "Authorization": f"SHA256 Credential={APP_ID}, Timestamp={timestamp}, Signature={signature}",
        "Content-Type": "application/json",
    }

    response = requests.post(SHOPEE_API_URL, headers=headers, data=payload, timeout=10)
    response.raise_for_status()
    response_body = response.json()
    if "errors" in response_body:
        raise RuntimeError(f"Shopee returned errors: {response_body['errors']}")
    offers = response_body["data"]["productOfferV2"]["nodes"]
    normalized_offers = []
    for raw_offer in offers:
        normalized_offers.append({
            "name": raw_offer["productName"],
            "price": float(raw_offer["priceMin"]),
            "link": raw_offer["offerLink"],
        })
    return normalized_offers


if __name__ == "__main__":
    print(search_shopee_offers("mouse gamer", limit=2))