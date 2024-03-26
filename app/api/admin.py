from fastapi import APIRouter, Response, HTTPException, File, UploadFile, Depends
from app.schemas import AllSubstance, EditSubstance, SmilesSubstance, AdminPred
from app.models import Substance
from app.managers.users import get_user_current
import asyncpg
import aiofiles
from app.managers.predict import predict
import os
import pubchempy as pcp
from uuid import UUID


router = APIRouter(prefix="/admin")


@router.post("/add_substance")
async def add_sub(data: AllSubstance, user=Depends(get_user_current)):
    try:
        await Substance.objects.get(user_id=user.id, smiles=data.smiles)
        return Response(status_code=409)
    except:
        data_dict = data.dict()
        data_dict["user_id"] = user.id
        data_dict["last_name"] = user.last_name
        data_dict["admin_name"] = user.name
        await Substance.objects.create(**data_dict)
        return Response(status_code=201)


@router.patch("/edit_substance")
async def edit_substance(data: EditSubstance):
    substance = await Substance.objects.get(smiles=data.smiles)
    try:
        await substance.update(**{k: v for k, v in data.dict().items() if v})
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail="smiles already in use")
    return substance


@router.get("/get_substances")
async def get_all_substances(user=Depends(get_user_current)):
    substances = (
        await Substance.objects.filter(user_id=user.id).order_by(Substance.created_at.desc()).all()
    )
    return substances


@router.get("/get_substances/{substance_id}")
async def get_substance_by_id(substance_id: UUID):
    substance = await Substance.objects.get(id=substance_id)
    return substance


@router.delete("/substance_delete")
async def delete_substance(smiles: SmilesSubstance, user=Depends(get_user_current)):
    await Substance.objects.delete(smiles=smiles.smiles, user_id=user.id)
    return Response(content="substance was deleted", status_code=410)


@router.post("/pred")
async def admin_pred(file: UploadFile = File(...)):
    try:
        path = file.filename
        async with aiofiles.open(path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
        smiles = predict(path)
        os.remove(path)
        compound = pcp.get_compounds(smiles, "smiles")
        return AdminPred(
            smiles=smiles,
            name=compound[0].iupac_name,
            mol_formula=compound[0].molecular_formula,
        )
    except:
        return Response(content="error", status_code=400)
