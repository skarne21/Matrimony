# Matrimony Website — Full Project Plan

## Project Goal

Build a full-featured Indian matrimony platform that handles culturally sensitive data (religion, caste, horoscope, government ID), complies with India's DPDP Act, and monetizes via subscription tiers with a Razorpay payment gateway.

---

## Part 1: User Registration System

### Registration Fields

#### Step 1 — Basic Information
- First Name
- Last Name
- Gender (Male / Female / Other)
- Date of Birth / Age
- Marital Status (Never Married / Divorced / Widowed)
- Height / Weight
- Profile Created By (Self / Parent / Relative / Friend)

#### Step 2 — Contact Details
- Mobile Number (OTP Verification)
- Email Address
- Password / Confirm Password
- Current Address
- City / State / Country
- ZIP / Postal Code

#### Step 3 — Personal Details
- Religion
- Caste / Community
- Sub-caste
- Mother Tongue
- Horoscope / Nakshatra / Rashi (Optional)
- Manglik / Dosha Details (Optional)

#### Step 4 — Education & Career
- Highest Education
- College / University
- Occupation / Profession
- Company Name
- Annual Income / Salary
- Work Location

#### Step 5 — Family Details
- Father Name & Occupation
- Mother Name & Occupation
- Number of Brothers / Sisters
- Family Type (Joint / Nuclear)
- Family Status

#### Step 6 — Lifestyle Information
- Eating Habits (Veg / Non-Veg / Vegan)
- Smoking Habit (Yes / No / Occasionally)
- Drinking Habit (Occasionally / Regular / Daily / No)
- Hobbies / Interests

#### Step 7 — Partner Preferences
- Preferred Age Range
- Preferred Height
- Religion / Caste Preference
- Education Preference
- Profession Preference
- Preferred Country / Location

#### Step 8 — Profile & Verification
- Upload Profile Photo
- ID Proof Upload (Optional)
- Bio / About Me
- Privacy Settings
- Email / Mobile Verification

### Registration Flow

```
Step 1: Basic Details →
Step 2: Personal & Religion →
Step 3: Education & Career →
Step 4: Family Details →
Step 5: Partner Preferences →
Step 6: Upload Photos & Verification
```

### Pinia State Management for Registration

- Each step of the form populates a single Pinia store (`registrationStore`).
- On final submission, the full store payload is sent as one `POST /api/auth/register` request.
- This prevents partial data loss if the user refreshes mid-flow (store persists to `sessionStorage`).

---

## Part 2: Core Feature Modules

### Module 1 — User Dashboard & Recommendation Feed

#### Live SQL Filtering Feed
- Replaces nightly ML-generated batch processing.
- When a user opens the dashboard, the backend fires a fast PostgreSQL query using fields from their `partner_preferences` row.
- Query uses basic relational operations to match profiles across `profiles`, `education`, `lifestyle`, and `partner_preferences` tables.
- Filter logic: `religion_id` match, `caste_id` overlap (JSONB), age within `age_min/age_max`, height within `height_min/height_max`.

#### Activity Triggers & WebSocket State
- Pinia holds notification counters globally (new interests received, new messages, profile views).
- When a WebSocket event fires (e.g., `interest.received`), the Pinia store updates the counter instantly — no page refresh required.
- WebSocket connection opens on dashboard load and stays alive for the session.

#### Profile Completeness Logic
- Backend helper function assigns a weighted integer score to each filled database column.
  - Example weights: `bio` = 15 pts, `profile_pic_url` = 20 pts, `annual_income` = 5 pts, `dob` = 10 pts, etc.
- A dedicated API endpoint (`GET /api/profile/completeness`) returns the aggregate score (0–100).
- The frontend uses this score to render a UI progress bar nudging users to fill missing fields.

---

### Module 2 — Search & Discovery Engine

#### Database Optimization
- PostgreSQL is mandatory.
- **GIN (Generalized Inverted Index)** indexing on JSONB columns (`acceptable_religions`, `acceptable_castes`) in `partner_preferences`.
- **Composite index** on `(religion_id, caste_id, gender)` in `profiles` — search queries always filter on multiple of these columns simultaneously.

