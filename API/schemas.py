from pydantic import BaseModel

class RssFeeder(BaseModel):
    title : str
    link : str
    published : str

    class Config():
        orm_mode = True
