# -*- coding: utf-8 -*-
'''
Created on 2017. ápr. 8.

@author: David
'''

'''
Created on 2016. m�rc. 2.

@author: SzuroveczD
'''

from googleapiclient.discovery import build
import pprint

my_api_key = "AIzaSyB3ntYlv1r1LE86IJFDqQ2c5dFEK63ULn8"
my_cse_id = "007025285003768411262:zvzianze6ts"

class Search():
    
    getlinks =[]
    
    def __init__(self,searchword):
        self.searchowrd = searchword
        self.main()

    def main(self):
          # Build a service object for interacting with the API. Visit
          # the Google APIs Console <http://code.google.com/apis/console>
          # to get an API key for your own application.
        service = build("customsearch", "v1",
                    developerKey=my_api_key)
        
        res = service.cse().list(
              q=self.searchowrd,
              cx=my_cse_id,
            ).execute()
        #pprint.pprint(res['items'])
        items = res['items']
        for i in items:
            self.getlinks=res['items']
        
  
if __name__ == '__main__':
  s = Search('zene')

 

 