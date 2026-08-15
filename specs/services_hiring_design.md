# Feature: Services and Hiring

## Requirements

- While a visitor is browsing the site, when they choose Services, the system shall show all six active services.
- While a visitor is viewing a service, when they open its page, the system shall show its hero, descriptions, benefits, process items, gallery and contact action.
- While an administrator is authenticated, when they edit service content, the system shall persist it through Django admin.
- While a visitor is on the hiring page, when they submit valid applicant data, the system shall store one private hiring request and show a success message.
- While a hiring request is invalid, automated or rate-limited, the system shall preserve safe form input and show actionable errors without storing a request.

## Architecture

### Frontend

- Responsive service index and detail templates using the existing Lahzeh, navy, yellow and gray design language.
- Shared service cards, image gallery selector, feature/process cards and contact call to action.
- Hiring page based on the contact-page composition with visible labels, inline errors, success feedback and mobile-first layout.
- Existing desktop/mobile navbar, footer and home service links point to real routes.

### Backend

- `Service`, `ServiceItem` and `ServiceGalleryImage` models with indexed active ordering and admin inlines.
- `HiringRequest` model and validated `HiringRequestForm`.
- Public list/detail service views with prefetched related content.
- Public hiring create view with PRG redirect and Django messages.
- A data migration seeds six services and representative service items.

### Security

- Django admin authentication protects all service editing and hiring-request review.
- Public forms use CSRF protection and server-side ModelForm validation.
- Resume uploads accept only PDF/DOC/DOCX files up to 5 MB.
- A honeypot rejects common automated submissions.
- Cache-based request throttling limits repeated POST attempts by client IP.
- Templates rely on Django escaping; applicant data is never returned publicly.
- Security events are logged without including applicant message or resume content.

## Implementation Plan

- [x] Define architecture and security controls.
- [x] Add models, forms, admin and migrations.
- [x] Add service and hiring views/routes.
- [x] Build responsive templates and shared service card.
- [x] Connect navbar, footer, home and team links.
- [x] Run migrations and Django system checks (no test suite per user request).
