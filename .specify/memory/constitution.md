# AI-Driven Book + RAG Chatbot on Physical AI & Humanoid Robotics Constitution

## Core Principles

### Technical Accuracy First
All technical claims, code examples, and architectural decisions must be verified from official documentation and peer-reviewed robotics/AI sources. No unverified technical statements allowed in the book or chatbot knowledge base.

### Source Verification Requirement
Every factual claim must be source-verified from official documentation or academic robotics/AI papers. Minimum 20 references required across the project. All sources must be cited appropriately.

### Reproducibility Standard (NON-NEGOTIABLE)
All code examples, setup steps, and robotics workflows must be reproducible. Code must run on specified ROS 2 Humble and NVIDIA Isaac Sim versions. Zero broken code allowed in deliverables.

### Multi-Modal Documentation
Both book and chatbot must use the same knowledge base. Content must be designed for both static documentation (book) and interactive retrieval (chatbot). Consistent terminology and concepts required.

### Hallucination Prevention
RAG chatbot must answer only from verified book content and user-provided text. Zero hallucinations allowed. Retrieval pipeline must be transparent and testable with ≥80% accuracy on test questions.

### Engineering-Level Clarity
All documentation must be written at FK grade 11–13 level. Technical concepts must be explained clearly with runnable examples and accurate architecture diagrams reflecting actual implementation.

## Project Standards and Constraints

Technology Stack: Spec-Kit Plus, Claude Code, Docusaurus, GitHub Pages, ROS 2, Gazebo, Unity, NVIDIA Isaac, FastAPI, Neon, Qdrant, OpenAI Agents/ChatKit. All components must integrate seamlessly and be version-compatible.

Deployment Requirements: Book built with Docusaurus deployed to GitHub Pages. Chatbot stack: FastAPI + Neon Postgres + Qdrant + OpenAI Agents/ChatKit. Both must deploy cleanly without errors.

Content Scope: Book covers ROS 2 humanoid control, Gazebo/Unity digital twins, NVIDIA Isaac perception/navigation, VLA (LLM → ROS actions), and capstone autonomous humanoid robot. Approximately 25k–35k words total.

Quality Assurance: Architecture diagrams must reflect actual pipelines. No unverified technical claims. All robotics workflows must be reproducible. Code examples must be tested and functional.

## Development Workflow

Specification-Driven Development: All development follows Spec-Kit Plus methodology. Features must be specified in detail before implementation begins. Changes to specification require explicit approval before proceeding.

Testing Requirements: All code changes must include appropriate tests. Book content must include runnable examples that are verified to work. Chatbot retrieval accuracy must be validated against test question sets.

Review Process: All PRs must verify compliance with technical accuracy requirements. Complex implementations must be justified with clear reasoning. Code reviews must validate both correctness and adherence to architectural decisions.

Quality Gates: All deliverables must pass technical accuracy verification, reproducibility testing, and hallucination prevention checks. No unverified technical claims allowed in final output.

## Governance

This constitution governs all aspects of the AI-Driven Book + RAG Chatbot project. All development practices, code changes, and documentation updates must comply with these principles. Any deviation requires explicit amendment to this constitution.

Amendments to this constitution must document the reasoning, obtain approval from project stakeholders, and include a migration plan for existing code and documentation. All team members must acknowledge and follow updated principles after amendments.

**Version**: 1.0.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09