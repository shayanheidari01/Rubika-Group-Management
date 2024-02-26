<<<<<<< HEAD
from requests import Session
from pydantic import BaseModel
from json import JSONDecoder
from random import choice


class LovePoem(BaseModel):
    fa: str
    keyword: str


class TawBio(Session):
    def __init__(self) -> None:
        super().__init__()
        self.decoder = JSONDecoder().decode

    def get_bio(self):
        response = self.get('https://taw-bio.ir/f/arc/text/all~1~all~bst.json').text
=======
from requests import Session
from pydantic import BaseModel
from json import JSONDecoder
from random import choice


class LovePoem(BaseModel):
    fa: str
    keyword: str


class TawBio(Session):
    def __init__(self) -> None:
        super().__init__()
        self.decoder = JSONDecoder().decode

    def get_bio(self):
        response = self.get('https://taw-bio.ir/f/arc/text/all~1~all~bst.json').text
>>>>>>> ae03d7c0e03114d91bd2c2b97b61e921e2a0a533
        return LovePoem(**choice(self.decoder(response).get('items')))