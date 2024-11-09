from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel
from app.functions.hash import check_hash, get_hash
from app.models.auth.role import Role


class User(BaseModel):
    __tablename__ = "user"

    # Campos principais
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    _password: Mapped[str] = mapped_column(name="password", nullable=False)
    verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    
    # Escopo de permissões com Role
    scope: Mapped[list[Role]] = mapped_column(JSON, nullable=False, default=[Role.USER])

    # Getter e Setter do campo password
    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        # Aqui, você pode adicionar uma validação de senha, se necessário
        self._password = get_hash(password)

    def check_password(self, password: str) -> bool:
        # Verifica se o hash da senha confere
        return check_hash(password, self.password)

    # Se necessário, você pode definir a relação com outras tabelas aqui, como posts ou tags
    # posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")

