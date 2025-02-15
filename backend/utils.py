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
        
    def upload_raster(self, workspace_name, raster_file, raster_name):
        raster_dir = os.path.join(os.getenv("GEOSERVER_DATA_DIR"), workspace_name, "raster")
        os.makedirs(raster_dir, exist_ok=True)

        raster_file_path = os.path.join(raster_dir, f"{raster_name}.tif")
        with open(raster_file_path, 'wb') as f:
            for chunk in raster_file.chunks():
                f.write(chunk)

        return raster_file_path
     
    def publish_raster_layer(self, workspace_name, raster_name, raster_file_path):
        if not self.catalog.get_workspace(workspace_name):
            raise Exception(f"Workspace '{workspace_name}' does not exist.")
        
        coverage = self.catalog.create_coveragestore(raster_name, raster_file_path, workspace_name, overwrite=True)
        self.catalog.save(coverage)