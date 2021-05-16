import argparse

from sanic import Sanic
from sanic.request import Request
from sanic.response import text
from dramatiq_tasks import websocket_notify, email_notify

app = Sanic(__name__)


@app.route('/', methods=['POST'])
async def foo(request: Request):
    data = request.json

    websocket_notify.send(data)
    email_notify.send(data)
    return text('Accepted', 202)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=9001)
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port, access_log=True)
