# API Contract

_To be finalized in the Architecture phase._

Planned endpoints (draft):
- GET  /api/health
- POST /api/logo/analyze                    (multipart image upload -> analysis JSON)
- POST /api/logo/recommendations/ai-prompt          (analysis -> improved image-generation prompt)
- POST /api/logo/recommendations/designer           (analysis -> designer recommendations)
- POST /api/logo/recommendations/designer/download  (analysis -> designer recommendations .txt file)
