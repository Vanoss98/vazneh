import mimetypes
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class VercelBlobStorage(Storage):
    """Store public Django media files in the project's Vercel Blob store."""

    def __init__(self, client=None):
        self._client = client

    @property
    def client(self):
        if self._client is None:
            from vercel.blob import BlobClient

            self._client = BlobClient()
        return self._client

    def _open(self, name, mode="rb"):
        if mode not in {"r", "rb"}:
            raise ValueError("Vercel Blob files can only be opened for reading.")
        filename = PurePosixPath(name).name
        downloaded = self.client.get(name)
        return ContentFile(downloaded.content, name=filename)

    def _save(self, name, content):
        content.seek(0)
        content_type = getattr(content, "content_type", None)
        if not content_type:
            content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
        uploaded = self.client.put(
            name,
            content.read(),
            access="public",
            content_type=content_type,
            add_random_suffix=True,
        )
        return uploaded.url

    def delete(self, name):
        if name:
            self.client.delete(name)

    def exists(self, name):
        return False

    def size(self, name):
        return self.client.head(name).size

    def url(self, name):
        if name.startswith(("https://", "http://")):
            return name
        return self.client.head(name).url
