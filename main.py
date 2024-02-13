import requests
from bs4 import BeautifulSoup

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
    return img_tag.attrs["data-lazy-src"]

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return "This is root path from MyAPI"


# if __name__ == "__main__":
#     url = "https://blog.naver.com/PostList.naver?blogId=naramf&categoryNo=25"
#     response = get_requests(url)
#     image_url = data_parser(response)
#     print(image_url)