from flask_app import db, app
from flask_admin import Admin
from flask_admin.contrib.sqla.view import ModelView
from models import Template, Content, Notification

admin = Admin(app, name='notify', template_mode='bootstrap3')
admin.add_view(ModelView(Template, db.session))
admin.add_view(ModelView(Content, db.session))
admin.add_view(ModelView(Notification, db.session))
