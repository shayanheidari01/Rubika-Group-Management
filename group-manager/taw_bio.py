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
        return LovePoem(**choice(self.decoder(response).get('items')))