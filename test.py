import requests
from datetime import datetime

from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import JSONResponse
import uvicorn
def get_requests(url: str) -> str:
    response = requests.get(url)
    return response.text

def data_parser(blog_data: str) -> str:
    soup = BeautifulSoup(blog_data, "html.parser")
    a = soup.find("div", {"class": "se-viewer"})
    # 날짜
    post_date = a.find("span", {"class": "se_publishDate"}) # type: ignore
    # 메인 글 포스트
    main_container = a.find("div", {"class": "se-main-container"}) # type: ignore
    # 식단표 사진
    image_box = main_container.find("div", {"class": "se-module-image"}) # type: ignore
    img_tag = image_box.find("img") # type: ignore
    return img_tag.attrs["data-lazy-src"] # type: ignore


app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str


@app.get("/")
def printHello():
	return "Hello"


@app.post("/items")
async def create_item(item: Item):
    """테스트 삼아서 만든거, 필요 없음"""
    print(item)
    dicted_item = dict(item)
    dicted_item['success'] = True
    return JSONResponse(
        content=dicted_item,
        media_type="application/json; charset=utf-8"
    )


@app.get("/test")
def test():
    return JSONResponse(
        content={"asd": 123, "test": "test"},
        media_type="application/json; charset=utf-8"
    )
@app.get("/test2")
def test2():
    return JSONResponse(
        content=str(datetime.now()),
        media_type="application/json; charset=utf-8"
    )

@app.get("/api/meal")
def get_blog_data():
    """블로그 글 크롤링 해오고 메뉴사진 및 시간 파이어베이스에 저장"""
    url = "https://blog.naver.com/PostList.naver?blogId=naramf&categoryNo=25"
    response = get_requests(url)
    image_url = data_parser(response)
    return JSONResponse(
        content=image_url,
        media_type="application/json; charset=utf-8"
    )

if __name__ == '__main__':
    uvicorn.run("test:app", reload=True)