from contextlib import contextmanager
from dependency_injector import providers
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, StatementError
from sqlalchemy.orm import sessionmaker, declarative_base, registry

from sqlalchemy.orm.query import Query as _Query
from time import sleep


Base = declarative_base()
mapper_registry = registry()


class RetryingQuery(_Query):
    __max_retry_count__ = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):
        attempts = 0
        while True:
            attempts += 1
            try:
                return super().__iter__()
            except OperationalError as ex:
                if "server closed the connection unexpectedly" not in str(ex):
                    raise
                if attempts <= self.__max_retry_count__:
                    sleep_for = 2 ** (attempts - 1)
                    print(
                        "/!\\ Database connection error: retrying Strategy => sleeping for {}s"
                        " and will retry (attempt #{} of {}) \n Detailed query impacted: {}".format(
                            sleep_for, attempts, self.__max_retry_count__, ex
                        )
                    )
                    sleep(sleep_for)
                    continue
                else:
                    raise
            except StatementError as ex:
                if "reconnect until invalid transaction is rolled back" not in str(ex):
                    raise
                self.session.rollback()


class DatabaseSessionProvider(providers.Provider):
    def __init__(self, db_uri):
        self.engine = create_engine(
            db_uri,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3300,
            pool_timeout=3000,
            pool_pre_ping=True,
            echo=True,
        )
        self.session = sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False, query_cls=RetryingQuery
        )
        # event.listen(self.engine, 'checkout', self.execute_keep_alive_query)

        Base.metadata.create_all(self.engine)

    def __call__(self):
        return self.session()

    # def execute_keep_alive_query(self, dbapi_conn, connection_record, connection_proxy):
    #     try:
    #         # Execute your keep-alive query here
    #         dbapi_conn.execute("SELECT 1")
    #     except Exception as e:
    #         # Handle any errors that occur during the keep-alive query execution
    #         print(f"Error executing keep-alive query: {e}")


@contextmanager
def session_scope(session_factory: DatabaseSessionProvider):
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
