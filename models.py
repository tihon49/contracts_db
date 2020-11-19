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
    contracts = orm.relationship('Contract', backref='agent')

    def __repr__(self):
        return f'<Agent(id="{self.id}", name="{self.name}")>'


class Contract(Base):
    """таблица с договорами contracts"""

    __tablename__ = 'contracts'

    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    number = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(128), nullable=False)

    __table_args__ = (db.PrimaryKeyConstraint(agent_id, number),)

    def __repr__(self):
        return f'<Contract(agent_id="{self.agent_id}", number="{self.number}", ' \
               f'description: {self.description})>\n'


def create_tales():
    Base.metadata.create_all(engine)
    return


def delete_all_tables():
    Base.metadata.drop_all(bind=engine)
