import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Keys(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'keys'

    key = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    is_use = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)

    def __repr__(self):
        return f'<Keys> {self.key} {self.is_use}'