#### Dynamic Query Builder (Backend)
- Build a query builder on the backend that dynamically constructs the `WHERE` clause.
- If a search field is left blank by the user, that clause is **omitted entirely** — do not filter by it.
- This prevents slow queries caused by filtering on `NULL` or empty values.
- Supports filters: age range, height range, religion, caste, education, income, profession, location, marital status, lifestyle habits.

#### Pagination Strategy
- **Basic / dashboard feed**: Infinite scroll (keeps users engaged).
- **Advanced search results**: Strict **cursor-based pagination** — users must not lose their page position when clicking into a profile and pressing "back".

---

### Module 3 — Detailed Profile View (Bio Page)

#### Component Architecture (Vue 3)
Break the profile page into smaller lazy-loaded components:
- `<ProfileHeader />` — avatar, name, age, location, height, caste/religion
- `<EducationCareer />` — education, occupation, income
- `<FamilyDetails />` — family structure and background
- `<LifestyleInfo />` — eating, smoking, drinking habits, hobbies
- `<AstroDetails />` — horoscope, nakshatra, rashi, manglik status (lazy loaded — many users skip this)
- `<PartnerPreferences />` — what they are looking for
- `<ActionTray />` — Send Interest / Chat / Request Photo / Block buttons

#### Gated Content Logic (Action Tray)
- Before rendering the photo gallery, the API checks:
  1. The **viewing user's subscription tier**.
  2. The **target user's `photo_privacy` setting**.
- If `photo_privacy === 'locked'`:
  - API returns a placeholder URL and a `canRequestPhoto: true` flag.
  - Frontend renders a "Request Photo Access" button instead of the photo.
- If `photo_privacy === 'public'` and viewer has a valid subscription:
  - API returns the actual CloudFront image URL.
- Phone number unlock:
  - Route `GET /api/users/{id}/phone` is behind premium middleware.
  - Checks `contact_views_used < contact_views_allowed`.
  - Increments `contact_views_used` in the same DB transaction as returning the phone number.

---

### Module 4 — Chat & Communication Hub

#### WebSocket Infrastructure
- Deploy a WebSocket server using one of:
  - **Laravel Reverb** (if using Laravel backend)
  - **Django Channels** (if using Django backend)
  - **Dedicated Node.js microservice** (framework-agnostic option)
- Handles bidirectional, real-time data flow.

#### Message Flow
1. User A sends a message → payload goes over WebSocket.
2. Backend saves the message to the `messages` table in PostgreSQL.
3. Message is immediately broadcast to User B's active WebSocket connection.
4. `is_read` flag on the message updates to `true` once User B opens the conversation.
5. `last_message_at` on the `conversations` row updates — used to sort the inbox by most recent activity.

#### Access Control Rule
- A conversation can only exist if a corresponding `interests` row has `status = 'accepted'`.
- The `conversations` table enforces this via a foreign key to the `interests` table.
- The backend must reject any attempt to open a chat if the interest is not accepted — enforced at the DB level, not just the API level.

---

### Module 5 — Monetization & Premium Gateway

#### Subscription Plans (Examples)
| Plan | Price | Duration | Contact Views | Initiate Chat |
|---|---|---|---|---|
| Free | ₹0 | — | 0 | No |
| Silver | ₹499 | 30 days | 10 | No |
| Gold | ₹999 | 90 days | 30 | Yes |
| Platinum | ₹1,999 | 180 days | Unlimited | Yes |

#### Middleware Protection
- Every API route that involves a premium feature must be wrapped in a strict middleware/decorator:
  - `POST /api/messages/initiate`
  - `GET /api/users/{id}/phone`
  - Any route that returns gated profile content
- Middleware checks `user_subscriptions` for:
  1. A row with `user_id` matching the requester.
  2. `expires_at > NOW()` (plan is active).
  3. The specific feature flag required (e.g., `can_initiate_chat = true`).

#### Payment Gateway (Razorpay / Stripe)
- **Never trust the frontend to confirm a payment.**
- Backend exposes a secure webhook endpoint.
- Listens for:
  - Razorpay: `payment.captured` event
  - Stripe: `payment_intent.succeeded` event
