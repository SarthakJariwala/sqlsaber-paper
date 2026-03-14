Thread: bef6ae0b-bbba-4a1c-9dd6-619c3fbecd43

Database: california_schools
Title: What is the total number of non-chartered schools in the county of Los Angeles with a percent (%) of eligible free meals for grades 1 through 12 that is less than 0.18%?

Context: non-chartered schools refer to schools whose Charter = 0; K-12 means grades 1 through 12; percent of eligible free rate for K-12 = `Free Meal Count (K-12)` * 100 / `Enrollment (K-12)`
Last activity: 2026-03-11 23:01:41
Model: claude-opus-4-6

**User:**

What is the total number of non-chartered schools in the county of Los Angeles with a percent (%) of eligible free meals for grades 1 through 12 that is less than 0.18%?

Context: non-chartered schools refer to schools whose Charter = 0; K-12 means grades 1 through 12; percent of eligible free rate for K-12 = `Free Meal Count (K-12)` * 100 / `Enrollment (K-12)`

**Assistant:**

Let me start by searching the knowledge base and exploring the relevant tables to understand the database structure.


**🔎 Searching knowledge base**

- **query**: non-chartered schools Los Angeles free meals K-12


**⚙️ Discovering available tables**

*No results*

**Database Tables (3 total)**

| Schema   | Table Name   | Type   |
|----------|--------------|--------|
| main     | frpm         | table  |
| main     | satscores    | table  |
| main     | schools      | table  |


**⚙️ Examining schema**


**🔎 Searching knowledge base**

- **query**: charter county free meal enrollment


**Schema Information (1 tables):**

**Table: main.frpm**

| Column                                      | Type    | Nullable   | Default   | Comments   |
|---------------------------------------------|---------|------------|-----------|------------|
| CDSCode                                     | TEXT    | False      |           |            |
| Academic Year                               | TEXT    | True       |           |            |
| County Code                                 | TEXT    | True       |           |            |
| District Code                               | INTEGER | True       |           |            |
| School Code                                 | TEXT    | True       |           |            |
| County Name                                 | TEXT    | True       |           |            |
| District Name                               | TEXT    | True       |           |            |
| School Name                                 | TEXT    | True       |           |            |
| District Type                               | TEXT    | True       |           |            |
| School Type                                 | TEXT    | True       |           |            |
| Educational Option Type                     | TEXT    | True       |           |            |
| NSLP Provision Status                       | TEXT    | True       |           |            |
| Charter School (Y/N)                        | INTEGER | True       |           |            |
| Charter School Number                       | TEXT    | True       |           |            |
| Charter Funding Type                        | TEXT    | True       |           |            |
| IRC                                         | INTEGER | True       |           |            |
| Low Grade                                   | TEXT    | True       |           |            |
| High Grade                                  | TEXT    | True       |           |            |
| Enrollment (K-12)                           | REAL    | True       |           |            |
| Free Meal Count (K-12)                      | REAL    | True       |           |            |
| Percent (%) Eligible Free (K-12)            | REAL    | True       |           |            |
| FRPM Count (K-12)                           | REAL    | True       |           |            |
| Percent (%) Eligible FRPM (K-12)            | REAL    | True       |           |            |
| Enrollment (Ages 5-17)                      | REAL    | True       |           |            |
| Free Meal Count (Ages 5-17)                 | REAL    | True       |           |            |
| Percent (%) Eligible Free (Ages 5-17)       | REAL    | True       |           |            |
| FRPM Count (Ages 5-17)                      | REAL    | True       |           |            |
| Percent (%) Eligible FRPM (Ages 5-17)       | REAL    | True       |           |            |
| 2013-14 CALPADS Fall 1 Certification Status | INTEGER | True       |           |            |

**Primary Keys:** CDSCode

**Foreign Keys:** CDSCode -> main.schools.CDSCode

*No results*

**Assistant:**

I can see the `frpm` table has all the columns we need. Now let me write and execute the query.

**What we're looking for:**
- **Non-chartered schools**: `"Charter School (Y/N)" = 0`
- **In Los Angeles county**: `"County Name" = 'Los Angeles'`
- **Free meal percent for K-12 < 0.18%**: Using the formula `"Free Meal Count (K-12)" * 100 / "Enrollment (K-12)" < 0.18`


**Executing SQL:**

```sql

SELECT COUNT(*) AS total_non_chartered_schools
FROM frpm
WHERE "Charter School (Y/N)" = 0
  AND "County Name" = 'Los Angeles'
  AND "Free Meal Count (K-12)" * 100.0 / "Enrollment (K-12)" < 0.18
  AND "Enrollment (K-12)" > 0

```


**Results (1 rows):**

|   total_non_chartered_schools |
|-------------------------------|
|                             1 |

**Assistant:**

### Result

The total number of **non-chartered schools** in **Los Angeles County** with a **free meal eligibility rate for grades K-12 less than 0.18%** is **1**.

### How the query works:
1. **Filters for non-chartered schools** — only schools where `Charter School (Y/N) = 0`
2. **Filters for Los Angeles County** — matches on `County Name = 'Los Angeles'`
3. **Calculates the free meal percentage** — using the formula: `Free Meal Count (K-12) × 100 / Enrollment (K-12)`, and keeps only those with a rate below 0.18%
4. **Excludes schools with zero enrollment** — to avoid division-by-zero errors

So only **1 school** in Los Angeles County meets all of these criteria.


