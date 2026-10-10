# VER-002c — independent KAB-001 review

Three records independently reopened from newly fetched original-language Sefaria JSON exports, quoted substrings verified exactly after tag stripping, and surrounding passages reread. Separate actual folio-labelled primary digital texts also read. All three pass with locator/evidence clarification; no literal horse transport between worlds established by these passages. Do not read 'symbolic' as a denial of the texts' asserted supernal powers or divine garments.

| Source | Traditional locator | Export locator |
|---|---|---|
| Horse/rider, upper/lower authority | Zohar II54b, Beshalach | Beshalach15:22 |
| Opposed chariots, mercy/judgment | Zohar I211b, Vayigash | Vayigash12:11 |
| Mare as merkavah, garments | Tikkunei Zohar, Introduction3b | 3b:8; one-based array[6,8] |

The two parasha subsection references are valid digital locators, not traditional folio numbers. Independently fetched Zohar export has Vilna Pages54b overlay in Beshalach15:13, preceding selected22, and211b overlay in Vayigash12:9, preceding selected11. Separate folio texts confirm the passage positions:

- https://he.wikisource.org/wiki/זהר_חלק_ב_נד_ב — actual horse/rider and linked upper/lower authorities; revision oldid476890.
- https://he.wikisource.org/wiki/זהר_חלק_א_ריא_ב — actual Song1:9 mare phrase and opposed chariots; revision oldid486613. The page also includes a later Vayechi section marked textually doubtful; that notice should not be silently transferred to the earlier reviewed Vayigash paragraph.
- https://www.zoharonline.org/zohar/tikkunei-zohar/tikkunei-zohar/daf-3b/ — actual Aramaic3b:5–9 and explicit position6/295. Digital textual provenance may overlap Sefaria, so this is independent agent reading plus digital locator corroboration, not independent manuscript collation.

Beshalach20–23 relates song/world-to-come context and judgement on upper authorities before earthly judgment. Vayigash10–13 explicitly uses mare/chariot verse, left/other-side and right/holiness, mercy/judgment; original short quote 'these of mercy and these of judgment' is exact but does not alone show the equine referent, so quote enrichment suggested in verdict. Tikkunei5–9 supplies prayer/throne repair, names, mare as divine merkavah, ten sefirot of Beriah/weekday angelic garment classes, and contrasting Atzilut relation. No passage narrates a horse carrying a traveler from one spiritual world to another.

All KAB source files left unchanged. Coordinator can apply verdict locator/link enrichments and mark independent_reviewed with original+reviewer identities. Historical composition dating, printed witnesses, and detailed sefirotic referent assignments remain pending.

Reproducibility issue: KAB-001.search.py refers to transient LAT-001.inventory-cache.json owned by another task. It should fetch books.json itself or consume KAB's own saved selected inventory. That cache was reproducible and removed by LAT cleanup; cross-task transient dependencies must not be relied on for future runs.
