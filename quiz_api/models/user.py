from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(index=True, nullable=False)
    is_admin: bool


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str


class UserCreate(UserBase):
    hashed_password: str
    pass


class UserRead(UserBase):
    id: int
