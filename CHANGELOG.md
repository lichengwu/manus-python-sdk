# Changelog

All notable changes to the Manus Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **BREAKING**: Clarified this is an unofficial community SDK (not affiliated with Manus AI)
- Updated LICENSE with community author and additional disclaimer terms
- Updated README with unofficial disclaimer and official Manus AI resources section

### Added
- Initial release of the Manus Python SDK (community maintained)
- Synchronous client (`Manus`) for API interactions
- Asynchronous client (`AsyncManus`) for async API interactions
- Projects API (create, list, retrieve, update, delete)
- Tasks API via Responses API
- Files API with presigned URL upload
- Webhooks API with signature verification
- Models API for listing and retrieving models
- Comprehensive error handling with custom exception hierarchy
- Type hints for all public APIs
- Pydantic models for request/response validation
- Support for cursor-based pagination
- Automatic retry with exponential backoff
- Environment variable configuration
- Complete test suite with pytest
- Example scripts for common use cases
- GitHub Actions CI/CD workflows
- GitHub Packages publishing support

## [0.1.0] - 2026-03-04

### Added
- Initial release
- PyPI package: `manus-sdk`
- Full API coverage: Projects, Tasks, Files, Webhooks, Models
- OpenAI SDK compatibility (`openai>=1.100.2`)
- Streaming support with SSE
- File upload with presigned URLs
- Webhook signature verification

### Note

This is an **unofficial community-maintained SDK** and is not affiliated with, endorsed by, or sponsored by Manus AI.
