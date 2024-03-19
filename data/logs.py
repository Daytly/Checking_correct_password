from datetime import datetime

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Logs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'logs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    log_type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Logs> {self.id} {self.created_date} {self.log_type}'
