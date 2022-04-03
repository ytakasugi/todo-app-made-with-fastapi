from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN

from database.db import Base