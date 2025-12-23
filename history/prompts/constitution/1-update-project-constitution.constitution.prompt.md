---
id: 1
title: Update-project-constitution
stage: constitution
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: exact
command: /sp.constitution
labels: [constitution,documentation,setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project: AI-Driven Book + RAG Chatbot on Physical AI & Humanoid Robotics
Tools: Spec-Kit Plus, Claude Code, Docusaurus, GitHub Pages, ROS 2, Gazebo, Unity, NVIDIA Isaac, FastAPI, Neon, Qdrant, OpenAI Agents/ChatKit

Core Principles:
- Technical accuracy from official docs and peer-reviewed robotics/AI sources
- Clear engineering-level writing (FK grade 11–13)
- Reproducible code and setup steps
- Book and chatbot must use the same knowledge base

Standards:
- All claims must be source-verified
- Sources: official documentation + academic robotics/AI papers
- Minimum 20 references
- Code must run on ROS 2 Humble and specified Isaac Sim version
- Architecture diagrams must reflect actual pipelines

Book Requirements:
- Built with Docusaurus + Spec-Kit Plus and deployed to GitHub Pages
- Covers:
  1) ROS 2 humanoid control
  2) Gazebo/Unity digital twins
  3) NVIDIA Isaac perception/navigation
  4) VLA (LLM → ROS actions)
  5) Capstone: Autonomous humanoid robot
- Include runnable examples and diagrams

RAG Chatbot Requirements:
- Answers only from book content (including user-selected text)
- Stack: FastAPI + Neon Postgres + Qdrant + OpenAI Agents/ChatKit
- Retrieval pipeline must be transparent and testable

Constraints:
- Approx. 25k–35k words
- Zero hallucinations, zero broken code, consistent terminology

Success Criteria:
- Book builds and deploys cleanly
- Chatbot answers ≥80% test questions correctly
- All robotics workflows reproducible
- No unverified technical claims
```

## Response snapshot

A complete project constitution was created for the AI-Driven Book + RAG Chatbot on Physical AI & Humanoid Robotics project. The constitution includes:

- Six core principles covering technical accuracy, source verification, reproducibility, multi-modal documentation, hallucination prevention, and engineering-level clarity
- Project standards and constraints section outlining technology stack, deployment requirements, content scope, and quality assurance
- Development workflow section detailing specification-driven development, testing requirements, review process, and quality gates
- Governance section with amendment procedures
- Version tracking with Version 1.0.0, ratified on 2025-12-09

## Outcome

- ✅ Impact: Project constitution established with clear principles and governance
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific content
- 🔁 Next prompts: Can proceed with project planning and implementation following constitution
- 🧠 Reflection: Constitution properly reflects project requirements and constraints

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A