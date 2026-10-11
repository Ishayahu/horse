#!/usr/bin/env python3
"""Build final bounded YER-008 review from the saved YER-002 primary segments."""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; HERE=ROOT/'research/yerushalmi'
def lines(p): return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def write_lines(p,rows): p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
batch=lines(HERE/'YER-007.remaining.jsonl'); cand={x['id']:x for x in lines(HERE/'YER-002.candidates.jsonl')}; prior=lines(HERE/'YER-007.verdicts.jsonl')
accepted={
'yer-002-jerusalem-talmud-sotah-5-4-3':('direct','song_at_sea_horse_and_rider',"Complete segment explains responsive recitation of the Song at the Sea and quotes 'horse and its rider He cast into the sea.' Biblical liturgical quotation about divine deliverance, not horse-powered supernatural travel."),
'yer-002-jerusalem-talmud-taanit-4-5-13':('direct','betar_war_horses',"Complete segment narrates Bar Koziva and the fall of Betar. Mounted uprooting of a cedar is a military strength test; a horse later sinking to its nostrils in blood is atrocity/hyperbole imagery. Extraordinary scale, but no flying or interworld horse."),
'yer-002-jerusalem-talmud-terumot-8-1-2':('direct','fast_horse_legal_hypothetical',"Complete segment gives a divorce-delivery timing hypothetical: a route normally taking ten days is completed in five after finding a running horse. Rapid ordinary transport affects the terumah rule; no supernatural motion."),
'yer-002-jerusalem-talmud-yoma-3-2-5':('indirect','esther_royal_horse_redemption_sequence',"Complete segment likens Israel's redemption to gradually increasing dawn and lists stages from Esther, including Haman taking the royal garment and horse. Scriptural royal-procession allusion, not supernatural horse travel."),
}
rejected={
'yer-002-jerusalem-talmud-shevuot-3-8-3':"מסוסטלא is a measurement/architectural term in a giant-snake report; the segment's flying camel example contains no horse.",
'yer-002-jerusalem-talmud-sukkah-1-1-2':"הקיסוס is ivy in a list of plants used over a sukkah; substring only, not equine.",
'yer-002-jerusalem-talmud-sukkah-1-5-1':"הקיסוס is ivy in the Mishnah's plant list; substring only, not equine.",
'yer-002-jerusalem-talmud-yevamot-16-9-2':"סוסרטא occurs only in the personal name Samuel bar Susarta; not equine.",
'yer-002-jerusalem-talmud-yoma-3-1-3':"סוסיתה is the place-name Susita/Hippos in a time-of-day report; not equine.",
}
receipts=[]; fresh=[]; sources=[]
for r in batch:
 c=cand[r['candidate_id']]; receipts.append({'candidate_id':c['id'],'export_url':c['export_url'],'quote':c['quote'],'read_scope':'complete saved segment','constituent_versions':c['constituent_versions']})
 base={'schema_version':1,'candidate_id':c['id'],'task_id':'YER-008','work':c['work'],'locator':c['locator'],'url':c['url']}
 if c['id'] in rejected:
  fresh.append({**base,'verdict':'rejected','reason':rejected[c['id']],'carried_from_task_id':'YER-007'}); continue
 typ,role,context=accepted[c['id']]; sid=c['id'].replace('yer-002-jerusalem-talmud-','yerushalmi-')+'-guggenheimer'
 fresh.append({**base,'verdict':'accepted','reason':context,'registered_source_id':sid,'carried_from_task_id':'YER-007'})
 sources.append({'schema_version':1,'id':sid,'corpus_id':'yerushalmi','work':c['work'],'locator':c['locator'],'url':c['url'],'access_url':c['export_url'],'edition':c['constituent_versions'][0][0],'language':'Hebrew/Aramaic','mention_type':typ,'parent_source_id':None,'quote':c['quote'],'context':context,'checks':{'primary_read':True,'quote_verified':True,'context_checked':True,'attribution_verified':True,'commentaries_checked':False,'interpretation_prepared':True,'independent_reviewed':False},'interpretation':context,'epistemic_type':'primary_text','reviewers':['research-runner'],'task_id':'YER-008','role':role,'limitations':['Complete saved YER-002 export-derived primary segment read; no fresh surrounding halakha retrieved.','Merged export provenance not manuscript collation; no traditional commentaries or independent review.'],'accessed_at':'2026-10-11'})
repl={x['candidate_id']:x for x in fresh}; ledger=[repl.get(x['candidate_id'],x) for x in prior]; counts=Counter(x['verdict'] for x in ledger)
write_lines(HERE/'YER-008.verdicts.jsonl',ledger); write_lines(HERE/'YER-008.sources.jsonl',sources); write_lines(HERE/'YER-008.remaining.jsonl',[])
(HERE/'YER-008.read-excerpts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
report=f"# YER-008 — final bounded primary context review, 2026-10-11\n\n9 previously pending candidates read: {len(sources)} accepted primary segment records ({sum(x['mention_type']=='direct' for x in sources)} direct, {sum(x['mention_type']=='indirect' for x in sources)} indirect); {9-len(sources)} rejected lexical false positives. Cumulative finite discovery ledger: {dict(counts)}. Remaining: 0 candidates. This closes the saved YER-002 candidate ledger, not every possible spelling, edition, commentary, manuscript or allusion.\n\n"
for s in sources: report+=f"- {s['work']} {s['locator']}: {s['context']}\n"
report+="\nActual access URLs and exact Hebrew/Aramaic quotations are in sources; read-excerpts preserves named receipt scope. Commentary and independent-review flags remain false. No reliable ancient dating or historical verification is inferred from modern edition metadata.\n"
(HERE/'YER-008.report.md').write_text(report)
