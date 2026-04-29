from database import Base
print('Tables in metadata:', [table for table in Base.metadata.tables.keys()])
feedback_tables = [t for t in Base.metadata.tables.keys() if 'feedback' in t.lower() or 'rating' in t.lower()]
print('Feedback/rating tables in metadata:', feedback_tables)