import psycopg2 as pg


def create_agent_table(cur):
    """Создание таблицы Agents"""

    # создаем таблицу Agents, если такой еще нет
    cur.execute("""
        create table if not exists Agents(
            id serial primary key,
            name varchar(48) UNIQUE not null    
        );
    """)


def create_contract_table(cur):
    """
    создание таблицы Contracts которая содержит
    данные о договоре с привязкой к контрагенту
    """

    # создаем таблицу Contracts, если такой еще нет
    cur.execute("""
        create table if not exists Contracts(
            id serial primary key,
            agent_id integer references agents(id) on delete cascade,
            number varchar(24) not null,
            description varchar(128)
        );
    """)


def create_bills_table(cur):
    """создание таблицы счетов Bills"""

    cur.execute("""
        create table if not exists Bills(
            id serial primary key,
            contract_id integer references contracts(id) on delete cascade,
            bill_number varchar(24) not null,
            act_number varchar(24) not null,
            sum integer not null,
            bill_date date not null,
            act_date date null
        );
    """)


def insert_new_agent(agent_name, cur):
    """
    доабавление контрагента в таблицу Agents

    agent_name: string с именем добовляемого контрагента
    """

    try:
        cur.execute(f"insert into Agents(name) values(%s)", (agent_name,))
    except pg.Error as e:
        print(e)
        # print('Данныйы контрагент уже существует в БД')


def insert_new_contract(agent_id, name, description, cur):
    """
    добавление нового договора в таблицу Contracts
    с привязкой к id контрагента из таблицы Agents

    agent_id: integer id контрагента из таблицы Agents
    name: string номер договора
    description: string краткое описание договора
    """

    # вставляем в таблицу Contracts новый договор с привязкой к контрагенту
    cur.execute(f"insert into Contracts(agent_id, number, description) values(%s, %s, %s)",
                (agent_id, name, description))


def show_all_agents(cur):
    """Вывод всех контрагентов из таблицы Agents"""

    cur.execute("select * from Agents")
    agents = cur.fetchall()

    for agent in agents:
        id_ = agent[0]
        name = agent[1]
        print(f'id: {id_} name: {name}')
    print()


def show_all_contracts(cur):
    """Вывод всех договоров из таблицы Contracts"""

    cur.execute("select * from Contracts")
    contracts = cur.fetchall()

    for contract in contracts:
        id_ = contract[0]
        agent_id = contract[1]
        contract_number = contract[2]
        description = contract[3]
        print(f'id: {id_}  agent_id:{agent_id}  contract_number: {contract_number}\n'
              f'description: {description}\n')
    print()


def show_all_bills(cur):
    """Вывод всех счетов"""

    cur.execute('select * from Bills')
    all_bills = cur.fetchall()

    for bill in all_bills:
        print(bill)
    print()


def show_all(cur):
    """Вывод сводной (JOIN) информации из таблиц Agents и Contracts"""

    cur.execute("""
        select c.id, name, agent_id, number, description 
        from contracts as c
        join Agents a
        on c.agent_id = a.id
    """)
    relations = cur.fetchall()

    for item in relations:
        id_ = item[0]
        agent_name = item[1]
        agent_id = item[2]
        contract_number = item[4]
        description = item[5]
        print(f'id: {id_}, agent_name: {agent_name}, agent_id: {agent_id}\n'
              f'description: {description}\n, '
              f'contract_number: {contract_number}')
        print()
    print()


def main():
    conn = pg.connect(dbname='contracts_db', user='contracts_admin', password='1234')
    conn.set_session(autocommit=True)  # чтобы не делать conn.commit() каждый раз
    cur = conn.cursor()

    create_agent_table(cur)
    create_contract_table(cur)
    create_bills_table(cur)

    while True:
        choose = input('Выберите действие:\n'
                       '1. Добавить контрагента\n'
                       '2. Добавить договор\n'
                       '3. Посмотреть список контрагентов\n'
                       '4. Посмотреть список договоров\n'
                       '5. Посмотреть все счета\n'
                       '6. Вывести всю информацию\n'
                       )

        if choose == 'q':
            break
        elif choose == '1':
            name = input('Введите имя контрагета: ')
            insert_new_agent(name, cur)
        elif choose == '2':
            agent_id = int(input('Введите id контрагента: '))
            number = input('Введите номер договора: ')
            description = input('Введите описание договора: ')
            insert_new_contract(agent_id, number, description, cur)
        elif choose == '3':
            show_all_agents(cur)
        elif choose == '4':
            show_all_contracts(cur)
        elif choose == '5':
            show_all_bills(cur)
        elif choose == '6':
            show_all(cur)
        else:
            print('Введена не верная команда. Попробуйте еще раз\n')

    conn.close()


if __name__ == '__main__':
    main()
