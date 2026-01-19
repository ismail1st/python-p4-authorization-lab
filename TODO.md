# TODO: Database Seeding for Tests

## Steps:

1. [x] Analyze the issue - tests fail because database isn't seeded
2. [x] Modify `server/testing/conftest.py` to add database seeding fixture
3. [x] Run pytest to verify tests pass - ALL 3 TESTS PASSING

## Issue Analysis:

- Tests call `User.query.first()` but database has no users
- `/clear` endpoint only clears session, not database
- Need a fixture to seed database before tests run

## Changes Made:

1. **conftest.py**: Added `setup_database` pytest fixture that:
   - Creates all database tables with `db.create_all()`
   - Seeds database with 25 users and 100 articles if not already seeded
   - Cleans up session after each test

2. **app_test.py**: Added `setup_database` fixture parameter to all 3 test methods

3. **app_test.py**: Fixed third test to query for member-only article specifically
