from app.config import settings
from app.providers.storage.mock import MockStorageProvider
from app.providers.storage.cloudinary import CloudinaryStorageProvider
def get_storage_provider():
    if settings.STORAGE_PROVIDER=="cloudinary": return CloudinaryStorageProvider()
    return MockStorageProvider()