from app.providers.storage.interface import StorageProvider
class CloudinaryStorageProvider(StorageProvider):
    def upload(self, filename, seed="food"): raise NotImplementedError("Set CLOUDINARY_*")