# CT Install App

This repository contains a prototype for a CT scanner installation project management system. It now includes:

- A Flask web app with a simple scanner model comparator.
- Role-based login so only engineers can trigger the AI conformity test.
- Conformity checks against basic requirements with OpenAI integration.
- Automatic generation of a bar chart comparing required vs actual values.

The web app code lives in `webapp/`. To run it, install dependencies and start the server:

```bash
pip install -r webapp/requirements.txt
python webapp/app.py
```

Set the `OPENAI_API_KEY` environment variable to enable AI responses.
