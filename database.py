from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLite数据库文件路径
SQLALCHEMY_DATABASE_URL = "sqlite:///./scripts.db"

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 数据库模型基类
Base = declarative_base()

# 剧本数据库模型
class Script(Base):
    __tablename__ = "scripts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    script_type = Column(String(50))
    novel_content = Column(Text)
    yaml_content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 创建所有数据库表
Base.metadata.create_all(bind=engine)

# 数据库依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()