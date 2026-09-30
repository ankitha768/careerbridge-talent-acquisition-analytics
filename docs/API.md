# CareerBridge API

## List jobs
`GET /api/v1/jobs`

## Match candidate
`POST /api/v1/match/{job_id}`

## Rank all jobs
`POST /api/v1/rank`

The ranking output includes score, matched skills, missing skills, and an explanation so that the result is inspectable rather than a black box.
