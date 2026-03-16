# Internal Contracts

This document defines the stable JSON-like shapes introduced in Phases 3 and 4.

## Resolve request

```json
{
  "original_name": "Faecalibacterium prausnitzii",
  "provided_level": "species",
  "allow_fuzzy": true,
  "source": {
    "batch_id": "import-001",
    "sheet": "Qualitative findings",
    "row": 42
  },
  "context": {}
}
```

## Resolve result

```json
{
  "original_name": "Faecalibacterium prausnitzii",
  "normalized_name": "faecalibacterium prausnitzii",
  "provided_level": "species",
  "status": "resolved_exact_scientific",
  "review_required": false,
  "auto_accept": true,
  "match_type": "exact_scientific",
  "warnings": [],
  "matched_taxid": 853,
  "matched_name": "Faecalibacterium prausnitzii",
  "matched_rank": "species",
  "score": 1.0,
  "candidates": [],
  "lineage": [],
  "cache_applied": false,
  "metadata": {}
}
```

## Fuzzy suggestion result

```json
{
  "original_name": "Faecalibacterim prausnitzii",
  "normalized_name": "faecalibacterim prausnitzii",
  "provided_level": "species",
  "status": "suggested_fuzzy_unique",
  "review_required": true,
  "auto_accept": false,
  "match_type": "fuzzy",
  "warnings": [],
  "matched_taxid": null,
  "matched_name": null,
  "matched_rank": null,
  "score": null,
  "candidates": [
    {
      "taxid": 853,
      "name": "Faecalibacterium prausnitzii",
      "rank": "species",
      "match_type": "fuzzy",
      "score": 96.4,
      "lineage": [],
      "warnings": []
    }
  ],
  "lineage": [],
  "cache_applied": false,
  "metadata": {}
}
```

## Decision record

```json
{
  "action": "confirm",
  "original_name": "F. prausnitzii",
  "normalized_name": "f. prausnitzii",
  "provided_level": "species",
  "taxonomy_build_version": "2026-03-16",
  "reviewer": "curator@example.com",
  "resolved_taxid": 853,
  "matched_scientific_name": "Faecalibacterium prausnitzii",
  "match_type": "user_selected",
  "status": "confirmed_by_user",
  "score": 95.8,
  "warnings": [],
  "notes": "Confirmed against paper context.",
  "created_at": "2026-03-16T21:00:00+00:00"
}
```

## Batch result summary

`BatchResolveResult.summary` is a dictionary keyed by status value. The scaffold
always returns all known statuses so downstream consumers can rely on stable
keys even when some counts are zero.
