from datetime import date

import pydantic


class BlogInfo(pydantic.BaseModel):
    title: str
    description: str
    link: str
    published: date
    blog_text: str

    class Config:
        frozen = True

    @property
    def filename(self) -> str:
        return f'{self.title.replace(" ", "_")}.json'


class BlogSummary(pydantic.BaseModel):
    title: str
    summary: str

    @property
    def filename(self) -> str:
        return f'{self.title.replace(" ", "_")}.json'
