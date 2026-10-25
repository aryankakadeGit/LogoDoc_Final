MODULE: ai                    STATUS: FINALIZED (pending real-API test)
Purpose : Send a prompt (+ optional PNG image) to an AI and get raw JSON text back.
Input   : await provider.generate_json(prompt: str, schema: type[BaseModel], image_png: bytes | None = None)
Output  : str  (raw JSON text; the caller parses and validates it)
Errors  : AIConfigError 500   missing/invalid key or model, bad request
          AIRateLimited 429   free quota used up (not retried)
          AIUnavailable 503   timeout / connection / Google server error after 3 attempts
          AIBadResponse 502   empty, blocked or cut-off response
Depends : core (config, exceptions); google-genai
Used by : analysis, recommendations (text-only calls)
Create  : create_provider(get_settings())  -- once at startup in main.py
Test    : pytest tests/ai   |   python -m scripts.try_ai [path/to/logo.png]
Settings: async, 30 s timeout per attempt, 3 attempts, temperature 0.2, JSON schema output