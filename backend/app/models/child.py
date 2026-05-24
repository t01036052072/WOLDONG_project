from beanie import Document
from pydantic import Field
from datetime import datetime
from enum import Enum


class GenderEnum(str, Enum):
    male = "남자아이"
    female = "여자아이"


class RelationEnum(str, Enum):
    primary = "주양육자"
    grandparent = "조부모"
    parent = "부모"


class DisabilityTypeEnum(str, Enum):
    intellectual = "지적장애"
    autism = "자폐스펙트럼장애"


VALID_SYMPTOMS = {
    "복잡한 설명 이해 어려움",
    "반복 설명 필요",
    "사람 많은 곳에서 불안",
    "낯선 사람 경계 어려움",
    "선택지 제시 필요",
    "감각스러운 접촉 싫어함",
    "반복 질문",
    "큰 소리에 민감",
    "밝은 빛에 민감",
    "기다리기 어려움",
    "위험 상황 인식 어려움",
    "예상과 다르면 불안",
    "교통수단 이용 어려움",
    "조용한 공간 필요",
    "감정 표현 어려움",
    "기타",
}


class Child(Document):
    guardian_id: str
    name: str
    gender: GenderEnum
    birth_date: str                  # "YYYY-MM-DD"
    guardian_relation: RelationEnum
    disability_type: DisabilityTypeEnum
    symptoms: list[str]
    coping_method: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "children"