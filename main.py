import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from models import Agent, Contract, Bill, create_tales, delete_all_tables

engine = db.create_engine('postgresql+psycopg2://contracts_admin:1234@localhost:5432/contracts_db')
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


def add_contract():
    """добавление контракта"""

    agent_id = int(input('id агента: '))

    # проверка на правильнось введеного id агента
    agent_query = session.query(Agent).filter_by(id=agent_id).all()
    if agent_query:
        print(f'Выбран контрагент: {agent_query[0]}')
    else:
        print('Не вероно указан id агента...\n')
        return

    number = input('Номер договора: ')
    contract_query = session.query(Contract).filter_by(agent_id=agent_id, number=number).all()
    if contract_query:
        print(f'У контрагента {agent_query[0]} уже есть договор {contract_query[0]}')
        return

    description = input('Краткое описание договора: ')

    new_contract = Contract(agent_id=agent_id, number=number, description=description)
    session.add(new_contract)
    session.commit()
    print(f'Договор №{number} добавлен\n')


def add_bill():
    """добавление счета"""

    contract_id = int(input('id Договора: '))
    bill_number = input('Номер счета: ')
    act_number = input('Номер акта: ')
    bill_sum = int(input('Сумма счета: '))
    act_sum = int(input('Сумма акта: '))

    new_bill = Bill(contract_id=contract_id, bill_number=bill_number,
                    act_number=act_number, bill_sum=bill_sum, act_sum=act_sum)
    session.add(new_bill)
    session.commit()

    bills_query = session.query(Bill).filter_by(contract_id=contract_id, bill_number=bill_number).all()
    print(f'Добавлен счет {bills_query[0]}')
    # TODO: проверку данных на валидность


def choose_table_to_show(choose_number):
    """выдаем queryset указанной таблицы"""

    if choose_number == '1':
        print(session.query(Agent).all())
    elif choose_number == '2':
        print(session.query(Contract).all())
    elif choose_number == '3':
        print(session.query(Bill).all())
    elif choose_number == 'q':
        return
    else:
        print('Не верная команда\n')
        return




def main():
    create_tales()  # создание всех таблиц

    while True:
        print('1. Внести данные в таблицы\n'
              '2. Поиск по таблицам\n'
              '3. Удалить все таблицы\n'
              'q. выйти\n')

        choose = input()

        if choose == '1':
            choose_number = input('\n1. Добавить агента\n'
                                  '2. Добавить договор\n'
                                  '3. Добавить счет\n'
                                  'q. Назад\n')
            if choose_number == '1':
                add_agent()
            elif choose_number == '2':
                add_contract()
            elif choose_number == '3':
                add_bill()
            elif choose_number == 'q':
                pass
            else:
                print('Не верная команда')

        elif choose == '2':
            choose_number = input('\n1. Все агенты\n'
                                  '2. Все договоры\n'
                                  '3. Все счета\n'
                                  'q. Назад\n')
            choose_table_to_show(choose_number)
        elif choose == '3':
            confirm = input('Вы точно уверены что хотите удалить все таблицы? (y/n): ')
            if confirm == 'y' or connection == 'yes':
                delete_all_tables()
            else:
                pass
        elif choose == 'q':
            break


if __name__ == '__main__':
    main()