- On successful webhook:
  1. Look up the pending order/session.
  2. Insert a row into `user_subscriptions` with `starts_at = now()` and `expires_at = now() + duration_days`.
  3. Return 200 to the payment provider.

#### Profile Booster (Microtransaction)
- "Boost Profile" deducts credits in a **database transaction**.
- Prevents race conditions where a user double-clicks "Boost" and goes into negative credit balance.
- Pattern: `SELECT FOR UPDATE` on the credits row, deduct, commit — all in one transaction.

---

### Module 6 — Admin Panel & Moderation Engine

#### AWS Image Pipeline (Auto-Approve)

**Step 1 — Direct-to-S3 Upload (Presigned URLs)**
- User wants to upload a photo → Vue.js frontend calls `POST /api/upload/presigned-url`.
- Backend generates a temporary, signed S3 URL pointing to the `raw-uploads` bucket.
- Frontend uploads the image **directly to S3** — the backend never handles the file bytes.
- This eliminates backend bandwidth and compute costs for file transfers.

**Step 2 — Serverless Compression (AWS Lambda)**
- S3 `raw-uploads` bucket triggers a Lambda function on every new object upload.
- Lambda:
  1. Fetches the raw image from S3.
  2. Resizes it to **800×800 pixels**.
  3. Converts it to **WebP format** (highly compressed).
  4. Simultaneously sends the image to **AWS Rekognition**.

**Step 3 — Automated Safety Check (AWS Rekognition)**
- Lambda calls `DetectModerationLabels` on the image.
- If Rekognition detects **explicit, suggestive, or violent content**:
  - Routes the photo to the **"Quarantine Queue"** (a separate S3 prefix or SQS queue).
  - Marks the image as `hidden` in the database.
  - Flags it for moderator review.
- If the photo is **clean**:
  - Lambda moves the compressed WebP to the **`public-profiles`** S3 bucket.
  - Updates the database record with the new `profile_pic_url` (CloudFront URL).
  - Photo goes **live instantly** — no human approval needed for clean images.
- **Cost**: Rekognition costs ~$0.001 per image — significantly cheaper than human-only moderation at scale.

#### Moderator Workflow (Second Line of Defense)

**Flagged Queue** (replaces old "Approval Queue")
- Photos land in the Flagged Queue via two paths:
  1. **User Reports** — a user clicked "Report Photo" on a profile.
  2. **AI Flags** — Rekognition flagged the image as borderline or violating.

**"One-Click Nuke" Button**
- Moderator dashboard shows a grid of flagged photos.
- Single action button: **"Delete & Warn"**
- Clicking this triggers one atomic backend operation:
  1. Deletes the object from the S3 `public-profiles` bucket.
  2. Removes the database record reference (`profile_pic_url` set to null).
  3. Drops the user's "Profile Completeness" score.
  4. Sends an automated warning email to the user's registered email address.

#### AWS Cost Minimization

| Tactic | Detail |
|---|---|
| CloudFront CDN | All images served through CloudFront, never directly from S3. CloudFront data transfer is significantly cheaper than S3 outbound. |
| S3 Lifecycle Policy | `raw-uploads` bucket auto-deletes original uncompressed files after **24 hours**. Only compressed WebP versions are retained. |
| Browser Cache Headers | CloudFront configured to force browsers to cache profile photos for **30 days minimum**. Repeat views cost nothing. |
| Upload Size Limit | Strict **5 MB** file size cap enforced on the frontend. Prevents users from uploading massive raw files and running up the AWS bill. |

---

## Part 3: Database Schema (Complete)

### Core User & Profile Tables

#### `users`
| Column | Type | Details |
|---|---|---|
| id | UUID | PK — prevents sequential ID scraping |
| email | String | Unique index |
| password_hash | String | bcrypt/Argon2 hashed |
| phone_number | String | Unique index, OTP login |
| account_status | Enum | active, suspended, deleted, pending_approval |

