import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from models import Agent, Contract, Bill, create_tales

engine = db.create_engine('postgresql+psycopg2://contracts_admin:1234@localhost:5432/contracts_db')  # 60557
connection = engine.connect()
Base = declarative_base()
session = sessionmaker(bind=engine)()


def add_agent():
    """добавление нового агента"""

    name = input('Введите название контрагента: ')
    q = session.query(Agent).filter_by(name=name).all()

    # проверка на наличие агента в базе
    if q:
        print(q[0], 'уже сущесвует.')
    else:
        new_agent = Agent(name=name)
        session.add(new_agent)
        session.commit()
    return


def choose_table_to_show(choose_number: str):
    """выдаем queryset указанной таблицы"""

    if choose_number == '1':
        table = Agent
    elif choose_number == '2':
        table = Contract
    elif choose_number == '3':
        table = Bill
    elif choose_number == 'q':
        return
    else:
        print('Не верная команда\n')
        return

    query = session.query(table).all()
    for item in query:
        print(item)


def main():
    create_tales()  # создание всех таблиц

    while True:
        print('1. Внести данные в таблицы\n'
              '2. Поиск по таблицам\n'
              'q. выйти\n')

        choose = input()

        if choose == '1':
            # choose_number = input('\n1. Новый агент\n'
            #                       '2. Новый договор\n'
            #                       '3. Новый счет\n'
            #                       'q. Назад\n')
            add_agent()
        elif choose == '2':
            choose_number = input('\n1. Все агенты\n'
                                  '2. Все договоры\n'
                                  '3. Все счета\n'
                                  'q. Назад\n')
            choose_table_to_show(choose_number)
        elif choose == 'q':
            break


if __name__ == '__main__':
    main()
