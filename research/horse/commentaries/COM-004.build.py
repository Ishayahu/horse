#!/usr/bin/env python3
"""Normalize the saved COM-004 Abarbanel/Ibn Ezra Zechariah discoveries."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; P=ROOT/'research/commentaries'
rows=[json.loads(x) for x in (P/'COM-004.discoveries.jsonl').read_text().splitlines() if x.strip()]
skip={('Ibn Ezra','6:4')}
interp={
('Abarbanel','1:8'):'Abarbanel rejects reducing every detail to separate intellects and spheres, frames the difficult vision within the four kingdoms, and insists prophetic details are meaningful; he records the Talmudic divine-rider reading as a question, not yet his complete horse interpretation.',
('Abarbanel','6:1'):'The four horse chariots represent four world empires and their component kingdoms; they are distinct from the first vision’s horses. The mountains mark world bounds or the two Temples. Political-historical allegory, not horse transport between worlds.',
('Abarbanel','6:2'):'Red horses symbolize bloodshed by Babylon; black horses symbolize Persia through dress, defeat, or Israel’s darkened condition under Haman.',
('Abarbanel','6:3'):'White horses symbolize Greece, linked conjecturally to Greek white dress; dappled/strong horses symbolize the combined and later divided Roman/Christian and Islamic powers.',
('Abarbanel','6:4'):'The four winds are four world empires authorised by heaven and correlated with four cosmic quarters and earthly directions. The chariot-horse image is political-cosmic allegory, not literal celestial zoology.',
('Abarbanel','6:6'):'Horse colours and directions map successive empires and conquests: Persia against Babylon, Greece after Persia, and Roman/Islamic power toward the south.',
('Abarbanel','6:7'):'The strong horses’ request to traverse the earth signifies imperial expansion and conquest under heavenly permission.',
('Abarbanel','6:8'):'Persian conquest satisfies divine anger against Babylon; Abarbanel also preserves a long Pesikta reading linking the chariots to Israel’s camps and four empires, plus a divine-rider interpretation of the first vision. These are attributed traditions, not proof of literal cosmic horse travel.',
('Ibn Ezra','1:8'):'Angelic agents are compared to a king’s mounted messengers who travel quickly and report on the realm. The rider is an angel; Ibn Ezra declines symbolic explanations of the red colour and treats the riderless coloured horses as visionary forms.',
('Ibn Ezra','6:1'):'Each chariot has four horses; the two mountains signify decrees or the heavenly court. Concise visionary explanation without literal interworld transport claim.',
('Ibn Ezra','6:2'):'The horses are identified with those of the first Zechariah vision.',
('Ibn Ezra','6:3'):'The first three chariots have single distinct colours; the fourth combines dappled and strong/intense colouring.',
('Ibn Ezra','6:5'):'The four winds are decrees going to the four ends of the earth from standing before God.',
('Ibn Ezra','6:6'):'The coloured chariots are directed north and south, especially toward the Jewish communities of Babylon and Persia.',
('Ibn Ezra','6:7'):'The strong/red horses traverse east and west by command of the Lord of all the earth; they are obedient visionary agents, without a mechanism of passage between worlds.',
('Ibn Ezra','6:8'):'The black horses execute divine vengeance in the north; the vision reassures Israel that northern exiles and Jerusalem will be secure.'}
out=[]
for d in rows:
 key=(d['author'],d['verse'])
 if key in skip: continue
 author=d['author'].replace(' ','-'); loc=d['verse']; parent=f"tanakh-wlc-zech-{loc.replace(':','-')}"
 out.append({'schema_version':1,'id':f"commentary:{author}:zech-{loc.replace(':','-')}:cell",'corpus_id':'traditional-commentaries','work':d['title'],'locator':loc,'url':d['api_url'],'edition':'Sefaria default Hebrew book response; version metadata preserved in COM-004.manifest.json','language':'he','mention_type':'direct','parent_source_id':parent,'quote':'\n'.join(d['segments']),'context':'Entire saved verse commentary cell read; HTML removed. '+interp[key],'checks':{'primary_read':True,'quote_verified':True,'context_checked':True,'attribution_verified':True,'commentaries_checked':False,'interpretation_prepared':True,'independent_reviewed':False},'interpretation':interp[key],'epistemic_type':'traditional_commentary','reviewers':['research-runner'],'task_id':'COM-004','role':'zechariah_horse_vision_interpretation','limitations':['Default digital Hebrew response may combine versions; no print/manuscript collation.','No independent review; historical identifications are preserved as Abarbanel/Ibn Ezra interpretations, not externally verified history.'],'accessed_at':'2026-10-11'})
(P/'COM-004.sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out))
(P/'COM-004.report.md').write_text(f"# COM-004 — Abarbanel and Ibn Ezra on Zechariah horse visions\n\nNormalized **{len(out)}** meaningful verse-commentary cells from the saved finite matrix (8 Abarbanel, 8 Ibn Ezra); one Ibn Ezra cell at Zechariah 6:4 merely marks narrative continuity and was not promoted. Coverage: 17 present, 3 empty and 13 unavailable-title cells. Missing titles and empty exact verses do not prove absence in print or grouped comments.\n\nAbarbanel reads Zechariah 6 primarily as the four empires under divine government, with horse colours representing Babylon, Persia, Greece and Rome/Islam; he also preserves attributed midrashic/divine-rider readings. Ibn Ezra treats the agents as angelic/mounted-messenger imagery, stresses speed and obedience, and often declines speculative colour symbolism. Neither commentator here describes winged horses or supplies a mechanism by which horses carry humans between worlds. Visionary and angelic agency is not promoted to literal celestial zoology.\n\nExact Hebrew cells, URLs, coverage and version metadata remain in the COM-004 artifacts. No independent review or manuscript/print collation was added.\n")
print({'sources':len(out),'skipped_nonmeaningful':1})
