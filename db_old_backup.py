# db.py
# This file holds all mock databases.
# In a real app, this would be replaced by actual database connections.

# Skills database: {id: skill_data}
SKILLS_DB: dict[int, dict] = {}

# Journals database: {id: journal_data}
JOURNALS_DB: dict[int, dict] = {}

# ID counters
next_skill_id = 1
next_journal_id = 1