from dependency_injector import containers, providers
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session

from services.Repository import Repository

URL = "sqlite:///./test.db?check_same_thread=False"


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["blueprints"])

    engine = providers.Callable(create_engine, url=URL, echo=True, future=True)
    session = providers.Resource(Session, bind=engine)
    repository = providers.Factory(Repository, session=session)