import json
import time

import requests
import yaml


class MyIntegration:

    def __init__(self):
        """
        Gets required variable data from config yaml file.
        """
        with open("my_variables.yml", 'r') as stream:
            try:
                self.my_variables_map = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print("[Error]: while reading yml file", exc)
        self.my_variables_map["NOTION_ENTRIES"] = {}
        self.getPageAndDatabaseData()

    def getDatabaseId(self):
        url = "https://api.notion.com/v1/databases/"
        headers = {
            'Notion-Version': '2021-05-13',
            'Authorization':
                'Bearer ' + self.my_variables_map["MY_NOTION_SECRET_TOKEN"]
        }
        response = requests.request("GET", url, headers=headers)
        self.my_variables_map["DATABASE_ID"] = response.json()["results"][0]["id"]

    def getPageAndDatabaseData(self):
        headers = {
                "Content-Type": "application/json",
                'Notion-Version': '2022-02-22',
                'Authorization': 'Bearer ' + self.my_variables_map["MY_NOTION_SECRET_TOKEN"]
            }
        if not self.my_variables_map.get("DATABASE_ID", ''):
            url = "https://api.notion.com/v1/search"
            payload = json.dumps({
                "query": 'Stocks Profits Tracker',
                "filter": {
                    "value": "database",
                    "property": "object"
                }
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            self.my_variables_map["DATABASE_ID"] = \
                response.json()["results"][0]["id"]
        
        # Database Entries
        url = f"https://api.notion.com/v1/databases/"\
              f"{self.my_variables_map['DATABASE_ID']}/query"
        response = requests.request("POST", url, headers=headers)
        resp = response.json()
        for v in resp["results"]:
            self.my_variables_map["NOTION_ENTRIES"].update(
                {
                    v["properties"]["Name"]["title"][0]["text"]["content"]: {
                        "page": v["id"],
                        "price": float(v["properties"]["Price/Unit"]["number"])
                    }
                }
            )

    def getStockPrices(self):
        """
        Download the required crypto prices using Binance API.
        Ref: https://query1.finance.yahoo.com/v8/finance/chart/
        """
        for name, data in self.my_variables_map["NOTION_ENTRIES"].items():
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{name}"
            f"?metrics=high?&interval=1h&range=1h"
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            }
            response = requests.request("GET", url, headers=headers)
            if response.status_code == 200:
                content = response.json()
                old_price = data['price']
                data['price'] = content['chart']['result'][0]['meta']['regularMarketPrice']
                new_price = data['price']
                print(f"{name}: {old_price} -> {new_price}")

    def updateNotionDatabase(self, pageId, unitPrice):
        """
        A notion database (if integration is enabled) page with id `pageId`
        will be updated with the data `coinPrice`.
        """
        url = "https://api.notion.com/v1/pages/" + str(pageId)
        headers = {
            'Authorization':
                'Bearer ' + self.my_variables_map["MY_NOTION_SECRET_TOKEN"],
            'Notion-Version': '2021-05-13',
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "properties": {
                "Price/Unit": {
                    "type": "number",
                    "number": float(unitPrice),
                },
            }
        })
        print(requests.request(
                "PATCH", url, headers=headers, data=payload
            ).text)

    def UpdateIndefinitely(self):
        """
        Orchestrates downloading of the prices and updating the same
        in notion database.
        """
        while True:
            try:
                self.getPageAndDatabaseData()
                self.getStockPrices()
                for _, data in self.my_variables_map["NOTION_ENTRIES"].items():
                    self.updateNotionDatabase(
                        pageId=data['page'],
                        unitPrice=data['price'],
                    )
                    time.sleep(1 * 5)
                time.sleep(1 * 10)
            except Exception as e:
                print(f"[Error encountered]: {e}")


if __name__ == "__main__":
    # With 😴 sleeps to prevent rate limit from kicking in.
    MyIntegration().UpdateIndefinitely()