#### `profiles`
| Column | Type | Details |
|---|---|---|
| user_id | UUID | FK → users. Unique (1-to-1) |
| first_name | String | |
| last_name | String | |
| gender | Enum | male, female, other |
| dob | Date | Storing DOB allows dynamic age calculation |
| marital_status | Enum | never_married, divorced, widowed |
| height_cm | Integer | Stored in cm for consistent filtering |
| weight_kg | Integer | |
| profile_created_by | Enum | self, parent, relative, friend |
| mother_tongue | String | |
| religion_id | Integer | FK → religions lookup table |
| caste_id | Integer | FK → castes lookup table |
| sub_caste | String | |
| nakshatra | String | Horoscope — optional |
| rashi | String | Horoscope — optional |
| is_manglik | Boolean | Optional |
| education_level | String | |
| college | String | |
| occupation | String | |
| company | String | |
| annual_income | Integer | Numeric for range filtering (e.g., > 500000) |
| work_location | String | |
| father_name | String | |
| father_occupation | String | |
| mother_name | String | |
| mother_occupation | String | |
| brothers_count | Integer | |
| sisters_count | Integer | |
| family_type | Enum | joint, nuclear |
| family_status | String | |
| eating_habit | Enum | veg, non_veg, vegan |
| smoking_habit | Enum | yes, no, occasionally |
| drinking_habit | Enum | no, occasionally, regular, daily |
| hobbies | JSONB/Array | Array of hobby strings |
| bio | Text | About me — weighted 15 pts in completeness score |
| profile_pic_url | String | CloudFront URL |
| id_proof_url | String | S3 private URL — moderator access only |
| is_verified | Boolean | True after ID proof approval |
| photo_privacy | Enum | public, locked |
| city | String | |
| state | String | |
| country | String | |
| postal_code | String | |

#### `partner_preferences`
| Column | Type | Details |
|---|---|---|
| user_id | UUID | FK → users |
| age_min | Integer | |
| age_max | Integer | |
| height_min_cm | Integer | |
| height_max_cm | Integer | |
| acceptable_religions | JSONB/Array | Array of religion_ids |
| acceptable_castes | JSONB/Array | Array of caste_ids |
| preferred_education | String | |
| preferred_profession | String | |
| preferred_location | String | |

### Interaction & Matching Tables

#### `profile_views`
| Column | Type | Details |
|---|---|---|
| id | BigInt | PK |
| viewer_id | UUID | FK → users (the person looking) |
| viewed_id | UUID | FK → users (the profile being looked at) |
| viewed_at | Timestamp | Default: `now()` |

#### `interests`
| Column | Type | Details |
|---|---|---|
| id | BigInt | PK |
| sender_id | UUID | FK → users (initiator) |
| receiver_id | UUID | FK → users (recipient) |
| status | Enum | pending, accepted, declined, withdrawn |
| created_at | Timestamp | |

**Unique constraint:** `(sender_id, receiver_id)` — prevents interest spam.

### Communication Tables

#### `conversations`
| Column | Type | Details |
|---|---|---|
| id | UUID | PK |
| interest_id | BigInt | FK → interests (enforces accepted-only chat) |
| user_one_id | UUID | FK → users |
| user_two_id | UUID | FK → users |
| last_message_at | Timestamp | Sorts inbox by most recent activity |

#### `messages`
| Column | Type | Details |
|---|---|---|
| id | BigInt | PK |
| conversation_id | UUID | FK → conversations |
| sender_id | UUID | FK → users |
| content_text | Text | Message body |
| is_read | Boolean | True once recipient opens the chat |
| created_at | Timestamp | Indexed for chronological sorting |

### Monetization Tables

#### `subscription_plans`
| Column | Type | Details |
|---|---|---|
| id | Integer | PK |
| name | String | e.g., "Gold", "Platinum" |
| price | Decimal | Plan cost in INR |
| duration_days | Integer | 30, 90, or 180 |
| contact_views_allowed | Integer | Phone number unlock limit (-1 = unlimited) |
| can_initiate_chat | Boolean | Premium messaging toggle |

#### `user_subscriptions`
| Column | Type | Details |
|---|---|---|
| id | BigInt | PK |
| user_id | UUID | FK → users |
| plan_id | Integer | FK → subscription_plans |
| starts_at | Timestamp | Date the payment webhook confirmed |
| expires_at | Timestamp | Indexed — used by daily cron job |
| contact_views_used | Integer | Increments per phone number unlock |

