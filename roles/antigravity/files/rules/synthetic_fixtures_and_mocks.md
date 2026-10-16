---
trigger: always_on
description: "Use 100% synthetic fixtures, placeholder infrastructure identifiers, and fictional domain-neutral mock names in tests, examples, and documentation."
---

# Synthetic Fixtures and Fictional Mock Naming

Fixtures, mocks, sample datasets, and example configs must be 100% synthetic.
Author test and example data from scratch using fictional stand-ins rather than
real infrastructure identifiers or production values.

## 1. Placeholder Infrastructure Identifiers

Use standard reserved domains and obviously fictional stand-ins across source
code, tests, fixtures (`testdata/`, `fixtures/`, `mocks/`), and docs:

- **Hostnames and URLs:** RFC 2606 reserved domains such as `api.example.com`
  or `widgets.example.org`, never real internal hostnames or admin consoles.
- **Databases (PostgreSQL, MySQL, Redis):** fictional connection strings and
  schemas such as `postgres://app@db.example.com/acme_widgets`, never real
  database, schema, or table names.
- **Object storage (S3 and similar):** fictional buckets such as
  `s3://acme-widget-archive/`, never real bucket names or paths.
- **Cloud accounts, IAM roles, and KMS keys:** zeroed placeholder IDs such as
  `arn:aws:iam::000000000000:role/acme-widget-reader`, never real account IDs,
  role names, or key ARNs.
- **gRPC and REST services:** fictional service namespaces such as
  `acme.widgets.v1.WidgetService/GetWidget`, never real service names or method
  paths.
- **People and groups:** placeholder identities such as `user@example.com` and
  `acme-widget-owners`, never real usernames, emails, or team groups.
- **Credentials and tokens:** obvious dummy placeholders, never real API keys,
  tokens, passwords, or private keys (even expired ones).

## 2. Fictional Mock Names Over Mock-Prefixed Real Names

A `Mock`, `Fake`, `Sample`, `Test`, or `Dummy` prefix does **not** make a name
synthetic. Putting one in front of a real or recognizable system, datastore,
product, or business concept still couples the fixture to the real asset.

- **Avoid mock-prefixed real names:** `Mock Production Users Database`,
  `Mock Prod Auth Service`, `Mock Main Search Cluster`, `MockUsersTable`,
  `fake-internal-admin-api`, `sample_prod_cluster`.
- **Use fictional, domain-neutral names:** `Acme Widget Database`,
  `Northwind Order Store`, `Example Inventory Catalog`, `Alpha Blob Archive`,
  `Beta Ticket Queue`, and IDs like `acme-widget-db` or
  `northwind_order_service`.
- **Format vocabulary exception:** config keys, enum values, and label
  constants that the code under test actually parses may appear verbatim. The
  values bound to them (asset names, IDs, principals, table names, file names)
  must still be fictional.
- **Scope:** applies to every line of a fixture or test file you touch, not
  only the lines you add.
- **Self-check:** if a reader could guess which real system a mock stands in
  for from its name alone, rename it to something fictional.
