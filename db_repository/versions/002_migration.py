from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('token', INTEGER),
    Column('username', VARCHAR(length=64)),
    Column('role', SMALLINT),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('twitter_id', Integer),
    Column('access_token', String(length=64)),
    Column('access_secret', String(length=64)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['token'].drop()
    post_meta.tables['user'].columns['access_secret'].create()
    post_meta.tables['user'].columns['access_token'].create()
    post_meta.tables['user'].columns['twitter_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['token'].create()
    post_meta.tables['user'].columns['access_secret'].drop()
    post_meta.tables['user'].columns['access_token'].drop()
    post_meta.tables['user'].columns['twitter_id'].drop()
