from pip._vendor import requests
import json, os
from html.parser import HTMLParser
from io import StringIO

baseUrl = "https://api.notion.com/v1/"

notionToken = os.environ['NOTION_TOKEN']

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def callApi(method: str, endpoint: str, payload=None) -> requests.Response:
  url = baseUrl+endpoint
  if method == "get":
    response = requests.get(url, headers={"Authorization":"Bearer " + notionToken,
            "Notion-Version": "2022-06-28", "Content-Type": "application/json"})
  elif method == "post":
    response = requests.post(url, headers={"Authorization":"Bearer " + notionToken,
            "Notion-Version": "2022-06-28", "Content-Type": "application/json"}, data=payload)
  elif method == "delete":
    response = requests.delete(url, headers={"Authorization":"Bearer " + notionToken,
            "Notion-Version": "2022-06-28", "Content-Type": "application/json"})
  else:
    response = requests.get(url, headers={"Authorization":"Bearer " + notionToken,
            "Notion-Version": "2022-06-28", "Content-Type": "application/json"})

  if response.status_code != 200:
    returnError(response)

  return response

def returnError(r: requests.Response):
  print(r)
  print(r.json())
  raise Exception(r)

def getDatabaseItems(databaseId: str):
  response = callApi("post", "databases/" + databaseId + "/query")
  jsonResponse = response.json()
  items = jsonResponse["results"]

  return items

def deleteAllDbItems(dbItems: list):
  for item in dbItems:
    response = callApi("delete", "blocks/" + item["id"])
    if response.status_code != 200:
      returnError(response)

def addPage(databaseId: str, item: dict):
  description = None
  if "description" in item: 
    description = cleanDescription(item['description'])
  payload = buildCreatePagePayload(databaseId, item['summary'], description,
            item['htmlLink'], item['start']['dateTime'], item['end']['dateTime'])
  response = callApi("post", "pages", payload)
  if response.status_code != 200:
      returnError(response)

def cleanDescription(htmlDescription: str):
  htmlDescription = htmlDescription.replace("<br>", "\n")
  htmlDescription = htmlDescription.replace("</p>", "\n\n")
  cleanDescription = strip_tags(htmlDescription)
  if len(cleanDescription) > 2000:
    cleanDescription = cleanDescription[:1850] + "[...]\n\n\n[Description too is large; please check the full description directly in Calender using the link above.]"
  return cleanDescription

def buildCreatePagePayload(databaseId: str, eventTitle: str, description: str, url: str, startDate: str, endDate: str):
  if description is None:
    return json.dumps({
  "parent": {
    "database_id": databaseId
  },
  "properties": {
    "Name": {
      "title": [
        {
          "type": "text",
          "text": {
            "content": eventTitle
          }
        }
      ]
    },
    "%3F%3FPi": {
      "url": url
    },
    "Date": {
      "type": "date",
      "date": {
        "start": startDate,
        "end": endDate,
        "time_zone": None
      }
    }
  }
})

  return json.dumps({
  "parent": {
    "database_id": databaseId
  },
  "properties": {
    "Name": {
      "title": [
        {
          "type": "text",
          "text": {
            "content": eventTitle
          }
        }
      ]
    },
    "%5E%5EW%3D": {
      "rich_text": [
        {
          "text": {
            "content": description
          }
        }
      ]
    },
    "%3F%3FPi": {
      "url": url
    },
    "Date": {
      "type": "date",
      "date": {
        "start": startDate,
        "end": endDate,
        "time_zone": None
      }
    }
  }
})