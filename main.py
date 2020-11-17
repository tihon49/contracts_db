import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

engine = sa.create_engine('postgresql+psycopg2://contracts_admin:1234@localhost:5432/contracts_db')  # 60557
connection = engine.connect()
Base = declarative_base()
session = sessionmaker(bind=engine)()


def choose_table_to_show(choose_number:str):
    """выдаем queryset указанной таблицы"""

    if choose_number == '1':
        table = Agent
    elif choose_number == '2':
        table = Contracts
    elif choose_number == '3':
        table = User
    elif choose_number == 'q':
        return
    else:
        print('Не верная команда\n')
        return

    query = session.query(table).all()
    for item in query:
        print(item)


class User(Base):
    """таблица users"""

    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    fullname = sa.Column(sa.String)
    nickname = sa.Column(sa.String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (self.name, self.fullname, self.nickname)


class Agent(Base):
    """таблица agents"""

    __tablename__ = 'agents'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(48))

    def __repr__(self):
        return f'<Agent(name="{self.name}")>'


class Contracts(Base):
    """таблица с договорами contracts"""

    __tablename__ = 'contracts'

    id = sa.Column(sa.Integer, primary_key=True)
    agent_id = sa.Column(sa.Integer, sa.ForeignKey('agent.id'), nullable=False)
    number = sa.Column(sa.String(24), nullable=False)
    description = sa.Column(sa.String(128), nullable=False)

    def __repr__(self):
        return f'<Contract(id="{self.id}", agent_id="{self.agent_id}", number="{self.number}"\ndescription: {self.description})>\n'


def main():
    Base.metadata.create_all(engine)  # создание всех таблиц

    while True:
        print('1. создать нового пользователя\n'
              '2. Поиск по таблицам\n'
              'q. выйти\n')

        choose = input()

        if choose == '1':
            name = input('Enter a name: ')
            fullname = input('Enter a fullname: ')
            nickname = input('Enter a nickname: ')
            new_user = User(name=name, fullname=fullname, nickname=nickname)
            session.add(new_user)
            session.commit()
        elif choose == '2':
            choose_number = input('\n1. Все агенты\n2. Все договоры\n3. Все пользователи\nq. Назад')
            choose_table_to_show(choose_number)
        elif choose == 'q':
            break


if __name__ == '__main__':
    main()
