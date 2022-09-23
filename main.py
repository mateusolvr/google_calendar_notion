from calendar_api import getEvents
from notion_api import getDatabaseItems, deleteAllDbItems, addPage
import os

def main():
  # Get events from Google Calendar
  events = getEvents(None)

  databaseId = os.environ['DATABASE_ID']
  # Get notion DB pages and delete all
  dbItems = getDatabaseItems(databaseId)
  deleteAllDbItems(dbItems)
  for item in events:
    addPage(databaseId, item)


if __name__ == '__main__':
    main()