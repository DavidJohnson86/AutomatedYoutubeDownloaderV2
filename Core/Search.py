# -*- coding: utf-8 -*-
from googleapiclient.discovery import build
import os

my_api_key = os.environ.get("GOOGLE_KEY")
my_cse_id = os.environ.get("CSE_ID")


class Search:
    """Handles Google API and search required object"""

    def __init__(self, searchword):
        """
        Init object variables
        Args:
            searchword(str) : The world what are you looking for.

        """
        self.searchowrd = searchword
        self.getlinks = []
        self.main()

    def main(self):
        """ Build a service object for interacting with the API. Visit
        the Google APIs Console <http://code.google.com/apis/console>
        to get an API key for your own application."""
        service = build("customsearch", "v1", developerKey=my_api_key)
        res = service.cse().list(
              q=self.searchowrd,
              cx=my_cse_id,
            ).execute()
        items = res['items']
        for item in items:
            self.getlinks=res['items']
        
  
if __name__ == '__main__':
  s = Search('zene')

 

 