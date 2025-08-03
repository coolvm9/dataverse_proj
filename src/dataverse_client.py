import os
import msal
import requests
from dotenv import load_dotenv

load_dotenv()


class DataverseClient:
    def __init__(self):
        self.client_id = os.getenv("DATAVERSE_CLIENT_ID")
        self.client_secret = os.getenv("DATAVERSE_CLIENT_SECRET")
        self.tenant_id = os.getenv("DATAVERSE_TENANT_ID")
        self.environment_url = os.getenv("DATAVERSE_ENVIRONMENT_URL")
        
        if not all([self.client_id, self.client_secret, self.tenant_id, self.environment_url]):
            raise ValueError("Missing credentials in .env file")
        
        self._token = None
    
    def _get_token(self):
        if not self._token:
            app = msal.ConfidentialClientApplication(
                self.client_id,
                client_credential=self.client_secret,
                authority=f"https://login.microsoftonline.com/{self.tenant_id}"
            )
            result = app.acquire_token_for_client([f"{self.environment_url}/.default"])
            self._token = result["access_token"]
        return self._token
    
    def _request(self, endpoint, params=None):
        headers = {
            "Authorization": f"Bearer {self._get_token()}",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0"
        }
        url = f"{self.environment_url}/api/data/v9.2/{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def test_connection(self):
        try:
            self._request("WhoAmI()")
            return True
        except:
            return False
    
    def get_table_schema(self, table_name):
        params = {"$expand": "Attributes($select=LogicalName,DisplayName,AttributeType,SchemaName,IsPrimaryId)"}
        return self._request(f"EntityDefinitions(LogicalName='{table_name}')", params)
    
    def list_tables(self):
        params = {
            "$select": "LogicalName,DisplayName,SchemaName,EntitySetName",
            "$filter": "IsCustomizable/Value eq true or IsManaged eq false"
        }
        result = self._request("EntityDefinitions", params)
        return result.get("value", [])
    
    def get_table_attributes(self, table_name):
        params = {"$select": "LogicalName,DisplayName,AttributeType,SchemaName,IsPrimaryId,IsValidForCreate,IsValidForUpdate"}
        result = self._request(f"EntityDefinitions(LogicalName='{table_name}')/Attributes", params)
        return result.get("value", [])
    
    def get_dataverse_details(self):
        if self.test_connection():
            print("✅ Connected to Dataverse!")
            
            tables = self.list_tables()
            print(f"\nFound {len(tables)} tables:")
            
            for table in tables[:10]:
                name = table.get('LogicalName')
                display = table.get('DisplayName', {}).get('UserLocalizedLabel', {}).get('Label', 'N/A')
                print(f"  {name}: {display}")
        else:
            print("❌ Connection failed")