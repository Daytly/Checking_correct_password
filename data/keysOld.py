import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class KeysOld(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'keys_old'

    key = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    is_use = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    def __repr__(self):
        return f'<Keys Old> {self.key} {self.is_use}'
