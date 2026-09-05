# Dataset Export Example

Scope: apply BEP design preferences directly to new APIs. In an existing API,
preserve established supported conventions, including version placement, naming,
and representation shapes. Do not require migration or deprecation merely for
style conformity. The checks below apply to the changed contract and selected
profile; security, protocol correctness, and supported behavior remain required.

Use this independent scenario to test resource modeling, asynchronous work,
idempotency, conditional requests, and result discovery. This example explicitly
selects required date-header versioning and required idempotency keys for export
job creation because clients retry long-running work after unknown outcomes.

## Contents

- [Requirements](#requirements)
- [Resource Inventory](#resource-inventory)
- [Capability Mapping](#capability-mapping)
- [Create Work](#create-work)
- [Complete And Retrieve](#complete-and-retrieve)
- [Create Cancellation And Retry](#create-cancellation-and-retry)
- [Replace And Patch](#replace-and-patch)
- [OpenAPI Fragment](#openapi-fragment)

## Requirements

A reporting service stores datasets. Clients can change dataset metadata,
replace complete export policies, start asynchronous exports, inspect progress,
cancel pending work, retrieve completed results, and retry failed exports.
The `analytics` domain group owns all resources in this example because it owns
their identity, export invariants, lifecycle, retention, and authorization.

## Resource Inventory

| Resource | Meaning | Identity and lifecycle | Canonical URI |
| --- | --- | --- | --- |
| Dataset | A reportable body of data | Stable dataset ID; created, updated, deleted | `/datasets/{datasetId}` |
| Export policy | Complete export rules owned by one dataset | Singleton; replaced as a whole | `/datasets/{datasetId}/export-policy` |
| Export job | One requested export attempt | Stable job ID; pending through terminal state | `/datasets/{datasetId}/export-jobs/{jobId}` |
| Export cancellation | The cancellation requested for one job | Singleton; created while the job is cancellable and retained for audit | `/datasets/{datasetId}/export-jobs/{jobId}/cancellation` |
| Export result | Immutable output of one completed job | Exists only after completion; retained by policy | `/datasets/{datasetId}/export-jobs/{jobId}/result` |

Retry creates a new export job referencing the failed job. It does not erase or
rewrite the failed attempt.

## Capability Mapping

| Capability | Resource operation |
| --- | --- |
| Browse datasets | `GET /datasets` |
| Change dataset metadata | `PATCH /datasets/{datasetId}` |
| Replace export policy | `PUT /datasets/{datasetId}/export-policy` |
| Start export | `POST /datasets/{datasetId}/export-jobs` |
| Inspect progress | `GET /datasets/{datasetId}/export-jobs/{jobId}` |
| Cancel pending export | `PUT /datasets/{datasetId}/export-jobs/{jobId}/cancellation` |
| Retrieve output | `GET /datasets/{datasetId}/export-jobs/{jobId}/result` |
| Retry failed export | Create a new job with `sourceJob` referencing the failure |

No `start`, `cancel`, or `retry` procedure endpoint is necessary.

## Create Work

Create the job in its collection:

```http
POST /datasets/dataset-123/export-jobs HTTP/1.1
Host: api.example.com
API-Version: 2026-08-02
Content-Type: application/json
Idempotency-Key: "4c8fd2a8-7e33-4c93-8ce7-158e3fbd8435"

{
  "format": "csv",
  "compression": "gzip"
}
```

The job exists immediately even though execution is asynchronous:

```http
HTTP/1.1 201 Created
Location: https://api.example.com/datasets/dataset-123/export-jobs/job-456
ETag: "job-456-1"
Content-Type: application/json
API-Version: 2026-08-02
Request-Id: req_01K1D3A3P0QK

{
  "id": "job-456",
  "datasetId": "dataset-123",
  "status": "pending",
  "format": "csv",
  "compression": "gzip",
  "createdAt": "2026-07-30T14:00:00Z",
  "links": {
    "self": "https://api.example.com/datasets/dataset-123/export-jobs/job-456"
  }
}
```

The idempotency contract binds the key to the caller, job collection, and
request fingerprint for the documented retention window. Replaying the same
request returns the original outcome. Reusing the key with different content
returns the API's documented `422` problem. A concurrent duplicate while the
first request is still processing returns the documented `409` problem.

## Complete And Retrieve

Once complete, the job links to its result:

```json
{
  "id": "job-456",
  "datasetId": "dataset-123",
  "status": "completed",
  "createdAt": "2026-07-30T14:00:00Z",
  "completedAt": "2026-07-30T14:01:12Z",
  "links": {
    "self": "https://api.example.com/datasets/dataset-123/export-jobs/job-456",
    "result": "https://api.example.com/datasets/dataset-123/export-jobs/job-456/result"
  }
}
```

Before completion, the result resource does not exist and `GET` returns the
documented `404` problem. After retention expiry, the contract may use `410`
when permanent removal is meaningful and observable.

## Create Cancellation And Retry

Create the known singleton cancellation resource for a pending job:

```http
PUT /datasets/dataset-123/export-jobs/job-456/cancellation HTTP/1.1
Host: api.example.com
API-Version: 2026-08-02
Content-Type: application/json
If-None-Match: *

{}
```

Return `201 Created` with the cancellation's `Location` and representation the
first time it is created. A repeated create-only request fails its precondition
with `412`; the client can retrieve the existing cancellation. Return
`409 Conflict` when the job was already terminal before the cancellation
resource could be created. Keep the cancellation available according to the
audit policy:

```json
{
  "job": "/datasets/dataset-123/export-jobs/job-456",
  "status": "requested",
  "requestedAt": "2026-07-30T14:00:15Z",
  "links": {
    "self": "https://api.example.com/datasets/dataset-123/export-jobs/job-456/cancellation"
  }
}
```

Retry by creating another job:

```http
POST /datasets/dataset-123/export-jobs HTTP/1.1
Host: api.example.com
API-Version: 2026-08-02
Content-Type: application/json
Idempotency-Key: "8e812b21-fd7d-42a0-aa85-4d043f345946"

{
  "format": "csv",
  "compression": "gzip",
  "sourceJob": "https://api.example.com/datasets/dataset-123/export-jobs/job-456"
}
```

Return `201 Created` and the new job's `Location`. Keep the failed job available
according to audit and retention policy.

## Replace And Patch

Replace the complete policy with idempotent `PUT` and optimistic concurrency:

```http
PUT /datasets/dataset-123/export-policy HTTP/1.1
Host: api.example.com
API-Version: 2026-08-02
Content-Type: application/json
If-Match: "policy-7"

{
  "allowedFormats": ["csv", "json"],
  "maximumRetentionDays": 30
}
```

Partially update dataset metadata with explicit merge-patch semantics:

```http
PATCH /datasets/dataset-123 HTTP/1.1
Host: api.example.com
API-Version: 2026-08-02
Content-Type: application/merge-patch+json
If-Match: "dataset-12"

{
  "name": "Quarterly Revenue"
}
```

## OpenAPI Fragment

Keep retry, concurrency, and security behavior discoverable in the operation:

```yaml
/datasets/{datasetId}/export-jobs:
  post:
    operationId: createDatasetExportJob
    summary: Create an export job
    parameters:
      - $ref: '#/components/parameters/DatasetId'
      - $ref: '#/components/parameters/ApiVersion'
      - $ref: '#/components/parameters/IdempotencyKey'
    security:
      - resourceOAuth: [datasets:export]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CreateExportJob'
    responses:
      '201':
        description: Export job created
        headers:
          Location:
            $ref: '#/components/headers/Location'
          Request-Id:
            $ref: '#/components/headers/RequestId'
          API-Version:
            $ref: '#/components/headers/ApiVersion'
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ExportJob'
      '409':
        $ref: '#/components/responses/IdempotencyRequestInProgress'
      '422':
        $ref: '#/components/responses/IdempotencyKeyReuse'
```

The complete contract must also define authentication failures, authorization
failures, missing datasets, validation failures, rate limits, and unexpected
server failures according to the API's error policy.
