from maltego_trx.entities import Phrase
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import UIM_PARTIAL
import requests

class LookUpTorExit(DiscoverableTransform):
    """
    Check if an IP is a Tor Exit Node and Returns a Phrase
    """

    @classmethod
    def create_entities(cls, request, response):
        ip_address = request.Value
        
        # cls.downloadUpdatedList()
        
        try:
            with open('tor_exit_nodes.csv', 'r') as fp:
                for row in fp:
                    if ip_address in row:
                        tor_node = response.addEntity(Phrase, 'Tor Exit Node')
                        tor_node.setNote("This is a Note")
            response.addEntity(Phrase, "Not a Tor")
        except Exception as e:    
            response.addUIMessage("An error occurred ", messageType=UIM_PARTIAL)
            

    def downloadUpdatedList():
        try:
            httpResponse = requests.get("https://check.torproject.org/exit-addresses")
            outputFile = open("tor_exit_nodes.csv",'w')
            outputFile.write(httpResponse.text)
            outputFile.close()
            httpResponse.close()
        except Exception as e:
            print(e)

