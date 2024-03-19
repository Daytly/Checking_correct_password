import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Codes(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'codes'

    code = sqlalchemy.Column(sqlalchemy.String, nullable=True, primary_key=True)
    is_use = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)

    def __repr__(self):
        return f'<Codes> {self.code} {self.is_use}'
