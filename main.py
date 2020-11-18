import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

engine = db.create_engine('postgresql+psycopg2://contracts_admin:1234@localhost:5432/contracts_db')  # 60557
connection = engine.connect()
Base = declarative_base()
session = sessionmaker(bind=engine)()


def choose_table_to_show(choose_number: str):
    """выдаем queryset указанной таблицы"""

    if choose_number == '1':
        table = Agent
    elif choose_number == '2':
        table = Contract
    elif choose_number == 'q':
        return
    else:
        print('Не верная команда\n')
        return

    query = session.query(table).all()
    for item in query:
        print(item)


class Agent(Base):
    """таблица agents"""

    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(48))

    def __repr__(self):
        return f'<Agent(name="{self.name}")>'


class Contract(Base):
    """таблица с договорами contracts"""

    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    number = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Contract(id="{self.id}", agent_id="{self.agent_id}", number="{self.number}"\n' \
               f'description: {self.description})>\n'


class Bill(Base):
    """таблица счетов bills"""

    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.ForeignKey('contract.id'), nullable=False)
    bill_number = db.Column(db.String(24), nullable=False)
    act_number = db.Column(db.String(24), nullable=False)
    bill_sum = db.Column(db.Integer, nullable=False)
    act_sum = db.Column(db.Integer, nullable=False)
    bill_date = db.Column(db.Date)
    act_date = db.Column(db.Date)

    def __repr__(self):
        return f'<Bill(id="{self.id}", contract_id="{self.contract_id}", bill_number="{self.bill_number}", ' \
               f'act_number="{self.act_number}"\nbill_sum="{self.bill_sum}", act_sum="{self.act_sum}", ' \
               f'bill_date="{self.bill_date}", act_date="{self.act_date}")>'


def main():
    Base.metadata.create_all(engine)  # создание всех таблиц

    while True:
        print('1. создать нового пользователя\n'
              '2. Поиск по таблицам\n'
              'q. выйти\n')

        choose = input()

        if choose == '1':
            pass
        elif choose == '2':
            choose_number = input('\n1. Все агенты\n2. Все договоры\nq. Назад\n')
            choose_table_to_show(choose_number)
        elif choose == 'q':
            break


if __name__ == '__main__':
    main()
