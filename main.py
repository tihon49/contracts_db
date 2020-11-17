import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

engine = sa.create_engine('postgresql+psycopg2://contracts_admin:1234@localhost:5432/contracts_db')  # 60557
connection = engine.connect()
Base = declarative_base()
session = sessionmaker(bind=engine)()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    fullname = sa.Column(sa.String)
    nickname = sa.Column(sa.String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (self.name, self.fullname, self.nickname)


class Agent(Base):
    __tablename__ = 'agents'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(48))

    def __repr__(self):
        return f'<Agent(name="{self.name}")>'


def main():
    Base.metadata.create_all(engine)

    while True:
        print('1. создать нового пользователя\n'
              '2. показать всех пользователей\n'
              'q. выйти\n')

        choose = input()

        if choose == '1':
            name = input('Enter a name: ')
            fullname = input('Enter a fullname: ')
            new_user = User(name=name, fullname=fullname)
            session.add(new_user)
        elif choose == '2':
            q = session.query(Agent).all()
            for a in q:
                print(a)
        elif choose == 'q':
            break




if __name__ == '__main__':
    main()
