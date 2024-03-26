from fastapi import APIRouter, File, UploadFile, Depends, status, Response
from app.managers.users import get_user_current
from app.models import Substance, Request
from app.schemas import MolInfo, History, HistoryItem, MolInfoItem, GetInfoItem
import pubchempy as pcp
from uuid import UUID
import ormar
import aiofiles
import os
from app.managers.predict import predict
import datetime


router = APIRouter(prefix="/user")


@router.post("/get_pred")
async def get_pred(file: UploadFile = File(...), user=Depends(get_user_current)):
    try:
        path = file.filename
        async with aiofiles.open(path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
        smiles = predict(path)
        os.remove(path)
        compound = pcp.get_compounds(smiles, "smiles")
        history_item = HistoryItem(
            user_id=user.id,
            mol_formula=compound[0].molecular_formula,
            name=compound[0].iupac_name,
            mol_weight=compound[0].molecular_weight,
            smiles=smiles,
            created_at=datetime.datetime.utcnow(),
        )
        await Request.objects.create(**history_item.dict())
        try:
            substance = await Substance.objects.all(smiles=smiles)
            sub_owners = []
            for i in substance:
                item = MolInfoItem(
                        last_name=i.last_name,
                        admin_name=i.admin_name,
                        quantity=i.quantity,
                        office=i.office,
                        wardrobe=i.wardrobe,
                        shelf=i.shelf,
                        manufacturer=i.manufacturer,
                        purity=i.purity
                    )
                sub_owners.append(item)
        except ormar.exceptions.NoMatch:
            sub_owners = []
        return MolInfo(
            smiles=smiles,
            mol_formula=compound[0].molecular_formula,
            mol_weight=compound[0].molecular_weight,
            name=compound[0].iupac_name,
            owners=sub_owners
        )
    except:
        return Response(content="error", status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/get_history")
async def get_history(user=Depends(get_user_current)):
    history: History = (
        await Request.objects.filter(user_id=user.id)
        .order_by(Request.created_at.desc())
        .all()
    )
    return History(history=history)


@router.delete("/delete_history_item/{item_id}")
async def delete_history_item(item_id: UUID):
    await Request.objects.delete(id=item_id)
    return Response(status_code=410)


@router.get("/get_item_info/{smiles}")
async def get_item_info(smiles: str):
    substance = await Substance.objects.all(smiles=smiles)
    sub_owners = []
    for i in substance:
        item = MolInfoItem(
            last_name=i.last_name,
            admin_name=i.admin_name,
            quantity=i.quantity,
            office=i.office,
            wardrobe=i.wardrobe,
            shelf=i.shelf,
            manufacturer=i.manufacturer,
            purity=i.purity
        )
        sub_owners.append(item)
    return GetInfoItem(owner=sub_owners)
