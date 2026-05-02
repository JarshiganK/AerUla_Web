# AerUla Updated PRD Report

## Web-Based Cultural Simulation, Roles, Marketplace, and Django MVP Stack

**Prepared for:** AerUla Project Planning  
**Date:** May 2026  
**Document Type:** Product Requirements Document (Updated PRD)  
**Product:** AerUla Web Platform / AerUla Virtual Village

---

## Updated Product Direction

Build AerUla as a browser-based **Virtual Village platform** using:

- **Python Django** for backend, authentication, roles, admin, business logic, bookings, marketplace, and progress tracking.
- **Bootstrap** for responsive and user-friendly UI.
- **PostgreSQL** for structured database storage.
- **JavaScript + SVG/Canvas** for the MVP simulation layer.

The MVP includes login, multiple roles, 2D clickable huts, mini simulations, badges, a cultural passport, booking, and a marketplace path for traditional products.

Advanced 3D, VR, and AR are kept as future expansion stages.

---

## Document Control

| Item | Details |
|---|---|
| Product | AerUla Web Platform / AerUla Virtual Village |
| Document Type | Product Requirements Document (Updated PRD) |
| Updated Decision | Use Python Django, Bootstrap, PostgreSQL, and JavaScript/SVG/Canvas for the MVP. |
| Primary Goal | Create a user-friendly, role-based cultural simulation platform that guides users from virtual cultural discovery to marketplace purchase. |
| MVP Direction | Browser-based 2D cultural village with clickable huts, mini simulations, badges, cultural passport, booking, and marketplace. |
| Target Users | Tourists, students, Sri Lankan diaspora, local hosts/artisans, admins, tourism partners, and education partners. |

---

## Table of Contents

