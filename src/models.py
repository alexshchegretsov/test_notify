import uuid
import datetime as dt

from flask import Markup
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from misc import TemplateType

Base = declarative_base()
metadata = Base.metadata


class Event(Base):
    __tablename__ = 'event'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    def __str__(self):
        return self.name


class Template(Base):
    __tablename__ = 'template'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    type = Column(String)  # named/unnamed
    text = Column(Text)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    def __str__(self):
        return self.text[:50]


class Content(Base):
    __tablename__ = 'content'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey('event.id'), nullable=False)  # register_user, new films for the week,
    event = relationship('Event', backref='content')
    text = Column(Text)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    def __str__(self):
        return self.text[:50]


# class Notification(Base):
#     __tablename__ = 'notification'
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
#     text = Column(Text)
#
#     event_type = Column(String)   # register_user
#     content_id = Column(UUID, ForeignKey('content.id'), nullable=False)
#     template_id = Column(UUID, ForeignKey('template.id'), nullable=False)
#     content = relationship('Content')
#     template = relationship('Template')
#
#     content_data = association_proxy('content', 'text')
#     template_data = association_proxy('template', 'text')
#     template_type = association_proxy('template', 'type')
#     created_at = Column(DateTime, default=dt.datetime.utcnow)
#
#     @property
#     def data(self):
#         return self.template_data.format(content=self.content_data)
#
#     def with_username(self, name):
#         if self.template_type == TemplateType.NAMED:
#             return self.data.format(username=name)
#         return self.data
#
#     def __str__(self):
#         return self.data


class Job(Base):
    __tablename__ = 'job'

    STATUS_PENDING = 'pending'
    STATUS_DONE = 'done'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    x_request_id = Column(String, nullable=False)
    email = Column(String, nullable=False)
    status = Column(String, default=STATUS_PENDING, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    def do_job(self):
        # todo: send email and make job DONE
        pass
