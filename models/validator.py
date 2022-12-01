from pydantic import BaseModel, validator
from datetime import datetime


class OrderValidate(BaseModel):
    client_name: str
    client_org: str
    num: int
    total: int | float
    date: str
    service: str

    @validator("client_name")
    def name_should_be_not_empty(cls, client_name: str):
        if client_name == '':
            raise ValueError("client_name is empty")
        return client_name

    @validator("client_org")
    def org_should_be_not_empty(cls, client_org: str):
        if client_org == ' ':
            raise ValueError("client_org is empty")
        return client_org

    @validator("num")
    def org_should_be_not_empty(cls, num: str):
        if num < 0:
            raise ValueError("num is uncorrect")
        return num

    @validator("total")
    def org_should_be_not_empty(cls, total: str):
        if total < 0:
            raise ValueError("total is uncorrect")
        return total

    @validator("date")
    def service_should_be_date_format(cls, date: str):
        return datetime.strptime(date, "%d.%m.%Y").date()

    @validator("service")
    def service_should_be_not_empty(cls, service: str):
        if not service or service == "-":
            raise ValueError("service is empty or '-'")
        return service


class FilterValidate(BaseModel):
    filter: str

    @validator("filter")
    def name_should_be_not_empty(cls, filter: str):
        if filter not in ('client_name', 'client_org', 'num', 'total', 'date', 'service'):
            raise ValueError("filter is uncorrect")
        return filter
