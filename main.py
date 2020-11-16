import psycopg2 as pg


def create_agent_db(cur):
    """Создание таблицы Agents"""

    # создаем таблицу Agents, если такой еще нет
    cur.execute("""
        create table if not exists Agents(
            id serial primary key,
            name varchar(48) UNIQUE not null    
        );
    """)


def create_contract_db(cur):
    """
    создание таблицы Contracts которая содержит
    данные о договоре с привязкой к контранету
    """

    # создаем таблицу Contracts, если такой еще нет
    cur.execute("""
        create table if not exists Contracts(
            id serial primary key,
            agent_id integer references agents(id),
            number varchar(24) not null,
            description varchar(128)
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
    print(f'\n{agents}\n')


def show_all_contracts(cur):
    """Вывод всех договоров из таблицы Contracts"""

    cur.execute("select * from Contracts")
    contracts = cur.fetchall()
    print(f'\n{contracts}\n')


def show_all(cur):
    """Вывод сводной (JOIN) информации из таблиц Agents и Contracts"""

    cur.execute("""
        select * from Agents as a
        join Contracts c
        on c.agent_id = a.id 
    """)
    relations = cur.fetchall()
    print(f'\n{relations}\n')


if __name__ == '__main__':
    conn = pg.connect(dbname='contracts_db', user='contracts_admin', password='1234')
    conn.set_session(autocommit=True)  # чтобы не делать conn.commit() каждый раз
    cur = conn.cursor()

    create_agent_db(cur)
    create_contract_db(cur)

    # insert_new_agent('ООО ПримаМедика', cur)
    # insert_new_contract(1, '745-20', 'Термометрия сотрудникам и посетителям НИИСИ РАН', cur)
    # print('Все контрагеты:')
    # show_all_agents(cur)
    # print('Все договоры:')
    # show_all_contracts(cur)
    # print('Полные данные:')
    # show_all(cur)

    while True:
        chouse = input('Выберите действие:\n' \
                       '1. Добавить контрагента\n' \
                       '2. Добавить договор\n' \
                       '3. Посмотреть список контрагентов\n' \
                       '4. Посмотреть список договоров\n' \
                       '5. Вывести всю информацию\n'
                       )

        if chouse == 'q':
            break
        elif chouse == '1':
            name = input('Введите имя контрагета: ')
            insert_new_agent(name, cur)
        elif chouse == '2':
            agent_id = int(input('Введите id контрагента: '))
            number = input('Введите номер договора: ')
            description = input('Введите описание договора: ')
            insert_new_contract(agent_id, number, description, cur)
        elif chouse == '3':
            show_all_agents(cur)
        elif chouse == '4':
            show_all_contracts(cur)
        elif chouse == '5':
            show_all(cur)
        else:
            print('Введена не верная команда. Попробуйте еще раз\n')

    conn.close()
