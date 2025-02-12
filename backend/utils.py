import os
from geoserver.catalog import Catalog
from dotenv import load_dotenv

load_dotenv()

class GeoServerManager:
    def __init__(self):
        self.geoserver_url = os.getenv("GEOSERVER_URL")
        self.username = os.getenv("GEOSERVER_USER")
        self.password = os.getenv("GEOSERVER_PASSWORD")
        self.catalog = Catalog(self.geoserver_url, self.username, self.password)
    
    def create_workspace(self, workspace_name):
        if not self.catalog.get_workspace(workspace_name):
            self.catalog.create_workspace(workspace_name, workspace_name)
        
    
    def create_postgis_datastore(self, workspace_name, datastore_name, db_config):
        datastore = self.catalog.create_datastore(datastore_name, workspace_name)
        datastore.connection_parameters.update(db_config)
        self.catalog.save(datastore)
       

    def publish_layer(self, workspace_name, datastore_name, layer_name):
        if not self.catalog.get_layer(layer_name):
            feature_type = self.catalog.publish_featuretype(layer_name, datastore_name, "EPSG:4326")
            self.catalog.save(feature_type)
        