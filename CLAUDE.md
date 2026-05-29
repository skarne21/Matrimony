# Matrimony Website — Claude Context

## Commit Rules

- **Never add a `Co-Authored-By: Claude` line to any commit message.** Claude must not appear anywhere in the git history or on GitHub.

## Project Overview

An Indian matrimony platform targeting users in India. It handles culturally sensitive data (religion, caste, horoscope, government ID), so correctness, security, and compliance are non-negotiable at every layer.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vue 3 + TypeScript + Vite, Pinia, Vue Router 4, Axios |
| Backend | Django 5.2 (Python 3.11) + Django REST Framework |
| Auth | JWT via djangorestframework-simplejwt, OTP via SMS (phone-first), Email verification |
| Real-time | Django Channels 4 + Daphne (ASGI WebSocket server) |
| Database | PostgreSQL (psycopg2-binary driver) |
| File Storage | AWS S3 (two buckets: `matrimony-raw-uploads`, `matrimony-public-profiles`) |
| CDN | AWS CloudFront |
| Serverless | AWS Lambda + Pillow (image compression → WebP) |
| Image Moderation | AWS Rekognition — `DetectModerationLabels` |
| Cloud SDK | boto3 + django-storages |
| Payments | Razorpay (primary for India) |
| Config management | python-decouple (all secrets in `.env`) |

## Architecture Decisions & Constraints

- **UUIDs** for all primary keys on user-facing tables — prevents sequential ID scraping.
- **PostgreSQL JSONB** for partner preferences (acceptable_religions, acceptable_castes) — enables overlap queries without messy join tables for every preference.
- **GIN indexes** on JSONB columns for search performance.
- **Composite indexes** on `(religion_id, caste_id, gender)` in `profiles` — search queries lean on these simultaneously.
- **Cursor-based pagination** for advanced search (users must not lose place when navigating back from a profile).
- **Infinite scroll** for basic/dashboard feed.
- **Presigned S3 URLs** — frontend uploads directly to S3; the backend never touches the raw image file (saves bandwidth and compute cost).
- **AWS Lambda** compresses images to WebP at 800×800 immediately on S3 upload.
- **AWS Rekognition** auto-moderates on every upload — explicit/violent content routes to quarantine queue; clean images go live instantly.
- **CloudFront** in front of S3 — never serve images directly from S3 (outbound S3 data transfer is expensive).
- **S3 Lifecycle Policy** — raw-uploads bucket auto-deletes originals after 24 hours.
- **CloudFront cache headers** — browsers cache profile photos for 30 days minimum.
- **5 MB upload limit** enforced on the frontend to cap AWS costs.
- Rekognition costs ~$0.001/image — cheaper than human moderation at scale.
- **Payment confirmation via webhook only** — never trust the frontend to confirm a payment. Backend listens for `payment_intent.succeeded` (Razorpay/Stripe webhook).
- **Database transactions for credit deduction** — prevents race conditions when a user double-clicks "Boost Profile".
- **Unique constraint on `(sender_id, receiver_id)`** in the `interests` table — prevents interest request spam.
- **Chat requires accepted interest** — the `conversations` table has an FK to `interests`, enforcing that chat is only possible after a connection is accepted.
- **Middleware on every premium route** — checks `user_subscriptions` for an active, non-expired plan before serving gated content (phone numbers, chat initiation, etc.).
- **`expires_at` indexed** on `user_subscriptions` — a daily cron job downgrades expired accounts efficiently.

## Data Privacy & Compliance

- India's **Digital Personal Data Protection (DPDP) Act** applies — the platform collects religion, caste, government ID proofs, and location (all classified as sensitive personal data).
- Passwords stored as hashes only (bcrypt or Argon2).
- Database encryption at rest required for sensitive columns.
- Users must be able to request deletion of their data (right to erasure).
- Privacy settings on profiles must be enforced at the API level, not just the UI.

## Database Schema Reference

### `users`
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| email | String | Unique index |
| password_hash | String | Hashed |
| phone_number | String | Unique index, OTP login |
| account_status | Enum | active, suspended, deleted, pending_approval |

### `profiles`
| Column | Type | Notes |
|---|---|---|
| user_id | UUID | FK → users (1-to-1) |
| dob | Date | Dynamic age calculation |
| religion_id | Integer | FK → lookup table |
| caste_id | Integer | FK → lookup table |
| annual_income | Integer | Numeric for range filtering |
| profile_pic_url | String | Cloud storage pointer |
| is_verified | Boolean | True after ID proof approval |

### `partner_preferences`
| Column | Type | Notes |
|---|---|---|
| user_id | UUID | FK → users |
| age_min / age_max | Integer | Age bounding range |
| height_min / height_max | Integer | Height in cm |
| acceptable_religions | JSONB/Array | Multiple religion_ids |
| acceptable_castes | JSONB/Array | Multiple caste_ids |

