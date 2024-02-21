import ormar
from app.core.db import BaseMeta
from uuid import UUID, uuid4
from passlib.hash import bcrypt
import datetime


class User(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    last_name: str = ormar.String(max_length=50, nullable=False)
    name: str = ormar.String(max_length=50, nullable=False)
    username: str = ormar.String(max_length=50, unique=False)
    password: str = ormar.String(max_length=128)
    is_admin: bool = ormar.Boolean(nullable=False)

    @classmethod
    async def get_user(cls, username):
        return cls.get(username=username)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)


class Substance(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    smiles: str = ormar.String(max_length=1000, nullable=False, unique=True)
    mol_formula: str = ormar.String(max_length=100, nullable=False)
    name: str = ormar.String(max_length=1000, nullable=False)
    quantity: str = ormar.String(max_length=100, nullable=True)
    location: str = ormar.String(max_length=100, nullable=True)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.utcnow)


class Request(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    user_id: UUID = ormar.UUID()
    mol_formula: str = ormar.String(max_length=1000, nullable=False)
    name: str = ormar.String(max_length=100, nullable=False)
    mol_weight: float = ormar.Float( nullable=False)
    smiles: str = ormar.String(max_length=100, nullable=False)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.utcnow)
