from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import date


class MemberOnLeave(BaseModel):
    id: int
    first_name: str
    last_name: str
    leave_type: str

    model_config = ConfigDict(from_attributes=True)


class DayInfo(BaseModel):
    date: date
    members_on_leave: List[MemberOnLeave]


class TeamCalendarResponse(BaseModel):
    year: int
    month: int
    days: List[DayInfo]