### `profile_views`
| Column | Type | Notes |
|---|---|---|
| id | BigInt | PK |
| viewer_id | UUID | FK → users |
| viewed_id | UUID | FK → users |
| viewed_at | Timestamp | Default: now() |

### `interests`
| Column | Type | Notes |
|---|---|---|
| id | BigInt | PK |
| sender_id | UUID | FK → users |
| receiver_id | UUID | FK → users |
| status | Enum | pending, accepted, declined, withdrawn |
| created_at | Timestamp | |

**Unique constraint:** `(sender_id, receiver_id)`

### `conversations`
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| interest_id | BigInt | FK → interests (enforces accepted-only chat) |
| user_one_id | UUID | FK → users |
| user_two_id | UUID | FK → users |
| last_message_at | Timestamp | Sorts inbox by recency |

### `messages`
| Column | Type | Notes |
|---|---|---|
| id | BigInt | PK |
| conversation_id | UUID | FK → conversations |
| sender_id | UUID | FK → users |
| content_text | Text | Message body |
| is_read | Boolean | True once recipient opens chat |
| created_at | Timestamp | Indexed |

### `subscription_plans`
| Column | Type | Notes |
|---|---|---|
| id | Integer | PK |
| name | String | e.g., "Gold", "Platinum" |
| price | Decimal | Plan cost |
| duration_days | Integer | 30, 90, 180 |
| contact_views_allowed | Integer | Phone number unlock limit |
| can_initiate_chat | Boolean | Premium messaging toggle |

### `user_subscriptions`
| Column | Type | Notes |
|---|---|---|
| id | BigInt | PK |
| user_id | UUID | FK → users |
| plan_id | Integer | FK → subscription_plans |
| starts_at | Timestamp | Payment cleared date |
| expires_at | Timestamp | Indexed for cron downgrade job |
| contact_views_used | Integer | Increments on each phone unlock |

## API Endpoints (Contract Reference)

| Method | Route | Purpose |
|---|---|---|
| POST | /api/auth/register | 6-step Pinia registration payload |
| POST | /api/auth/login | Phone number → OTP |
| POST | /api/auth/verify-otp | OTP confirmation |
| GET | /api/matches | Live SQL dashboard feed |
| GET | /api/users/{id} | Full profile view |
| GET | /api/search | Advanced search with dynamic query builder |
| POST | /api/interests/{id} | Send connection request |
| PATCH | /api/interests/{id} | Accept / decline / withdraw |
| GET | /api/conversations | Inbox list |
| GET | /api/conversations/{id}/messages | Chat history |
| POST | /api/conversations/{id}/messages | Send message |
| GET | /api/profile/completeness | Returns weighted completeness score |
| POST | /api/upload/presigned-url | Returns S3 presigned URL for direct upload |
| POST | /api/subscriptions/checkout | Initiate payment session |
| POST | /api/webhooks/payment | Razorpay/Stripe webhook (provision plan) |
| GET | /api/users/{id}/phone | Unlock phone number (premium gate) |
| GET | /api/admin/flagged-photos | Moderator queue |
| DELETE | /api/admin/photos/{id} | Delete & warn (one-click nuke) |

## Key Business Rules

- Chat can only be initiated after an interest is `accepted`.
- A user cannot send interest to the same person twice (DB unique constraint, not just frontend validation).
- Phone number unlock checks `contact_views_used < contact_views_allowed` before serving the number and increments in the same transaction.
- Profile photo visibility checks `photo_privacy` setting AND viewer's subscription tier before returning the image URL.
- "Request Photo Access" button renders only when the API returns `canRequestPhoto: true`.
- Profile completeness score is a weighted integer sum of filled columns (example: bio = 15 pts, income = 5 pts). Returned by `/api/profile/completeness`.
- Moderator "Delete & Warn" action: deletes S3 object, removes DB reference, drops profile completeness score, sends warning email — all in one atomic operation.
- Expired subscriptions are downgraded by a scheduled cron job (not lazily on request).

## Frontend Component Structure (Vue 3)

- `<ProfileHeader />` — avatar, name, age, location
- `<FamilyDetails />` — family info section
- `<AstroDetails />` — horoscope/nakshatra/rashi (lazy loaded)
- Pinia stores: auth store, notification store (WebSocket-driven), matches store, chat store
- WebSocket events update Pinia notification counters globally without page refresh

## Registration Flow (6 Steps)

