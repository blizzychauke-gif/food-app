from app.providers.storage.interface import StorageProvider
class MockStorageProvider(StorageProvider):
    def upload(self, filename, seed="food"):
        url=f"https://picsum.photos/seed/{seed}/600/400"
        print(f"[MOCK STORAGE] {filename} -> {url}")
        return url