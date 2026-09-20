# Repository Architecture Map

## 1. High-Level Summary
- **Purpose**: [1-2 sentences on what this repository does]
- **Primary Tech Stack**: [Language, framework, key libraries]

## 2. Core Entry Points
- `src/main.py` / `index.ts`: Application bootstrap
- `src/config.py`: Environment and settings

## 3. Directory & Module Responsibilities
- `api/`: HTTP / RPC request handlers
- `services/`: Business logic and workflows
- `models/`: Database entities and schemas
- `tests/`: Automated unit and integration tests

## 4. Primary Data Flow
```text
Client Request -> Router -> Service Layer -> Database/Storage -> Response
```