### Lookup Tables

#### `religions`
| Column | Type |
|---|---|
| id | Integer PK |
| name | String |

#### `castes`
| Column | Type |
|---|---|
| id | Integer PK |
| religion_id | Integer FK → religions |
| name | String |

---

## Part 4: API Contract

| Method | Route | Description |
|---|---|---|
| POST | /api/auth/register | Submit full 6-step Pinia payload |
| POST | /api/auth/login | Send phone number to receive OTP |
| POST | /api/auth/verify-otp | Confirm OTP, receive auth token |
| POST | /api/auth/logout | Invalidate session/token |
| GET | /api/matches | Live SQL dashboard feed (partner prefs filter) |
| GET | /api/users/{id} | Full profile view |
| GET | /api/search | Advanced search with dynamic query builder |
| POST | /api/interests/{id} | Send connection request |
| PATCH | /api/interests/{id} | Accept / decline / withdraw interest |
| GET | /api/profile/me | Current user's own profile |
| PATCH | /api/profile/me | Update own profile fields |
| GET | /api/profile/completeness | Weighted completeness score (0–100) |
| GET | /api/profile/views | Who viewed my profile |
| GET | /api/conversations | Inbox — sorted by last_message_at |
| GET | /api/conversations/{id}/messages | Chat history (paginated) |
| POST | /api/conversations/{id}/messages | Send a message |
| GET | /api/users/{id}/phone | Unlock phone number (premium middleware) |
| POST | /api/upload/presigned-url | Get temporary S3 presigned URL |
| POST | /api/subscriptions/checkout | Initiate Razorpay/Stripe payment session |
| POST | /api/webhooks/payment | Payment provider webhook (provision plan) |
| POST | /api/users/{id}/report | Report a user or photo |
| GET | /api/admin/flagged-photos | Moderator flagged queue |
| DELETE | /api/admin/photos/{id} | Delete & Warn (atomic moderator action) |
| GET | /api/admin/users | Admin user management |
| PATCH | /api/admin/users/{id}/status | Suspend / unsuspend / approve account |

---

## Part 5: Data Privacy & Compliance

### India's DPDP Act Requirements
- The platform collects **sensitive personal data**: religion, caste, government ID proofs, precise location.
- All sensitive columns must be **encrypted at rest**.
- Users have the **right to erasure** — a "Delete My Account" feature must fully remove all personal data from all tables and S3 buckets.
- A **Privacy Policy** page must be presented and accepted during registration.
- **Data minimization** — only collect data that is necessary for the matching function.
- Logs must not capture raw PII (phone numbers, names) — use anonymized user IDs in logs.
- Government ID proofs (`id_proof_url`) must be stored in a **private S3 bucket** with no public access — access only via signed URLs, only for admins.

---

## Part 6: Sprint Milestones (MVP Order of Operations)

### Phase 1 — Infrastructure Setup
- [ ] Initialize Git repository
- [ ] Initialize Vue 3 project with Vite
- [ ] Initialize Laravel or Django backend project
- [ ] Connect PostgreSQL database (local dev + production config)
- [ ] Set up environment variable management (.env files)
- [ ] Create AWS S3 buckets: `raw-uploads`, `public-profiles`
- [ ] Set up CloudFront distribution pointing to `public-profiles` bucket
- [ ] Configure S3 Lifecycle Policy (auto-delete `raw-uploads` after 24 hours)
- [ ] Set up AWS Lambda function stub (will be fleshed out in Phase 4)
- [ ] Set up base project folder structure

### Phase 2 — Database Migrations & Models
- [ ] Migration: `religions` lookup table
- [ ] Migration: `castes` lookup table (with religion FK)
- [ ] Migration: `users` table
- [ ] Migration: `profiles` table (all demographic columns)
- [ ] Migration: `partner_preferences` table
- [ ] Migration: `profile_views` table
- [ ] Migration: `interests` table (with unique constraint)
- [ ] Migration: `conversations` table (with interests FK)
- [ ] Migration: `messages` table
- [ ] Migration: `subscription_plans` table (seed with initial plans)
- [ ] Migration: `user_subscriptions` table
- [ ] Add composite index on `profiles(religion_id, caste_id, gender)`
- [ ] Add GIN index on `partner_preferences(acceptable_religions)` and `(acceptable_castes)`
- [ ] Add index on `user_subscriptions(expires_at)`
- [ ] Add index on `messages(created_at)`
- [ ] Create all ORM models with relationships

