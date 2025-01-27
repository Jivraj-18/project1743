import io
import sys
from sqlalchemy import create_engine, MetaData
from sqlacodegen.codegen import CodeGenerator

def generate_model(host, user, password, database, outfile = None):
    engine = create_engine(f'postgresql://postgres.vxvglefymtcqlvylhnxj:dtl7FbAlLsVOYghU@aws-0-ap-northeast-2.pooler.supabase.com:6543/postgres')
    metadata = MetaData(bind=engine)
    metadata.reflect()
    outfile = io.open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(metadata)
    generator.render(outfile)

if __name__ == '__main__':
    generate_model('database.example.org', 'dbuser', 'secretpassword', 'mydatabase', 'db.py')