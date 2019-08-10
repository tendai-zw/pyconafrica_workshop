from maltego_trx.maltego import UIM_TYPES

from maltego_trx.transform import DiscoverableTransform
import sqlite3
import re


class searchcompany(DiscoverableTransform):
    """
    This will return all the companies which contains the phrase
    
    Input Entity: Phrase
    Output Entity: Company
    """

    @classmethod
    def create_entities(cls, request, response):
        try:
            companyName = request.Value
            companyName = re.sub('[,!.&"()-:]', ' ', companyName)  #replacing problem creating special charactes with space

            
            QUERY = "SELECT ROWID FROM company_fts WHERE name MATCH '" + companyName + "' order by rank"

            conn = sqlite3.connect('C:\\handelsregister.db')
            cursor = conn.execute(QUERY)
            
            for row in cursor:
                QUERY = "SELECT name, company_number, current_status, registered_address, native_company_number " \
                        "FROM company " \
                        "WHERE ROWID = " + str(row[0])
                cursor = conn.execute(QUERY)
                for row1 in cursor:
                    companyTableE = response.addEntity("maltego.Company", row1[0])
                    companyTableE.addProperty('companynumber', 'Company Number', 'strict', row1[1])
                    companyTableE.addProperty('registrationstatus', 'Registration Status', 'strict', row1[2])
                    companyTableE.addProperty('registeredaddress', 'Registered Address', 'strict', row1[3])
                    companyTableE.addProperty('nativecompanynumber', 'Native Company Number', 'strict', row1[4])
            conn.close()
        except Exception as e:
            response.addUIMessage("Error: " + str(e), UIM_TYPES["partial"])
