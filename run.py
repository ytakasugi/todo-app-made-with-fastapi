from app import urls
import uvicorn

if __name__ == '__main__':
    uvicorn.run(app = urls.app)