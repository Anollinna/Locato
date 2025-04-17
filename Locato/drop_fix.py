from linecache import cache
from pathlib import PurePath, PurePosixPath
from storages.backends.dropbox import DropboxStorage


class PatchedDropboxStorage(DropboxStorage):
    def _full_path(self, name):
        fixed_name = PurePath(name).as_posix()
        full_pash = (PurePosixPath(self.root_path) / fixed_name).as_posix()
        return full_pash

    # @staticmethod
    # def _generate_cache_key(name):
    #     return f"dropbox_{name}"
    #
    # def url(self, name):
    #     cache_key = self._generate_cache_key(name)
    #
    #     if cached_url := cache.get(cache_key):
    #         return cached_url
    #
    #     url = super().url(name)
    #
    #     cache.set(cache_key, url, 60 * 60 * 3)
    #     return url

    # def _save(self, name, content):
    #     super()._save(name, content)
    #
    #     url = self.client.sharing_create_shared_link_with_settings(self._full_path(name))
    #     url = url.url.replace("&dl=0", "&dl=1")
    #
    #     return url
    #
    # def url(self, name):
    #     return name
    #I wanted the photos to load faster but it doesn't work