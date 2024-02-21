from pydantic import BaseModel
import orjson
from typing import Optional, List
from uuid import UUID
import datetime


class BaseSchema(BaseModel):
    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class UserAllInfo(BaseSchema):
    last_name: str
    name: str
    username: str
    password: str
    is_admin: bool


class UserAuth(BaseSchema):
    username: str
    password: str


class UserGet(BaseSchema):
    id: str
    username: str
    password: str


class UserEdit(BaseSchema):
    last_name: Optional[str]
    name: Optional[str]
    username: Optional[str]
    password: Optional[str]


class CheckEmail(BaseSchema):
    username: str


class CheckAnswer(BaseSchema):
    answer: bool


class AllSubstance(BaseSchema):
    smiles: str
    name: str
    mol_formula: str
    quantity: str
    location: str


class EditSubstance(BaseSchema):
    smiles: str
    name: Optional[str]
    mol_formula: Optional[str]
    quantity: Optional[str]
    location: Optional[str]


class SmilesSubstance(BaseSchema):
    smiles: str


class MolInfo(BaseSchema):
    smiles: str
    mol_formula: str
    mol_weight: str
    name: str
    quantity: Optional[str]
    location: Optional[str]


class HistoryItem(BaseSchema):
    user_id: UUID
    mol_formula: str
    name: str
    mol_weight: float
    smiles: str
    created_at: datetime.datetime


class History(BaseSchema):
    history: List[HistoryItem]
