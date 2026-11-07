import hashlib

from micita.domain.ports import HasherPasswords


class HasherMD5(HasherPasswords):
    def hash(self, password: str) -> str:
        return hashlib.md5(password.encode("utf-8")).hexdigest()
