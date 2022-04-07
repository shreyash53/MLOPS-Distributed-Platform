
from azure.storage.file import FileService
import os
import dotenv
from .constants import *
dotenv.load_dotenv() 

fileshareName = os.environ.get('AZURE_FILESHARE')

file_service = FileService(account_name=os.environ.get('AZURE_STORAGE_NAME'), account_key=os.environ.get('AZURE_STORAGE_KEY'))


def download_dir(azurePath, azureFileName, filePath):
    '''
    azurePath: Folder path where you want to upload file
    azureFileName: Name of the file you want to keep
    filePath: filePath(including file) where you want to download
    '''
    file_service.get_file_to_path(fileshareName, azurePath, azureFileName, filePath)

# download_dir(AZURE_MODEL_PATH+'/demo', 'demo', '/home/shreyash/Downloads/demo.zip')