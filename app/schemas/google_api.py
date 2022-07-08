from pydantic import BaseModel, HttpUrl


class GoogleSpreadsheetsUrl(BaseModel):
    url: HttpUrl