1. Basic Details (name, gender, DOB, marital status, height/weight, profile created by)
2. Personal & Religion (religion, caste, sub-caste, mother tongue, horoscope/nakshatra/rashi, manglik)
3. Education & Career (education, college, occupation, company, income, work location)
4. Family Details (father/mother name & occupation, siblings, family type/status)
5. Partner Preferences (age range, height, religion/caste, education, profession, location)
6. Photos & Verification (profile photo upload, ID proof, bio, privacy settings, email/mobile verification)

## Development Phases (MVP Order)

1. Repo setup — Vue init, Laravel/Django init, PostgreSQL connection
2. Database migrations and models (backend only)
3. 6-step registration UI + backend (full-stack)
4. Dashboard and Profile pages
5. Chat and Monetization gates

## Code Quality Rules

- Every premium API route must have subscription middleware — no exceptions.
- Never confirm payments on the frontend; always wait for the webhook.
- All DB writes that involve credits or counters must be wrapped in transactions.
- Dynamic query builder: if a search field is blank, omit that WHERE clause entirely.
- Images are never served directly from S3 — always through CloudFront.

---

## Build Progress Log

This section is updated after every commit. It records exactly what exists in the codebase, what decisions were made, and what comes next.

---

### Commit 1 — `39e781b` — Initial commit: add .gitignore
**Date:** 2026-05-25

**What was done:**
- Initialized the local Git repository and connected it to `github.com/skarne21/Matrimony`.
- Created `.gitignore` at the repo root.

**Key decisions:**
- `CLAUDE.md` and `plan.md` are in `.gitignore` — they are kept local only (not pushed to GitHub) because the repo is public and these files contain full architecture details.
- `backend/.env` is also gitignored — secrets never go to GitHub.

**Files created:**
- `.gitignore`

---

### Commit 2 — `a6f827d` — Add README
**Date:** 2026-05-25

**What was done:**
- Created `README.md` at the repo root for the public GitHub page.

**What the README covers:**
- Project description and feature list
- Full tech stack table
- Project folder structure (as a reference — not yet built at this point)
- Development phase tracker (Phase 1–5 with status)
- Getting started section (placeholder — to be filled in as each phase is built)

**Files created:**
- `README.md`

---

### Commit 3 — `fb2da46` — Phase 1: scaffold Vue 3 + Vite frontend, Django backend, and Lambda stub
**Date:** 2026-05-25

**What was done:**
This is the main Phase 1 infrastructure commit. Everything below now exists in the repo.

**Frontend (`frontend/`):**
- Scaffolded with `npm create vite@latest` using the `vue-ts` template (Vue 3 + TypeScript + Vite).
- Installed additional packages: `vue-router@4`, `pinia`, `axios`.
- `tsconfig.app.json`, `tsconfig.node.json`, `vite.config.ts` are all Vite defaults — not yet customized.
- `src/main.ts` and `src/App.vue` are the default Vite stubs — to be replaced when we build the registration UI in Phase 3.

**Backend (`backend/`):**
- Python virtual environment created at `backend/venv/` (not committed — gitignored).
- Django 5.2 project scaffolded with `django-admin startproject config backend`.
  - `config/` is the Django settings package (settings, urls, asgi, wsgi).
  - `apps/` directory created as a Python package — all future Django apps (users, profiles, interests, etc.) go here.
- `requirements.txt` generated from the virtual environment. Pinned versions:
  - `django==5.2.14`
  - `djangorestframework==3.17.1`
  - `django-cors-headers==4.9.0`
  - `djangorestframework-simplejwt==5.5.1`
  - `channels==4.3.2` + `daphne==4.2.1`
  - `psycopg2-binary==2.9.12`
  - `boto3==1.43.14` + `django-storages==1.14.6`
  - `python-decouple==3.8`
  - `Pillow==12.2.0`

**`config/settings.py` — key configuration:**
- All secrets (`SECRET_KEY`, `DB_PASSWORD`, AWS keys, Razorpay keys) read from `.env` via `python-decouple`. The app will not start without a valid `.env` file.
- `TIME_ZONE` set to `Asia/Kolkata` (not UTC) — important for correct timestamp display for Indian users.
- `INSTALLED_APPS` includes `rest_framework`, `corsheaders`, `channels`, `storages`. Local apps (`apps.users`, etc.) are commented out as stubs — uncomment each one as we build it.
- `DATABASES` configured for PostgreSQL. The app is not yet connected to a running PostgreSQL instance — user must install PostgreSQL first and set `DB_PASSWORD` in `.env`.
- `CHANNEL_LAYERS` uses `InMemoryChannelLayer` for local development. Must be switched to `channels_redis` with a Redis URL before deploying to production.
- `CORS_ALLOWED_ORIGINS` whitelists `http://localhost:5173` (the Vite dev server URL).
- `REST_FRAMEWORK` defaults all endpoints to `IsAuthenticated` with JWT authentication.