- [AerUla Updated PRD Report](#aerula-updated-prd-report)
  - [Web-Based Cultural Simulation, Roles, Marketplace, and Django MVP Stack](#web-based-cultural-simulation-roles-marketplace-and-django-mvp-stack)
  - [Updated Product Direction](#updated-product-direction)
  - [Document Control](#document-control)
  - [Table of Contents](#table-of-contents)
- [1. Executive Summary](#1-executive-summary)
- [2. Product Vision and Objectives](#2-product-vision-and-objectives)
  - [Product Vision](#product-vision)
  - [Main Objectives](#main-objectives)
- [3. Problem Statement](#3-problem-statement)
- [4. Proposed Solution](#4-proposed-solution)
  - [Solution Components](#solution-components)
- [5. Target Users and Roles](#5-target-users-and-roles)
- [6. Core User Journey](#6-core-user-journey)
  - [Tourist / Learner Flow](#tourist--learner-flow)
- [7. Core Pages and Modules](#7-core-pages-and-modules)
- [8. Updated Technology and Simulation Architecture](#8-updated-technology-and-simulation-architecture)
  - [Selected Stack](#selected-stack)
  - [Simulation Responsibility Split](#simulation-responsibility-split)
- [9. Simulation Requirements](#9-simulation-requirements)
  - [Simulation Acceptance Criteria](#simulation-acceptance-criteria)
- [10. Functional Requirements](#10-functional-requirements)
- [11. Non-Functional Requirements](#11-non-functional-requirements)
- [12. MVP Scope](#12-mvp-scope)
  - [MVP Must-Have Features](#mvp-must-have-features)
  - [Out of Scope for MVP](#out-of-scope-for-mvp)
- [13. Data Model Overview](#13-data-model-overview)
- [14. Development Roadmap](#14-development-roadmap)
- [15. Risks, Mitigation, and Conclusion](#15-risks-mitigation-and-conclusion)
  - [Risks and Mitigation](#risks-and-mitigation)
  - [Conclusion](#conclusion)
  - [Final Product Path](#final-product-path)
- [Appendix A: Django App Structure](#appendix-a-django-app-structure)
- [Appendix B: Future Enhancement Backlog](#appendix-b-future-enhancement-backlog)

---

# 1. Executive Summary

AerUla is being updated into a **software-first cultural tourism product**. The platform will not only list tourism experiences; it will also let users enter a browser-based virtual village, interact with cultural huts, complete mini simulations, earn badges, build a digital cultural passport, book real experiences, and finally buy related traditional products through a marketplace.

The updated implementation direction is to use **Python Django, Bootstrap, PostgreSQL, and JavaScript/SVG/Canvas**.

Django will handle:

- Authentication
- User roles
- Dashboards
- Admin workflows
- Bookings
- Marketplace logic
- Content management
- Progress tracking

Bootstrap will support a clean responsive UI. PostgreSQL will store users, huts, experiences, progress, badges, bookings, products, and orders. JavaScript with SVG/Canvas will handle the actual interactive simulation layer.

> **PRD Decision:** The MVP should use a 2D web simulation approach first. Advanced 3D, VR, AR, and game-engine style movement are future stages, not MVP requirements.

---

# 2. Product Vision and Objectives

## Product Vision

To become a trusted digital gateway where global users can experience Sri Lankan traditional village life through interactive learning, then convert that interest into bookings and marketplace purchases.

## Main Objectives

- Create a user-friendly web platform with login, home page, role-based dashboards, and guided navigation.
- Build a 2D Virtual Village map where each hut represents a cultural experience.
- Provide mini simulations such as arranging pottery steps, selecting cooking ingredients, matching fishing tools, and creating simple palmyrah patterns.
- Track progress using simulation completion, badges, and a digital cultural passport.
- Connect the learning journey to real bookings and a marketplace for traditional products.
- Keep the MVP realistic by using Django, Bootstrap, PostgreSQL, and JavaScript before moving into advanced 3D/VR/AR.

---

# 3. Problem Statement

Tourists, students, and diaspora communities often want to understand authentic Sri Lankan culture, but many available tourism platforms focus mainly on transport, hotels, or surface-level sightseeing. They rarely provide a structured, interactive way to understand traditional village life before visiting.

Local artisans, cooks, farmers, fishermen, musicians, and storytellers also need a digital channel to show their knowledge, receive bookings, and sell cultural products. Without a structured platform, their visibility and income opportunities remain limited.

The platform must therefore solve three problems at once:

1. **Cultural discovery**
2. **Interactive learning**
3. **Marketplace conversion**

---

# 4. Proposed Solution

AerUla will be developed as a **role-based web platform and cultural simulation system**.

Users enter through a normal website, login/register if needed, explore a 2D village map, interact with digital huts, complete learning activities, book real or future experiences, and finally reach a marketplace for related cultural products.

## Solution Components

| Component | Purpose | MVP Priority |
|---|---|---|
| Public Website | Explain AerUla, cultural mission, featured huts, community impact, and marketplace value. | High |
| Authentication and Roles | Support tourist, host, admin, and super admin paths. | High |
| Virtual Village Map | 2D illustrated map with clickable huts. | High |
| Hut Experience Pages | Story, media, mini simulation, badge, and product suggestions. | High |
| Simulation Activities | Small browser interactions handled by JavaScript/SVG/Canvas. | High |
| Cultural Passport | Track completed huts, scores, badges, and certificates. | High |
| Booking Module | Allow users to reserve real/future cultural experiences. | Medium |
| Marketplace | Sell products related to each hut or host. | High |
| Admin Dashboard | Manage users, huts, products, bookings, and approvals. | High |

---

# 5. Target Users and Roles

AerUla requires multiple roles because users, hosts, and admins interact with different parts of the product. Role-based access improves security and keeps each dashboard simple.

| Role | Main Need | Key Permissions |
|---|---|---|
| Guest User | Understand AerUla before registration. | View home page, preview huts, browse public marketplace items, register/login. |
| Tourist / Learner | Explore culture, complete simulations, book experiences, and buy products. | Use virtual village, complete simulations, earn badges, manage bookings, use cart and orders. |
| Local Host / Artisan | Publish experiences and sell products. | Create/edit listings, add products, manage availability, view bookings and earnings. |
| Admin | Manage daily operations and content quality. | Approve hosts, huts, products, bookings, reviews, and reports. |
| Super Admin | Control platform settings. | Manage admins, permissions, commission rates, audit logs, and system settings. |

---

# 6. Core User Journey

The primary user journey should be designed as a guided path from cultural curiosity to marketplace conversion.

```text
Home -> Enter Virtual Village -> Click Hut -> Simulation -> Badge / Passport -> Marketplace
```

## Tourist / Learner Flow

1. User opens the home page and understands the AerUla concept.
2. User selects **Enter Virtual Village** and sees a 2D illustrated Jaffna village map.
3. User clicks a hut such as Pottery, Palmyrah Craft, Cooking, Fishing Life, or Folk Music.
4. User reads the story, views images/audio/video, and completes the mini simulation.
5. System saves progress, unlocks a badge, and updates the digital cultural passport.
6. System recommends related bookings and marketplace products linked to that hut.

---

# 7. Core Pages and Modules

| Page / Module | Main Content | Primary Action |
|---|---|---|
| Home Page | Hero section, AerUla mission, featured huts, how it works, community impact, marketplace preview. | Enter Virtual Village / Register |
| Login Page | Email, password, forgot password, role-based routing after login. | Login |
| Register Page | Tourist registration and host application path. | Create Account |
| Tourist Dashboard | Recommended huts, progress, badges, bookings, saved products. | Continue Journey |
| Virtual Village Map | 2D map with clickable huts and progress indicators. | Open Hut |
| Hut Experience Page | Story, media, simulation, badge, marketplace suggestions. | Complete Hut |
| Cultural Passport | Completed huts, scores, badges, certificate status. | Share / Download later |
| Marketplace | Products linked to huts and hosts. | Add to Cart |
| Host Dashboard | Experience/product listing, bookings, earnings, availability. | Manage Listings |
| Admin Dashboard | Approvals, content, users, analytics, reports. | Approve / Manage |

---

# 8. Updated Technology and Simulation Architecture

The updated MVP stack is intentionally simple and realistic. Django will be the central application framework. Bootstrap will be used for fast responsive UI development. PostgreSQL will be the relational database. JavaScript with SVG/Canvas will be used for browser-side simulation interactions.

## Selected Stack

| Layer | Selected Technology | Responsibility |
|---|---|---|
| Backend | Python Django | Authentication, roles, routing, business logic, admin dashboard, bookings, orders, progress tracking. |
| Frontend UI | Django Templates + Bootstrap | Home page, forms, dashboards, cards, tables, marketplace screens, responsive layout. |
| Database | PostgreSQL | Users, roles, huts, stories, badges, progress, bookings, products, carts, orders, reviews. |
| Database Admin | psql / pgAdmin | Local database inspection, backups, migrations support, testing queries. |
| Simulation Layer | JavaScript + SVG/Canvas | Clickable village map, drag-and-drop, tile selection, matching activities, mini games. |
| Media | Django media storage initially | Images, hut illustrations, audio clips, product images, badge images. |
| Admin | Django Admin + Custom Admin Pages | Fast content management for huts, products, bookings, and approvals. |
| Future 3D | Three.js / Unity WebGL later | Advanced 3D village, VR/AR, animated walkthroughs after MVP validation. |

## Simulation Responsibility Split

| Task | Handled By |
|---|---|
| Store hut data, story text, and media paths | Django + PostgreSQL |
| Render pages, forms, cards, dashboards, and marketplace | Django Templates + Bootstrap |
| Run drag-and-drop, matching, tile selection, and clickable map interactions | JavaScript + SVG/Canvas |
| Validate simulation completion and save progress | Django backend + PostgreSQL |
| Unlock badges and update cultural passport | Django business logic + PostgreSQL |

---

# 9. Simulation Requirements

The MVP simulation should be lightweight, browser-friendly, and educational. It should not require installing apps, VR devices, or high-end graphics hardware.

| Hut | MVP Simulation Activity | Implementation Method | Saved Result |
|---|---|---|---|
| Pottery Hut | Arrange pottery-making steps in the correct order. | JavaScript drag-and-drop cards. | Score, completion, badge. |
| Palmyrah Craft Hut | Create a simple weaving pattern using clickable tiles. | JavaScript grid with CSS/SVG tiles. | Pattern completed, score. |
| Cooking Hut | Select correct ingredients for a traditional Jaffna dish. | Ingredient cards with checkbox/tile selection. | Correct ingredients, completion score. |
| Fishing Life Hut | Match fishing tools with their purpose. | Drag-and-match or dropdown matching. | Matching score, completion. |
| Folk Music Hut | Listen to a sound and identify the instrument or rhythm. | HTML audio + interactive choices. | Completion score, badge. |

## Simulation Acceptance Criteria

- Each hut must include a story section, media section, one mini simulation, and one badge.
- A logged-in user must be able to save progress after completing a hut.
- A guest user may preview a hut, but full progress tracking requires login.
- The virtual village map must visually show locked, available, and completed huts.
- The simulation must work on desktop and mobile browsers without extra installation.

---

# 10. Functional Requirements

| ID | Requirement | Description | Priority |
|---|---|---|---|
| FR-01 | Authentication | Users must register, login, logout, and reset passwords using Django authentication. | Must |
| FR-02 | Role-Based Access | Tourist, host, admin, and super admin users must access only permitted pages. | Must |
| FR-03 | Virtual Village Map | Users must view a 2D map and click huts to open experiences. | Must |
| FR-04 | Hut Experience | Each hut must show story, media, activity, badge, and product recommendations. | Must |
| FR-05 | Mini Simulation | Each hut must include one JavaScript-based simulation activity. | Must |
| FR-06 | Simulation Completion | System must validate simulation progress and completion scores. | Must |
| FR-07 | Progress Tracking | System must save hut completion, simulation score, badge status, and completion time. | Must |
| FR-08 | Cultural Passport | Users must view completed huts, badges, and total progress. | Must |
| FR-09 | Host Onboarding | Hosts must apply and be approved before publishing experiences or products. | Must |
| FR-10 | Booking | Tourists must be able to book listed cultural experiences. | Should |
| FR-11 | Marketplace | Users must browse products, view details, add to cart, and place orders. | Must |
| FR-12 | Admin Approval | Admins must approve hosts, huts, experiences, products, and reviews. | Must |
| FR-13 | Content Management | Admins must manage hut content, stories, media, and badges. | Must |
| FR-14 | Analytics | Admin dashboard should show users, hut completions, bookings, orders, and revenue indicators. | Should |

---

# 11. Non-Functional Requirements

| Area | Requirement |
|---|---|
| Usability | The interface must be simple for tourists and local hosts, with clear buttons, guided steps, and visual cues. |
| Mobile Responsiveness | All pages and 2D simulations must work on phones, tablets, and desktops. |
| Performance | 2D simulations must load quickly; images and audio should be compressed for web use. |
| Security | Passwords must be hashed, routes protected by role permissions, and inputs validated. |
| Reliability | Progress, cart, bookings, and orders must not be lost unexpectedly. |
| Maintainability | Django apps should be separated by module: accounts, village, simulations, bookings, marketplace, dashboard. |
| Scalability | The system must allow new huts, villages, languages, hosts, products, and future 3D modules. |
| Accessibility | Use readable contrast, alt text, keyboard-friendly forms, and clear labels. |
| Cultural Accuracy | Content should be reviewed by local experts, elders, artisans, teachers, or researchers. |

---

# 12. MVP Scope

The MVP should prove that users are interested in interactive cultural simulation before investing in advanced 3D, VR, AR, or a physical heritage village.

## MVP Must-Have Features

- Professional landing page explaining AerUla and the Virtual Village concept.
- User registration/login with tourist, host, admin, and super admin roles.
- 2D illustrated virtual village map with five clickable Jaffna-based huts.
- Five hut pages:
  - Pottery
  - Palmyrah Craft
  - Northern Cooking
  - Fishing Life
  - Folk Music
- One mini simulation per hut.
- Badge unlocking and digital cultural passport progress tracking.
- Basic Django admin/custom admin dashboard for hut, badge, product, and user management.
- Marketplace listing, product details, cart, and basic order placement.
- Responsive Bootstrap UI for desktop, tablet, and mobile.

## Out of Scope for MVP

- Full 3D village walkthrough.
- VR/AR experiences.
- Advanced AI guide chatbot.
- Native mobile apps.
- Complex host wallet and payout automation.
- Real-time multiplayer or live 3D avatars.

---

# 13. Data Model Overview

| Entity | Important Fields | Purpose |
|---|---|---|
| User | id, name, email, password, role, status, created_at | Accounts and role-based routing. |
| HostProfile | user, phone, location, verification_status, bio | Host onboarding and verification. |
| Hut | title, category, region, image, status, display_order | Clickable village locations. |
| ExperienceContent | hut, story_text, media_url, simulation_type, content_json | Story and simulation configuration. |
| UserProgress | user, hut, completed, score, completed_at | Progress tracking and passport. |
| Badge | hut, title, description, image | Reward system. |
| ExperienceBooking | user, host, hut/experience, date, time, participants, status | Real/future booking path. |
| Product | host, hut, title, price, stock, image, status | Marketplace items linked to cultural huts. |
| Order | user, total, status, created_at, delivery_info | Marketplace checkout. |
| Review | user, target_type, target_id, rating, comment, status | Trust and quality. |

---

# 14. Development Roadmap

| Phase | Duration | Main Activities | Deliverables |
|---|---|---|---|
| 1. Planning | Week 1 | Finalize huts, user roles, content plan, database model, and page list. | PRD, wireframes, content plan. |
| 2. Django Setup | Week 2 | Create Django project, apps, auth, PostgreSQL connection, base templates, Bootstrap layout. | Working project skeleton. |
| 3. Core UI | Week 3 | Build home, login, register, dashboards, and virtual village map page. | Navigable frontend. |
| 4. Hut + Simulation | Weeks 4-5 | Build hut pages, mini simulations, progress saving, and badges. | Functional simulation flow. |
| 5. Marketplace + Booking | Week 6 | Build product listing, cart, order placement, simple booking path. | End-to-end product path. |
| 6. Admin | Week 7 | Configure Django admin/custom admin for content, hosts, products, and approvals. | Admin management system. |
| 7. Testing + Deploy | Week 8 | Test roles, mobile responsiveness, simulation actions, database states, and deployment. | Demo-ready MVP. |

---

# 15. Risks, Mitigation, and Conclusion

## Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Simulation becomes too complex. | Start with 2D JavaScript/SVG/Canvas interactions only; postpone 3D and VR. |
| Users see it only as a game. | Use storytelling, cultural explanations, badges, and cultural passport framing. |
| Cultural content is inaccurate. | Validate content with local experts, elders, artisans, teachers, and researchers. |
| Marketplace feels disconnected. | Recommend products based on the hut completed or experience booked. |
| Hosts find the system difficult. | Use simple forms, admin support, and approval-based onboarding. |
| Performance issues on mobile. | Compress media, avoid heavy 3D in MVP, and use responsive Bootstrap components. |

## Conclusion

The updated PRD confirms that AerUla can be built realistically using **Django, Bootstrap, PostgreSQL, and JavaScript/SVG/Canvas**. This stack is enough for the MVP because the first version focuses on 2D web simulation, structured learning, role-based access, booking, and marketplace conversion.

## Final Product Path

```text
Home -> Login -> Virtual Village -> Hut Simulation -> Cultural Passport -> Marketplace
```

AerUla should begin as a clean, practical browser-based product. Once the team validates user interest, it can expand into 3D, VR, AR, AI cultural guides, tourism partnerships, and real-world cultural experiences.

---

# Appendix A: Django App Structure

| Django App | Responsibility |
|---|---|
| accounts | Custom user model, roles, login, registration, permissions, profiles. |
| village | Virtual village map, huts, hut content, media, categories. |
| simulations | Simulation configuration, scoring, progress, badges, cultural passport. |
| bookings | Experience availability, reservations, booking status, host booking view. |
| marketplace | Products, cart, orders, order status, product reviews. |
| dashboard | Tourist, host, admin, and super admin dashboards. |
| core | Home page, static pages, shared layout, settings, common utilities. |

---

# Appendix B: Future Enhancement Backlog

- 3D virtual village using Three.js or Unity WebGL.
- AI cultural guide chatbot with multilingual support.
- Tamil and Sinhala narration for each hut.
- Downloadable cultural passport certificate.
- School/education mode with teacher dashboard.
- Payment gateway integration and host payout wallet.
- Hotel and travel agency partner portal.
- Real-world booking integration with verified hosts.
- VR/AR cultural tours and museum digital objects.

---

**End of Updated PRD Report**
