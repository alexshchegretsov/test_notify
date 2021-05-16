from flask import Flask, request, Response
from flask_dramatiq import Dramatiq
from flask_admin import Admin
from flask_admin.contrib.sqla.view import ModelView
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from periodiq import PeriodiqMiddleware, cron
from settings import SQLALCHEMY_DATABASE_URI
from models import Template, Content, Event
from misc import TemplateType
import logging
import json

app = Flask(__name__)
dramatiq = Dramatiq(app)
dramatiq.broker.add_middleware(PeriodiqMiddleware())
# dramatiq.middleware.append(PeriodiqMiddleware())
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = 'A0Zr98j/3yXeqwe R~XHH!jmN]LWX/312l123sa,?RT'
db = SQLAlchemy(app, session_options={'query_cls': BaseQuery})

admin = Admin(app, name='notify', template_mode='bootstrap3')

admin.add_view(ModelView(Template, db.session))
admin.add_view(ModelView(Content, db.session))
admin.add_view(ModelView(Event, db.session))


@dramatiq.actor(periodic=cron('* * * * *'))
def hartbeat():

    with open('cron.txt', 'a') as f:
        f.write('text\n')
    logging.info('PULSE')


@dramatiq.actor(queue_name='hello')
def websocket_notify(data):
    logging.info(data)
    with open('websocket.txt', 'a') as f:
        f.write(json.dumps(data))


@dramatiq.actor(queue_name='ready')
def email_notify(data):
    logging.info(data)
    with open('email.txt', 'a') as f:
        f.write(json.dumps(data))


class Router:
    exchange = {
        'register_user': [email_notify, websocket_notify]
    }


"""
{
    'event_type': 'register_user',
    'x_request_id': 'bazz',  - get from http header
    'user_name': 'foo',
    'email': 'foo@bar.com'
    
}
"""


@app.route('/', methods=['POST'])
def index():
    data = request.get_json(force=True)
    event_type = data.get('event_type')
    content = db.session.query(Content) \
        .join(Event, Event.id == Content.event_id) \
        .filter(Event.name == event_type).all()
    template = db.session.query(Template).filter(Template.type == TemplateType.UNNAMED).all()

    queues = Router.exchange.get(data['event_type'])
    for queue in queues:
        queue.send(data)
    return Response(status=200)


# or use named URL, coz url dispatcher == rabbit exchange point
@app.route('/register_user', methods=['POST'])
def register_user():
    # prepare template/message
    # create job
    # send to queue
    pass


@app.route('/comment_like', methods=['POST'])
def comment_like():
    # prepare template/message
    # create job
    # send to queue
    pass


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9001)
