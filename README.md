# electroplant ENGINEERING (Render auto-deploy)

This repository is configured to **auto-deploy to Render** on each GitHub push and uses a managed PostgreSQL database.

Important:
- Push this repo to GitHub and connect it to Render.
- Render will provision the Postgres instance defined in `render.yaml`.
- Render automatically sets `DATABASE_URL`. The app uses it if present.

