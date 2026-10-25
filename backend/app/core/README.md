MODULE: core                  STATUS: FINALIZED (pending local test)
Purpose : Shared settings, base error type and logging setup.
Output  : config      -> get_settings() -> Settings  (from env vars / backend/.env)
          exceptions  -> AppError, app_error_handler  (one JSON error shape)
          logging     -> setup_logging(level)          (modules use logging.getLogger(__name__))
Errors  : invalid .env values -> pydantic ValidationError at startup
Depends : pydantic-settings, fastapi
Used by : every module; main.py registers app_error_handler and calls setup_logging
Test    : pytest tests/core