# Soft Rebuild Status — 2026-04-22

## What was safe to promote

The current V7 export state supports a genuine soft rebuild of the public
payloads, but only for some layers.

- The paper-level science summary layer is mature.
- The paper-level PNU layer is mature.
- The operationalization layer is materially present.
- The theory-mechanism packet layer exists structurally, but is still empty in
  substance.

That means the right soft rebuild is:

- promote the 760-paper PNU surface into a first-class public payload
- enrich `article_details.json` with theory and metadata fields already present
  elsewhere
- add a theory index derived from article labels, debate clusters, and topic
  hierarchy
- add a mechanism inventory payload derived from the existing canonical
  mechanism manifest

It does **not** mean pretending that paper-grounded mechanism chains are ready.

## New payloads

The rebuild now emits three additional public payloads:

- `data/ka_payloads/paper_pnus.json`
- `data/ka_payloads/theories.json`
- `data/ka_payloads/mechanisms.json`

### `paper_pnus.json`

This is the strongest new surface. It contains all 760 papers with:

- paper identity and topic metadata
- short and long PNU text
- panel and verifier status
- basic operationalization counts
- basic argumentation counts

### `theories.json`

This is an honest soft-rebuild theory index, not a grand theory engine. It is
derived from:

- `articles.json`
- `article_details.json`
- `argumentation.json`
- `topic_hierarchy.json`

It is therefore descriptive. It supports navigation, clustering, and discovery,
but not yet paper-grounded theoretical prediction chains.

### `mechanisms.json`

This is a flattening of the existing canonical mechanism manifest from
`pnus.json`. It is useful as an inventory, but it is **not** yet the
paper-grounded mechanism-chain payload described in some journey documents.

## What remains not yet ready

These upstream structures should not yet be treated as rich public exports:

- lifecycle `theory_mechanism_packets`
- accepted-row `theory_mechanism_inventory`
- inferred theory/mechanism candidate chains

At present, those structures are present but substantively empty.

## Validation added

The local validation now covers:

- payload generation via `scripts/build_ka_adapter_payloads.py`
- runtime smoke checks for:
  - `paper_pnus.json`
  - `theories.json`
  - `mechanisms.json`
- payload contract tests in
  `tests/test_payload_soft_rebuild_contract.py`

## Practical interpretation

The public Atlas can now expose:

- paper-level PNU summaries
- a real theory index
- a real mechanism inventory

But it still cannot honestly claim:

- paper-grounded mechanism chains
- theory packets with populated prediction and linkage structure

That is the next deeper rebuild, not this one.
