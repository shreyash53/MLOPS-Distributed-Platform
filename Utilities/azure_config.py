from azure.storage.file import FileService
from azure.storage.file import ContentSettings
import os
import dotenv
from constant import *
dotenv.load_dotenv() 

fileshareName = os.environ.get('AZURE_FILESHARE')

file_service = FileService(account_name=os.environ.get('AZURE_STORAGE_NAME'), account_key=os.environ.get('AZURE_STORAGE_KEY'))

def create_dir(parent_dir,child_dir):
    '''
    Parent Dir: Directory in Azure inside which you want to create folder
    Child Dir: Directory name you want to add
    '''
    file_service.create_directory(parent_dir, child_dir)

def upload_file(azurePath,filePath,azureFileName,fileType):
    '''
    azurePath: Folder path where you want to upload file
    filePath: filePath(including file) which you want to upload
    azureFileName: Name of the file you want to keep
    fileType: Type of file you are uploading

    Common File Types
    {extension, type}
    {".java", "text/x-java-source,java"},
    {".js", "application/javascript"},
    {".json", "application/json"},
    {".jpeg", "image/jpeg"},
    {".jpg", "image/jpeg" },
    {".txt", "text/plain"},
    {".zip", "application/zip"},

    '''
    file_service.create_file_from_path(
    os.environ.get('AZURE_FILESHARE'),
    azurePath,  # We want to create this file in the root directory, so we specify None for the directory_name
    azureFileName,
    filePath,
    content_settings=ContentSettings(content_type=fileType))


def download_dir(azurePath, azureFileName, filePath):
    '''
    azurePath: Folder path where you want to upload file
    azureFileName: Name of the file you want to keep
    filePath: filePath(including file) which you want to upload
    '''
    file_service.get_file_to_path(fileshareName, azurePath, azureFileName, filePath)

