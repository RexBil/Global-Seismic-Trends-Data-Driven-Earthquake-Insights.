from sqlalchemy import create_engine

def get_engine():
    return create_engine(
        "mysql+mysqlconnector://root:Test%40123@localhost/seismic_db"
    )