**`config/asgi.py` — WebSocket routing:**
- Replaced the default single-app ASGI setup with Django Channels' `ProtocolTypeRouter`.
- HTTP requests go to the standard Django ASGI app.
- WebSocket connections go through `AuthMiddlewareStack` → `URLRouter`. The URL list is empty for now — chat WebSocket routes will be added in Phase 5.

**`backend/.env` (local only, not in GitHub):**
- Template created with all required keys. User must fill in:
  - `DB_PASSWORD` — set when PostgreSQL is installed
  - `SECRET_KEY` — must be changed to a long random string before deploying
  - AWS keys — when AWS is configured
  - Razorpay keys — when payment integration begins

**Lambda (`lambda/handler.py`):**
- Fully written Lambda function (not deployed yet — deployment happens when AWS is configured).
- Triggered by S3 `ObjectCreated` events on the `matrimony-raw-uploads` bucket.
- Flow: fetch raw image → call Rekognition `DetectModerationLabels` at 75% confidence →
  - If flagged: copy to `quarantine/` prefix in raw bucket, log, return without publishing.
  - If clean: resize to 800×800 with `LANCZOS` resampling, convert to WebP at quality 85, upload to `matrimony-public-profiles` bucket.
- Uses `Pillow` for image processing, `boto3` for S3 and Rekognition calls.

---

### Commit 4 — `9ad3368` — Phase 2: all Django models, app structure, and Pyright config
**Date:** 2026-05-26

**What was done:**
- 5 Django apps created inside `backend/apps/`: `users`, `profiles`, `interests`, `conversations`, `subscriptions`.
- Custom `User` model with UUID primary key, `phone_number` as `USERNAME_FIELD` (OTP-first login).
- `AUTH_USER_MODEL = 'users.User'` set in `settings.py` — critical: must be set before the first migration ever runs.
- `django.contrib.postgres` added to `INSTALLED_APPS` — required for GIN index support.
- `pyrightconfig.json` added to suppress VSCode false-positive errors for `python-decouple` missing type stubs.

**Models written:**
- `Profile` — all 30+ demographic columns from the schema (religion, caste, horoscope, education, family, lifestyle, location, privacy).
- `PartnerPreferences` — `acceptable_religions` and `acceptable_castes` as `JSONField` with GIN indexes.
- Composite index on `profiles(religion, caste, gender)` for search query performance.
- `Interest` — `unique_together = (sender, receiver)` prevents duplicate requests at the DB level.
- `Conversation` — `OneToOneField → Interest` enforces accepted-only chat at the DB level.
- `Message.created_at` and `Conversation.last_message_at` — `db_index=True`.
- `UserSubscription.expires_at` — `db_index=True` for the daily cron downgrade job.

---

### Commit 5 — `9c65962` — Phase 2 complete: add database migrations
**Date:** 2026-05-26

**What was done:**
- PostgreSQL 18 installed on Windows. `matrimony` database created.
- `DB_PASSWORD` set in `backend/.env` (local only, never committed).
- `python manage.py makemigrations` generated 10 migration files across all 5 apps.
- `python manage.py migrate` applied all migrations successfully.

**All 20 tables confirmed in PostgreSQL:**
`users`, `profiles`, `partner_preferences`, `castes`, `religions`, `interests`, `conversations`, `messages`, `profile_views`, `subscription_plans`, `user_subscriptions`, plus Django internals (`auth_*`, `django_*`).

**PostgreSQL path note:**
- PostgreSQL 18 installed at `C:\Program Files\PostgreSQL\18\bin\`.
- PATH was updated via `[System.Environment]::SetEnvironmentVariable(...)` — takes effect in new PowerShell windows.
- Until a new terminal is opened, use the full path: `& "C:\Program Files\PostgreSQL\18\bin\psql.exe"`.

---

## Phase Status

| Phase | Description | Status |
|---|---|---|
| 1 | Infrastructure setup | Complete |
| 2 | Database migrations & models | Complete |
| 3 | 6-step registration (full-stack) | In progress |
| 4 | Dashboard, search, profile view | Not started |
| 5 | Chat, monetization, admin panel | Not started |

## Next Up — Phase 3: 6-Step Registration

1. Build Pinia `registrationStore` with all fields + `sessionStorage` persistence
2. Build Step 1–6 registration UI in Vue
3. Build `POST /api/auth/register` endpoint in Django
4. Build `POST /api/auth/login` (OTP initiation) and `POST /api/auth/verify-otp`
5. Implement OTP SMS provider (MSG91 recommended for India)
6. Implement email verification flow
7. Profile completeness scoring function + `GET /api/profile/completeness` endpoint
