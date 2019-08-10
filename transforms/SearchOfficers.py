from maltego_trx.maltego import UIM_TYPES
from maltego_trx.entities import Person
from maltego_trx.transform import DiscoverableTransform
import sqlite3
import re



class SearchOfficers(DiscoverableTransform):
    """
    This will return all the officers within a given Company
    Input Entity: maltego.Company
    Output Entity: maltego.Person

    """

    @classmethod
    def create_entities(cls, request, response):
        try:

            

            company_number = request.getProperty('companynumber')

            QUERY = " SELECT company.name, officer.position, officer.type, officer.name FROM company \
                     INNER JOIN officer ON company.company_number = officer.company_id \
                     WHERE  company.company_number = '" + company_number+ "'"

            conn = sqlite3.connect('C:\\handelsregister.db')
            rowcursor = conn.execute(QUERY)

            for row1 in rowcursor:
                officerPerson = response.addEntity(Person, row1[3])
                officerPerson.addProperty('position', 'Position', 'strict', row1[1])

            conn.close()
        except Exception as e:
            response.addUIMessage("Company Number or Company Name not found in the entity\n"    
                                  "Error: " + str(e), UIM_TYPES["partial"])
