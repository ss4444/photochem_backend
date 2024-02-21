from fastapi import APIRouter, File, UploadFile, Depends, status, Response
from app.managers.users import get_user_current
from app.models import Substance, Request
from app.schemas import MolInfo, History, HistoryItem
import pubchempy as pcp
from uuid import UUID
import ormar
import aiofiles
import DECIMER
import os
import datetime

router = APIRouter(
    prefix="/user"
)


@router.post("/get_pred")
async def get_pred(file: UploadFile = File(...), user=Depends(get_user_current)):
    try:
        path = file.filename
        async with aiofiles.open(path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        smiles = DECIMER.predict_SMILES(path)
        os.remove(path)
        compound = pcp.get_compounds(smiles, "smiles")
        history_item = HistoryItem(
            user_id=user.id,
            mol_formula=compound[0].molecular_formula,
            name=compound[0].iupac_name,
            mol_weight=compound[0].molecular_weight,
            smiles=smiles,
            created_at=datetime.datetime.utcnow()
        )
        await Request.objects.create(**history_item.dict())
        try:
            substance = await Substance.objects.get(smiles=smiles)
            quantity = substance.quantity
            location = substance.location
        except ormar.exceptions.NoMatch:
            quantity = "Нет"
            location = "Нет"
        return MolInfo(
            smiles=smiles,
            mol_formula=compound[0].molecular_formula,
            mol_weight=compound[0].molecular_weight,
            name=compound[0].iupac_name,
            quantity=quantity,
            location=location
        )
    except:
        return Response(content="error", status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/get_history")
async def get_history(user=Depends(get_user_current)):
    history: History = await Request.objects.filter(user_id=user.id).order_by(Request.created_at.desc()).all()
    return History(
        history=history
    )
