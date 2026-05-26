# Matrimony

A full-featured matrimony platform built for India. Designed to handle culturally sensitive matching criteria, real-time communication, subscription-based monetization, and compliance with India's Digital Personal Data Protection (DPDP) Act.

---

## Features

- **6-Step Registration** — Guided profile creation covering personal details, religion & caste, education & career, family background, lifestyle, and partner preferences
- **Smart Matching Feed** — Live SQL-powered recommendation feed filtered by partner preferences (age, height, religion, caste, location)
- **Advanced Search** — Dynamic multi-filter search with cursor-based pagination
- **Detailed Profile Pages** — Lazy-loaded profile sections with gated photo and contact access based on subscription tier
- **Real-Time Chat** — WebSocket-powered messaging, unlocked only after a mutual interest is accepted
- **Interest System** — Send, accept, decline, or withdraw connection requests
- **Subscription Plans** — Free, Silver, Gold, and Platinum tiers with contact view limits and chat access controls
- **Razorpay Payments** — Webhook-confirmed subscription provisioning
- **AWS Image Pipeline** — Direct-to-S3 uploads, serverless WebP compression via Lambda, and automated moderation via AWS Rekognition
- **Admin & Moderation Panel** — Flagged photo queue with one-click delete & warn actions
- **DPDP Compliance** — Data encryption at rest, right to erasure, privacy-first design

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vue 3, Vite, Pinia |
| Backend | Laravel (PHP) / Django (Python) |
| Database | PostgreSQL |
| Real-Time | WebSockets (Laravel Reverb / Django Channels) |
| File Storage | AWS S3 |
| CDN | AWS CloudFront |
| Image Processing | AWS Lambda + WebP compression |
| Image Moderation | AWS Rekognition |
| Payments | Razorpay |
| Authentication | OTP (SMS) + Email verification |

---

## Project Structure

```
Matrimony/
├── frontend/          # Vue 3 + Vite application
├── backend/           # Laravel or Django API server
├── lambda/            # AWS Lambda function for image processing
└── .gitignore
```

> Structure will be populated as each phase is built out.

---

## Development Phases

| Phase | Scope | Status |
|---|---|---|
| 1 | Infrastructure setup — Vue, backend, PostgreSQL, AWS | Pending |
| 2 | Database migrations and models | Pending |
| 3 | 6-step registration UI + API | Pending |
| 4 | Dashboard, search, and profile pages | Pending |
| 5 | Chat, monetization, and admin panel | Pending |

---

## Getting Started

> Setup instructions will be added as the project is scaffolded.

### Prerequisites

- Node.js 20+
- PHP 8.2+ (Laravel) or Python 3.11+ (Django)
- PostgreSQL 15+
- AWS account (S3, Lambda, CloudFront, Rekognition)
- Razorpay account

### Installation

```bash
# Clone the repository
git clone https://github.com/skarne21/Matrimony.git
cd Matrimony
```

Frontend and backend setup instructions will follow in Phase 1.

---

## License

This project is private and not licensed for public use.
