LabelForce - Production Starter

Quick local run:
1. Install Docker & Docker Compose.
2. From project root: docker-compose up --build
3. Backend: http://localhost:8000
4. Frontend: http://localhost:5173

Push to GitHub:
1. Ensure GH CLI installed and authenticated.
2. ./setup.sh

Deploy to Render (GUI):
1. Create Render account - connect GitHub.
2. Import repository.
3. Render auto-detects render.yaml; verify services.
4. Create managed Postgres DB on Render and copy DATABASE_URL into backend service env.
5. Set other env vars: LF_SECRET, REDIS_URL (if using managed redis), ACCESS_EXPIRE_MIN.
6. Deploy.

Notes:
- Change LF_SECRET to a long random string.
- For production, use S3 for uploads (not local disk).
- Replace placeholder AI prelabel with proper model inference or cloud endpoint.
