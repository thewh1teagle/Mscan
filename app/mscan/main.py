import webbrowser
import threading
import socket
import json
import asyncio
from mscan import settings
from mscan.scanner.interface import InterfaceManager, Interface
from mscan.scanner.scanner import Scanner
from bottle import Bottle, run, static_file, request, response

app = Bottle()
scanner = Scanner()
imanager = InterfaceManager()


def local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        pass


@app.route("/")
def index_route():
    print(settings.UI_BUILD_PATH.absolute() / 'index.html')
    return static_file("index.html", root=str(settings.UI_BUILD_PATH))


@app.route("/interfaces")
def interfaces_route():
    """ Get list of interfaces """
    # exclude 255.0.0.0 netmask since it has too many ips, billions...
    interfaces = [
        i.to_dict() for i in imanager.get_interfaces()
        if i.prefix_length != 8
    ]
    response.content_type = 'application/json'
    return json.dumps({"interfaces": interfaces, "default": imanager.get_default().to_dict()})


@app.post("/scan")
def scan_route():
    interface_data = dict(request.json)
    interface = Interface(**interface_data)
    res = asyncio.run(scanner.scan(interface))
    res = [i.to_dict() for i in res]
    response.content_type = 'application/json'
    return json.dumps(res)


@app.route("/<filename:path>")
def static_files(filename):
    return static_file(filename, root=str(settings.UI_BUILD_PATH))


def open_in_browser(host):
    webbrowser.open(f"{settings.PROTOCOL}://{host}:{settings.PORT}")


def main():
    host = settings.HOST
    if settings.HOST == "0.0.0.0":
        host = local_ip() or settings.HOST

    print(f"Mscan running at {settings.PROTOCOL}://{host}:{settings.PORT}/")
    threading.Timer(1.25, open_in_browser, (host,)).start()
    run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reloader=settings.DEV_MODE,
        server="gunicorn" if settings.DEV_MODE else "wsgiref",
    )


if __name__ == "__main__":
    main()
