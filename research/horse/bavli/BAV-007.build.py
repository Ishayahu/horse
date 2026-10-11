#!/usr/bin/env python3
"""Build final BAV-007 adjudication from saved primary export segments."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; HERE=ROOT/'research/bavli'
def rows(p): return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def save(p,x): p.write_text(''.join(json.dumps(y,ensure_ascii=False)+'\n' for y in x))
remaining=rows(HERE/'BAV-006.remaining.jsonl'); keys={(x['work'],x['locator']):x for x in remaining}
candidates={}
for c in rows(HERE/'BAV-002.candidates.jsonl'):
 if (c['work'],c['locator']) in keys: candidates[(c['work'],c['locator'])]=c

covered={
 ('Chullin','79a:11'):('bavli-chullin-79a-10-davidson','Continuation already read within the adjacent context of Chullin 79a:10; lineage signs for a mule are not a new independent context.'),
 ('Shabbat','52a:14'):('bavli-shabbat-52a-5-davidson','Exact four-animal halter teaching already quoted and context-checked at Shabbat 52a:5; not double-counted.'),
}
analysis={
 ('Chullin','114b:2'):('direct','horse_mule_legal_analogy','A horse born to a mare and sibling of a mule is introduced as a counterexample in deriving the prohibition of cooking offspring with its mother. Legal analogy, not extraordinary horse lore.'),
 ('Chullin','114b:4'):('direct','horse_mule_legal_analogy','The parallel counterexample uses a mule born to a mare and sibling of a female mule to test parent–offspring food prohibitions. Ordinary breeding taxonomy.'),
 ('Gittin','14b:5'):('direct','horses_as_status_and_pursuit_capacity','The presence of fast-following horses and mules establishes that certain people are close to the government and capable of pursuit; ordinary status and enforcement capacity.'),
 ('Ketubot','66a:5'):('direct','horse_in_damages_analogy','Rava tests a theory of compensation for humiliation by asking whether embarrassing another person’s horse would incur humiliation damages, then rejects the category because a horse is not subject to shame.'),
 ('Ketubot','67a:2'):('direct','horse_hooves_poverty_image','R. Eleazar b. R. Zadok recalls an impoverished woman gathering barley from between horses’ hooves at Acre. The horse supplies a concrete degradation/poverty setting.'),
 ('Ketubot','111b:2'):('direct','mule_breeding_rule_parallel','R. Judah’s rule says a female mule in heat may be bred neither with a horse nor donkey unless with her own kind. Legal breeding classification, parallel to Chullin.'),
 ('Kiddushin','24b:10'):('direct','horse_sound_damage','A horse neighing and breaking vessels indoors is assigned half damages. The passage concerns indirect damage by sound, not supernatural agency.'),
 ('Menachot','85b:17'):('direct','horses_in_mass_oil_transport','A story of an enormous oil purchase says every available horse, mule, camel and donkey in the Land of Israel was hired for transport. Hyperbolic abundance/logistics imagery, not otherworldly travel.'),
 ('Moed Katan','10a:16'):('direct','horse_hoof_care_on_festival','Rav Hama permits trimming the nails/hooves of a ridden horse or donkey during the intermediate festival. Ordinary animal maintenance halakha.'),
 ('Moed Katan','10b:2'):('direct','horse_grooming_on_festival','Rava permits grooming a horse during the intermediate festival among other practical maintenance rulings.'),
 ('Nedarim','33a:3'):('direct','horse_use_as_food_enabling_benefit','Rav Pappa asks whether lending a horse to ride counts as a benefit that leads to food in vow law. The horse is ordinary transport enabling access.'),
 ('Shabbat','52a:9'):('direct','horse_halter_sabbath','The sugya explains whether a horse may go out or be led with its chain/halter on Shabbat. Ordinary restraint law.'),
 ('Shabbat','64a:9'):('indirect','horse_tail_hair_impurity','A scriptural derivation extends the textile category to material made from a horse’s or cow’s tail. The horse appears as a source of hair.'),
 ('Shabbat','64a:13'):('indirect','horse_tail_hair_impurity','An analogy between corpse and creeping-animal impurity asks whether horse- and cow-tail material is treated like goat hair.'),
 ('Shabbat','64a:15'):('indirect','horse_tail_hair_impurity','A verbal analogy extends the impurity rule for horse- and cow-tail material from creeping-animal impurity to corpse impurity.'),
 ('Shabbat','90b:3'):('indirect','horse_tail_hair_carrying_quantity','The carrying threshold includes two hairs from a horse’s tail, in a list of small materials and their uses.'),
 ('Shabbat','93b:1'):('direct','horse_support_and_sabbath_carrying','R. Yose says a horse transmits impurity through its forelegs because it rests its weight there; the point is used in a discussion of assistance in carrying.'),
 ('Shabbat','94a:3'):('direct','horse_as_riding_work_exception','Ben Beteira permits the horse because its characteristic work—carrying a living rider—is treated as work for which one is not liable to a sin offering.'),
 ('Sotah','13a:6'):('direct','horses_in_funeral_honour','The great mourning for Jacob is amplified by a teaching that even horses and donkeys participated/appeared in the funeral honour. Rhetorical scale, not celestial animals.'),
 ('Yevamot','98a:3'):('indirect','horse_semen_biblical_metaphor','Ezekiel’s comparison of foreign flesh to donkeys and emission to horses is cited in a legal argument about gentile kinship. Scriptural sexual metaphor, not horse travel.'),
 ('Yoma','77a:11'):('direct','horse_as_alternative_to_barefoot','In deriving the prohibition of footwear, the sugya asks whether David’s going barefoot might instead mean being without a horse and foot-rest. The horse represents ordinary mounted travel/status.'),
}
receipts=[]; sources=[]; verdicts=[]
for r in remaining:
 c=candidates[(r['work'],r['locator'])]; key=(r['work'],r['locator'])
 receipts.append({'candidate_id':r['candidate_id'],'work':r['work'],'locator':r['locator'],'export_url':c['url'],'quote':c['excerpt'],'read_scope':'complete saved target segment excerpt from BAV-002 export; adjacent API retrieval unavailable in this pass'})
 base={**r,'task_id':'BAV-007'}
 if key in covered:
  sid,reason=covered[key]; verdicts.append({**base,'verdict':'duplicate_context_covered','reason':reason,'registered_source_id':sid}); continue
 typ,role,interpretation=analysis[key]; sid=f"bavli-{r['work'].lower().replace(' ','-')}-{r['locator'].replace(':','-')}-davidson"
 sources.append({'schema_version':1,'id':sid,'corpus_id':'bavli','work':r['work'],'locator':r['locator'],'url':f"https://www.sefaria.org/{r['work'].replace(' ','_')}.{r['locator'].replace(':','.')}",'access_url':c['url'],'edition':'Sefaria merged Hebrew export (William Davidson witness family)','language':'Hebrew/Aramaic','mention_type':typ,'parent_source_id':None,'quote':c['excerpt'],'context':interpretation,'checks':{'primary_read':True,'quote_verified':True,'context_checked':True,'attribution_verified':True,'commentaries_checked':False,'interpretation_prepared':True,'independent_reviewed':False},'interpretation':interpretation,'epistemic_type':'primary_text','reviewers':['research-runner'],'task_id':'BAV-007','role':role,'limitations':['Saved complete target segment from the BAV-002 primary export was read; live adjacent-segment API retrieval timed out, so no broader daf context is claimed in this pass.','No manuscript or printed-edition collation, traditional commentary review, or independent review.'],'accessed_at':'2026-10-11'})
 verdicts.append({**base,'verdict':'accepted','reason':interpretation,'source_id':sid})
save(HERE/'BAV-007.sources.jsonl',sources); save(HERE/'BAV-007.verdicts.jsonl',verdicts); save(HERE/'BAV-007.remaining.jsonl',[])
(HERE/'BAV-007.read-excerpts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
report=f"# BAV-007 — final finite-ledger review\n\n2026-10-11. Adjudicated all {len(remaining)} entries in the saved BAV-006 remainder. The complete saved target segments from the BAV-002 Sefaria export were read; an attempted live retrieval of adjacent API segments timed out, so this pass does not claim a broader daf reading.\n\n- Separately registered contexts: **{len(sources)}** ({sum(x['mention_type']=='direct' for x in sources)} direct, {sum(x['mention_type']=='indirect' for x in sources)} indirect).\n- Already covered continuations/exact repeated teaching: **{len(covered)}**.\n- Remaining finite queue: **0**.\n\nThe entries concern breeding taxonomy, damages, poverty, transport, festival/Sabbath animal care, horse-tail material, funeral rhetoric and biblical metaphor. Menachot 85b uses mass animal transport as abundance/logistics hyperbole. **No target segment describes a horse flying, transporting a person between worlds, or independently establishes a celestial horse species.** This closes the saved BAV-002 discovery ledger, not every spelling, edition, commentary, manuscript or allusion in the Bavli.\n\nExact saved quotations and access URLs are in `BAV-007.sources.jsonl`; reading receipts are in `BAV-007.read-excerpts.json`. Commentary and independent-review flags remain false.\n"
(HERE/'BAV-007.report.md').write_text(report)
print(json.dumps({'accepted':len(sources),'covered':len(covered),'remaining':0}))
