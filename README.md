# Electriclarryland — Natural Language to SQL (Museum DB)
Natural Language Project By. Logan Carpenter

This project connects GPT-4 to a SQLite museum database and lets you ask plain English questions that get translated into SQL queries. I wanted to see how far you could push a zero-shot approach before it starts falling apart — turns out, pretty far for simple stuff, not so much for anything that requires real-world context.

The database tracks a museum's artifacts, curators, exhibitions, restorations, and location history.

![Schema Diagram](https://github.com/Lars1994507/Electriclarryland/blob/main/Screenshot%202024-10-05%20212115.png)

---

## Questions That Worked

### Question 1 — Zero-shot
**Asked:** How many artifacts are in the museum?

```sql
SELECT COUNT(*) FROM artifact;
```

**Response:**
> The museum has 4 artifacts.

---

### Question 2 — Zero-shot
**Asked:** Which artifacts have an origin country that is in Europe?

```sql
SELECT artifact_id, name, origin_country
FROM artifact
WHERE origin_country IN ('Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom', 'Vatican City');
```

The model hardcoded every European country rather than anything clever — but hey, it works.

**Response:**
> The ancient vase originates from Greece, and the Renaissance painting is from Italy. Both countries are in Europe.
>
> - (1, 'Ancient Vase', 'Greece')
> - (3, 'Renaissance Painting', 'Italy')

---

### Question 3 — Zero-shot
**Asked:** Which artifacts have been curated by Mark Roberts?

```sql
SELECT a.artifact_id, a.name
FROM artifact a
INNER JOIN curator c ON a.curator_id = c.curator_id
WHERE c.name = 'Mark Roberts';
```

**Response:**
> Mark Roberts has curated the artifact known as the Medieval Sword.
>
> (2, 'Medieval Sword')

---

### Question 4 — Single-domain double-shot
**Asked:** Which artifacts were restored in 2022?

```sql
SELECT artifact.artifact_id, artifact.name
FROM artifact
JOIN restoration ON artifact.artifact_id = restoration.artifact_id
WHERE strftime('%Y', restoration.restoration_date) = '2022';
```

**Response:**
> In 2022, an ancient vase was among the artifacts restored.
>
> (1, 'Ancient Vase')

---

### Question 5 — Zero-shot
**Asked:** Which curator manages the most artifacts?

```sql
SELECT c.name, COUNT(a.artifact_id) AS artifact_count
FROM curator c
JOIN artifact a ON c.curator_id = a.curator_id
GROUP BY c.curator_id, c.name
ORDER BY artifact_count DESC
LIMIT 1;
```

Solid use of `GROUP BY` + `ORDER BY` + `LIMIT` — this is the kind of aggregation question that zero-shot handles cleanly because the schema makes the relationship obvious.

**Response:**
> Alice Johnson manages the most artifacts, with a total of 2 — the Ancient Vase and the Mayan Statue.
>
> ('Alice Johnson', 2)

---

### Question 6 — Zero-shot
**Asked:** Show every artifact, which exhibition it's in, and where in the building it's displayed.

```sql
SELECT a.name AS artifact, e.title AS exhibition, e.location, ea.display_position
FROM artifact a
JOIN exhibition_artifact ea ON a.artifact_id = ea.artifact_id
JOIN exhibition e ON ea.exhibition_id = e.exhibition_id
ORDER BY e.exhibition_id;
```

Three-table join with a clean natural language description. The model picked the right join path and aliased columns sensibly without being told to.

**Response:**
> Here's where everything is currently displayed:
>
> - **Renaissance Painting** — *The Art of the Renaissance*, Main Gallery (Center Wall)
> - **Medieval Sword** — *Medieval Weaponry*, Exhibition Hall A (Middle of the Room)
> - **Ancient Vase** — *Ancient Civilizations*, Exhibition Hall B (Entrance Display)
> - **Mayan Statue** — *Ancient Civilizations*, Exhibition Hall B (Corner Display)

---

### Question 7 — Zero-shot
**Asked:** Which artifact has never been restored?

```sql
SELECT a.artifact_id, a.name
FROM artifact a
LEFT JOIN restoration r ON a.artifact_id = r.artifact_id
WHERE r.restoration_id IS NULL;
```

This one's interesting because it requires a `LEFT JOIN` to find the absence of a record. The model didn't reach for a subquery or `NOT IN` — it went straight for the cleaner approach.

**Response:**
> The Renaissance Painting is the only artifact in the collection with no restoration on record.
>
> (3, 'Renaissance Painting')

---

### Question 8 — Zero-shot
**Asked:** How many artifacts does each curator manage, and what is their specialization?

```sql
SELECT c.name, c.specialization, COUNT(a.artifact_id) AS total_artifacts
FROM curator c
LEFT JOIN artifact a ON c.curator_id = a.curator_id
GROUP BY c.curator_id, c.name, c.specialization
ORDER BY total_artifacts DESC;
```

Using `LEFT JOIN` here is the right call — it ensures curators with zero artifacts still show up. The model chose it correctly without being prompted.

**Response:**
> Here's the breakdown by curator:
>
> - **Alice Johnson** (Ancient Artifacts) — 2 artifacts
> - **Mark Roberts** (Sculptures) — 1 artifact
> - **Sophie Martinez** (Paintings) — 1 artifact

---

### Question 9 — Zero-shot
**Asked:** What was the most recent restoration, and what work was done?

```sql
SELECT a.name, r.restoration_date, r.details
FROM restoration r
JOIN artifact a ON r.artifact_id = a.artifact_id
ORDER BY r.restoration_date DESC
LIMIT 1;
```

Simple `ORDER BY DESC LIMIT 1` pattern, but it's a good example of how the model pulls the human-readable `details` column without being told it exists.

**Response:**
> The most recent restoration was performed on the Mayan Statue on January 20, 2023. The work involved repairing missing pieces of the statue.
>
> ('Mayan Statue', '2023-01-20', 'Repaired missing pieces of the statue')

---

## Questions That Didn't Work

### Question 10 — Cross-domain
**Asked:** Which artifacts from the Italian Renaissance are currently on display in the Main Gallery?

```sql
SELECT a.artifact_id, a.name
FROM artifact a
JOIN exhibition_artifact ea ON a.artifact_id = ea.artifact_id
JOIN exhibition e ON ea.exhibition_id = e.exhibition_id
WHERE a.origin_country = 'Italy'
  AND a.creation_date BETWEEN '1400-01-01' AND '1600-12-31'
  AND e.location = 'Main Gallery'
  AND e.start_date <= date('now')
  AND (e.end_date >= date('now') OR e.end_date IS NULL);
```

The SQL itself is actually correct. The problem is the data — the exhibition end dates in the test database are in 2023, so `date('now')` returns nothing. The model had no way to know the data was stale.

**Response:**
> []
>
> I'm sorry, but without knowing the specific institution or museum you are referring to, I cannot provide the information about Italian Renaissance artifacts currently on display in the Main Gallery.

---

### Question 11 — Cross-domain
**Asked:** Which exhibitions currently feature artifacts that have been moved from storage within the last year?

```sql
SELECT DISTINCT e.exhibition_id, e.title
FROM exhibition e
JOIN exhibition_artifact ea ON e.exhibition_id = ea.exhibition_id
JOIN artifact_location al ON ea.artifact_id = al.artifact_id
WHERE al.move_date >= DATE('now', '-1 year')
  AND al.from_location = 'storage';
```

Same issue as above — the `from_location` values in the DB use full names like `'Storage Room A'`, not just `'storage'`. The model guessed at a value it couldn't see. Would probably be fixable with a few-shot example showing the actual location format.

**Response:**
> []
>
> I'm unable to provide real-time or the most current updates on exhibitions and the movement of artifacts.