### Phase 3 — 6-Step Registration (Full Stack)
- [ ] Build Pinia `registrationStore` with all fields, sessionStorage persistence
- [ ] Build Step 1 UI: Basic Details
- [ ] Build Step 2 UI: Personal & Religion (populate religion/caste from API)
- [ ] Build Step 3 UI: Education & Career
- [ ] Build Step 4 UI: Family Details
- [ ] Build Step 5 UI: Partner Preferences
- [ ] Build Step 6 UI: Photo Upload + Bio + Verification
  - [ ] Presigned URL fetch from backend
  - [ ] Direct S3 upload from Vue frontend
  - [ ] Show upload progress indicator
- [ ] Build `POST /api/auth/register` endpoint
- [ ] Build `POST /api/auth/login` (OTP initiation)
- [ ] Build `POST /api/auth/verify-otp` (token issuance)
- [ ] Implement OTP SMS provider (e.g., Twilio, MSG91)
- [ ] Implement email verification flow
- [ ] Profile completeness scoring function
- [ ] `GET /api/profile/completeness` endpoint

### Phase 4 — Dashboard, Search & Profile View
- [ ] Build Live SQL matching query (reads from partner_preferences)
- [ ] Build `GET /api/matches` endpoint
- [ ] Build Vue Dashboard page with infinite scroll feed
- [ ] Connect Pinia notification store to WebSocket events
- [ ] Build advanced search query builder backend
- [ ] Build `GET /api/search` endpoint
- [ ] Build Vue Search page with cursor-based pagination
- [ ] Build `<ProfileHeader />` component
- [ ] Build `<EducationCareer />` component
- [ ] Build `<FamilyDetails />` component
- [ ] Build `<AstroDetails />` component (lazy loaded)
- [ ] Build `<LifestyleInfo />` component
- [ ] Build `<PartnerPreferences />` component
- [ ] Build `<ActionTray />` component with gated content logic
- [ ] Build `POST /api/interests/{id}` endpoint
- [ ] Build `PATCH /api/interests/{id}` endpoint
- [ ] Build `GET /api/profile/views` endpoint
- [ ] Build AWS Lambda function: resize → WebP → Rekognition check → route to correct bucket
- [ ] Integrate Rekognition `DetectModerationLabels`
- [ ] Build quarantine queue handler

### Phase 5 — Chat, Monetization & Admin Panel
- [ ] Deploy WebSocket server (Laravel Reverb / Django Channels / Node.js)
- [ ] Build `GET /api/conversations` endpoint (inbox)
- [ ] Build `GET /api/conversations/{id}/messages` endpoint
- [ ] Build `POST /api/conversations/{id}/messages` endpoint
- [ ] Build Vue Chat UI with real-time WebSocket message rendering
- [ ] Build subscription plans seed data
- [ ] Build `POST /api/subscriptions/checkout` (create payment session)
- [ ] Build Razorpay webhook handler (`POST /api/webhooks/payment`)
- [ ] Implement subscription middleware for all premium routes
- [ ] Build `GET /api/users/{id}/phone` endpoint (premium gated)
- [ ] Build Profile Booster microtransaction with `SELECT FOR UPDATE` transaction
- [ ] Build Admin dashboard: flagged photo queue grid
- [ ] Build `GET /api/admin/flagged-photos` endpoint
- [ ] Build "Delete & Warn" handler (`DELETE /api/admin/photos/{id}`) — atomic operation
- [ ] Build admin user management panel
- [ ] Set up daily cron job to downgrade expired subscriptions
- [ ] Set up CloudFront cache headers (30-day browser cache for profile images)
- [ ] Enforce 5 MB upload limit on the Vue file input component
- [ ] Write Privacy Policy page
- [ ] Implement "Delete My Account" full data erasure flow (DPDP compliance)
