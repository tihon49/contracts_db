from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
import sqlalchemy.orm as orm

engine = db.create_engine('postgresql+psycopg2://contracts_admin:1234@localhost:5432/contracts_db')  # 60557
connection = engine.connect()

Base = declarative_base()


class Agent(Base):
    """таблица agents"""

    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(48), unique=True)
    contracts = orm.relation('Contract', backref='agent')

    def __repr__(self):
        return f'<Agent(id="{self.id}", name="{self.name}")>'


class Contract(Base):
    """таблица с договорами contracts"""

    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    number = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    bills = orm.relation('Bill', backref='contract')

    def __repr__(self):
        return f'<Contract(id="{self.id}", agent_id="{self.agent_id}", number="{self.number}", ' \
               f'description: {self.description})>\n'


class Bill(Base):
    """таблица счетов bills"""

    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)
    bill_number = db.Column(db.String(24), nullable=False)
    act_number = db.Column(db.String(24), nullable=False)
    bill_sum = db.Column(db.Integer, nullable=False)
    act_sum = db.Column(db.Integer, nullable=False)
    bill_date = db.Column(db.Date)
    act_date = db.Column(db.Date)

    def __repr__(self):
        return f'<Bill(id="{self.id}", contract_id="{self.contract_id}", bill_number="{self.bill_number}", ' \
               f'act_number="{self.act_number}", bill_sum="{self.bill_sum}", act_sum="{self.act_sum}", ' \
               f'bill_date="{self.bill_date}", act_date="{self.act_date}")>'


def create_tales():
    Base.metadata.create_all(engine)
    return


def delete_all_tables():
    Base.metadata.drop_all(bind=engine)
