# CT Install App

This repository contains a minimal prototype for a CT scanner installation project management system. It demonstrates:

- A Flask web app with a simple scanner model comparator.
- An engineer-only conformity check using the OpenAI API.

The web app code lives in `webapp/`. To run it, install dependencies and start the server:

```bash
pip install -r webapp/requirements.txt
python webapp/app.py
```

Set the `OPENAI_API_KEY` environment variable to enable AI responses.
