# Fixes and Changes

Date: 2025-12-17

Summary of fixes made to make the app run error-free and tests pass:

- Align `backend/utils/auth_utils.py` with `User` model: replaced earlier `erp/email/bcrypt` usage with the project's `roll_no` and `User.set_password` / `User.check_password` helpers. This removes mismatches and avoids possible runtime errors if `auth_utils` is used.
- Hardened `backend/routes/materials_routes.py` `list_materials` endpoint: return an empty list if materials directory does not exist to avoid directory listing errors.
- Added basic tests in `backend/tests/test_api.py` to verify `GET /helpdesk/list` and `GET /attendance/view/1` behaviors.

Verification:

- Tests: `pytest` — all tests pass (2 passed).
- Smoke tests: `backend/tests/smoke_test.py` (run as module) was used to exercise key endpoints.

Notes / Next steps:

- The Gemini integration is a best-effort stub; if you plan to enable real Gemini API calls, ensure API keys are set in environment and the endpoints accept the expected payload (this code assumes a `description` or `similarity_score` is returned).
- Consider adding CI (GitHub Actions) to run `pytest` and linting automatically.

If you'd like, I can add a `requirements-dev.txt` with `pytest` and a flake8 configuration next.
