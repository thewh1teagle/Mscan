import webbrowser
import threading
from mscan import settings
from mscan.scanner.interface import InterfaceManager, Interface
from mscan.scanner.scanner import Scanner
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse
import uvicorn

app = FastAPI()
scanner = Scanner()
imanager = InterfaceManager()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index_route():
    return FileResponse(settings.UI_BUILD_PATH / "index.html")

@app.get("/interfaces")
async def interfaces_route():
    """ Get list of interfaces """
    interfaces = [i.to_dict() for i in imanager.get_interfaces()]
    return {"interfaces": interfaces, "default": imanager.get_default()}

@app.post("/scan")
async def scan_route(interface: Interface):
    res = await scanner.scan(interface)
    return res

app.mount("/", StaticFiles(directory=settings.UI_BUILD_PATH), name="public")

def open_in_browser():
    webbrowser.open(f'{settings.PROTOCOL}://{settings.HOST}:{settings.PORT}')

def main():
    threading.Timer(1.25, open_in_browser).start()
    uvicorn.run(
        "main:app" if settings.DEV_MODE else app, 
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEV_MODE,
        workers=1
    )
if __name__ == '__main__':
    main()
