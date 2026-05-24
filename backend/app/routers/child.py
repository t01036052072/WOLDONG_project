from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from beanie import PydanticObjectId

from app.models.user import User
from app.middleware.auth import parent_only
from app.utils.response import success, error
from app.models.child import Child, GenderEnum, RelationEnum, DisabilityTypeEnum, VALID_SYMPTOMS

router = APIRouter(prefix="/api/children", tags=["아동 프로필"])


# ─── 요청 스키마 ────────────────────────────────────────
class ChildCreateRequest(BaseModel):
    name: str
    gender: GenderEnum
    birth_date: date
    guardian_relation: RelationEnum
    disability_type: DisabilityTypeEnum
    symptoms: list[str]
    coping_method: str


class ChildUpdateRequest(BaseModel):
    name: Optional[str] = None
    gender: Optional[GenderEnum] = None
    birth_date: Optional[date] = None
    guardian_relation: Optional[RelationEnum] = None
    disability_type: Optional[DisabilityTypeEnum] = None
    symptoms: Optional[list[str]] = None
    coping_method: Optional[str] = None


# ─── 유효성 검사 ────────────────────────────────────────
def validate_symptoms(symptoms: list[str]):
    invalid = [s for s in symptoms if s not in VALID_SYMPTOMS]
    if invalid:
        return error(f"유효하지 않은 증상 태그: {invalid}", 422)
    if len(symptoms) != len(set(symptoms)):
        return error("중복된 증상 태그가 있습니다", 422)
    return None


# ─── 라우트 ────────────────────────────────────────────

# POST /api/children
@router.post("")
async def create_child(body: ChildCreateRequest, user: User = Depends(parent_only)):
    err = validate_symptoms(body.symptoms)
    if err:
        return err

    child = Child(
        guardian_id=str(user.id),
        name=body.name,
        gender=body.gender,
        birth_date=body.birth_date.isoformat(),
        guardian_relation=body.guardian_relation,
        disability_type=body.disability_type,
        symptoms=body.symptoms,
        coping_method=body.coping_method,
    )
    await child.insert()

    return success({
        "child_id": str(child.id),
        "name": child.name,
        "created_at": str(child.created_at)
    }, "아동 프로필이 등록되었습니다", 201)


# GET /api/children
@router.get("")
async def get_my_children(user: User = Depends(parent_only)):
    children = await Child.find(Child.guardian_id == str(user.id)).to_list()
    return success([
        {
            "child_id": str(c.id),
            "name": c.name,
            "gender": c.gender,
            "birth_date": c.birth_date,
            "disability_type": c.disability_type,
        }
        for c in children
    ])


# GET /api/children/{child_id}
@router.get("/{child_id}")
async def get_child(child_id: str, user: User = Depends(parent_only)):
    try:
        oid = PydanticObjectId(child_id)
    except Exception:
        return error("유효하지 않은 child_id입니다", 400)

    child = await Child.get(oid)
    if not child:
        return error("아동 프로필을 찾을 수 없습니다", 404)
    if child.guardian_id != str(user.id):
        return error("접근 권한이 없습니다", 403)

    return success({
        "child_id": str(child.id),
        "name": child.name,
        "gender": child.gender,
        "birth_date": child.birth_date,
        "guardian_relation": child.guardian_relation,
        "disability_type": child.disability_type,
        "symptoms": child.symptoms,
        "coping_method": child.coping_method,
        "created_at": str(child.created_at),
        "updated_at": str(child.updated_at),
    })


# PATCH /api/children/{child_id}
@router.patch("/{child_id}")
async def update_child(child_id: str, body: ChildUpdateRequest, user: User = Depends(parent_only)):
    try:
        oid = PydanticObjectId(child_id)
    except Exception:
        return error("유효하지 않은 child_id입니다", 400)

    child = await Child.get(oid)
    if not child:
        return error("아동 프로필을 찾을 수 없습니다", 404)
    if child.guardian_id != str(user.id):
        return error("접근 권한이 없습니다", 403)

    if body.symptoms is not None:
        err = validate_symptoms(body.symptoms)
        if err:
            return err

    update_data = body.model_dump(exclude_none=True)
    if "birth_date" in update_data:
        update_data["birth_date"] = update_data["birth_date"].isoformat()
    update_data["updated_at"] = datetime.utcnow()

    await child.set(update_data)
    return success(None, "아동 프로필이 수정되었습니다")


# DELETE /api/children/{child_id}
@router.delete("/{child_id}")
async def delete_child(child_id: str, user: User = Depends(parent_only)):
    try:
        oid = PydanticObjectId(child_id)
    except Exception:
        return error("유효하지 않은 child_id입니다", 400)

    child = await Child.get(oid)
    if not child:
        return error("아동 프로필을 찾을 수 없습니다", 404)
    if child.guardian_id != str(user.id):
        return error("접근 권한이 없습니다", 403)

    await child.delete()
    return success(None, "아동 프로필이 삭제되었습니다")