from fastapi import APIRouter, Response, HTTPException
from app.schemas import AllSubstance, EditSubstance, SmilesSubstance
from app.models import Substance
import asyncpg
from uuid import UUID


router = APIRouter(
    prefix="/admin"
)


@router.post("/add_substance")
async def add_sub(data: AllSubstance):
    data_dict = data.dict()
    try:
        await Substance.objects.create(**data_dict)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail="smiles already in use")
    return Response(content="Substance created", status_code=201)


@router.patch("/edit_substance")
async def edit_substance(data: EditSubstance):
    substance = Substance.objects.get(smiles=data.smiles)
    try:
        await substance.update(**{k: v for k, v in data.dict().items() if v})
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail="smiles already in use")
    return substance


@router.get("/get_substances")
async def get_all_substances():
    substances = await Substance.objects.filter().order_by(Substance.created_at.desc()).all()
    return substances


@router.get("/get_substances/{substance_id}")
async def get_substance_by_id(substance_id: UUID):
    substance = await Substance.objects.get(id=substance_id)
    return substance


@router.delete("/substance_delete")
async def delete_substance(smiles: SmilesSubstance):
    await Substance.objects.delete(smiles=smiles.smiles)
    return Response(content="substance was deleted", status_code=410)
