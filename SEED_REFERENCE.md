# Seed Script Reference

## Quick Commands

```bash
# Basic seed (will skip if data exists)
python app/seed.py

# Force seed (add data even if exists)
python app/seed.py --force

# Clear all data then seed fresh
python app/seed.py --clear
python app/seed.py
```

## What Gets Seeded

✅ **1 User:**
- Name: John Doe
- Email: john.doe@example.com

✅ **2 Exercises:**
- Bench Press (STRENGTH) - Chest, shoulders, triceps exercise
- 5K Run (CARDIO) - 5-kilometer running workout

✅ **1 Workout:**
- Linked to John Doe
- Date: Yesterday
- Notes: "Great chest day! Increased weight by 5 lbs..."

✅ **1 Run:**
- Linked to John Doe
- Distance: 5.2 km
- Duration: 28 minutes (1680 seconds)
- Pace: 5.38 min/km
- Date: 2 days ago

## Usage Scenarios

### Scenario 1: First Time Setup
```bash
python app/seed.py
# ✅ Adds all sample data
```

### Scenario 2: Data Already Exists
```bash
python app/seed.py
# ⚠️  Database already contains 1 user(s).
#    Use --force to add more data anyway
#    Use --clear to delete existing data first
```

### Scenario 3: Add More Sample Data
```bash
python app/seed.py --force
# ✅ Adds another John Doe with new exercises/workouts/runs
```

### Scenario 4: Start Fresh
```bash
python app/seed.py --clear
# ⚠️  This will DELETE all data. Are you sure? (yes/no): yes
# ✅ Deleted 1 runs
# ✅ Deleted 1 workouts
# ✅ Deleted 2 exercises
# ✅ Deleted 1 users

python app/seed.py
# ✅ Adds fresh sample data
```

## Verification

### Check if data exists:
```bash
# Count users
docker exec fitforge-postgres psql -U admin -d fitforge -c "SELECT COUNT(*) FROM users;"

# View users
docker exec fitforge-postgres psql -U admin -d fitforge -c "SELECT id, name, email FROM users;"

# View all tables
docker exec fitforge-postgres psql -U admin -d fitforge -c "
  SELECT 'users' as table, COUNT(*) as count FROM users
  UNION ALL
  SELECT 'exercises', COUNT(*) FROM exercises
  UNION ALL
  SELECT 'workouts', COUNT(*) FROM workouts
  UNION ALL
  SELECT 'runs', COUNT(*) FROM runs;
"
```

### Expected output after first seed:
```
  table   | count
----------+-------
 users    |     1
 exercises|     2
 workouts |     1
 runs     |     1
```

## Common Issues

### Issue: "EOF when reading a line"
**Cause:** Old version of seed script tried to prompt for input
**Fix:** Updated! Now shows message instead of prompting

### Issue: "Database already contains X user(s)"
**Solution:** This is expected behavior!
- To skip: Just move to next step (data already exists)
- To add more: `python app/seed.py --force`
- To reset: `python app/seed.py --clear` then `python app/seed.py`

### Issue: "ModuleNotFoundError: No module named 'app'"
**Fix:**
```bash
# Make sure you're in the correct directory
cd fitforge-backend

# Make sure venv is activated
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows
```

### Issue: "ModuleNotFoundError: No module named 'sqlalchemy'"
**Fix:**
```bash
pip install -r requirements.txt
```

## Integration with API

After seeding, the `/api/test` endpoint returns:

```json
{
  "ok": true,
  "db_user_count": 1,
  "first_user": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
}
```

## Pro Tips

1. **Check before seeding:**
   ```bash
   docker exec fitforge-postgres psql -U admin -d fitforge -c "SELECT COUNT(*) FROM users;"
   ```

2. **Reset database completely:**
   ```bash
   python app/seed.py --clear
   python -m app.scripts.create_db  # Recreate tables if needed
   python app/seed.py
   ```

3. **Seed multiple times for testing:**
   ```bash
   # Adds multiple John Does (useful for pagination testing)
   python app/seed.py --force
   python app/seed.py --force
   python app/seed.py --force
   ```

4. **Quick verification:**
   ```bash
   curl http://localhost:8000/api/test | jq
   ```

## Summary

- **Default behavior:** Skip if data exists (safe)
- **`--force` flag:** Add data anyway (testing multiple records)
- **`--clear` flag:** Delete everything (start fresh)
- **No interactive prompts:** Works in scripts/automation
