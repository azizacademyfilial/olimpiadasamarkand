# English levels hardened update

Updated English question levels in:
`backend/olympiad/management/commands/seed_demo.py`

Changed levels:
- Starter: 20 harder questions
- Elementary: 20 harder questions
- Pre-Intermediate: 20 harder questions
- Intermediate: 20 harder questions

Not changed:
- Beginner: left as it was

The topics were kept the same as the previous questions. Only the difficulty and sentence complexity were increased.

To apply these seed questions to a fresh or reset database, run the existing seed command from the backend folder:

```bash
python manage.py seed_demo
```
