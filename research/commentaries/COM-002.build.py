import json,re,html,pathlib,collections
p=pathlib.Path('horse-check/research/commentaries');xs=json.loads((p/'COM-002.raw.json').read_text())
def clean(s):return html.unescape(re.sub('<[^>]+>','',s))
# All quoted segments below are drawn verbatim from the fetched Hebrew, with markup removed only.
sel=[
('Malbim','Job','39:19',0,'Providence gives the horse its usefulness for riding, burden, work and especially war; the ancient poets observation is Malbim’s own nineteenth-century statement, not evidence of ancient borrowing.'),
('Malbim','Job','39:25',0,'God plants battle perception in the horse’s nature. Smelling war and recognising commanders’ signals are natural endowments in this comment, not interworld movement.'),
('Rashi','Job','39:24',1,'The horse’s disbelief is delight and appetite for battle. A behavioural explanation of the poetic warhorse.'),
('Rashi','Song of Songs','1:9',0,'Rashi reports an aggadic reading of God’s assembled horse-camps at the sea to save Israel, linking Habakkuk 3:15 and Exodus 14:14. This is a traditional divine military image, without a claim of transport between worlds.'),
('Ibn Ezra','Song of Songs','1:9',3,'In the third interpretive pass, the mare/harness becomes Israel’s keeping the yoke of commandments, followed by reward from Egypt. Preserve distinction from the first lexical and second literary passes.'),
('Malbim','Song of Songs','1:9',1,'In the explicitly labelled melitzah the divine soul is God’s mare, bodily powers are Pharaoh’s chariots, and the small bodily chariot should follow the divine governance of the whole cosmos. This is a psychological/cosmological allegory, not a literal journey by a horse.'),
('Radak','Psalms','33:17',0,'Horse strength is God-given (explicit Job 39:19 cross-reference); God can make it fail, so the rider cannot treat it as guaranteed salvation.'),
('Ibn Ezra','Psalms','147:10',0,'Reads human shanks as the rider and opposes reliance on strength to fear of God; explicitly links Job 39:19.'),
('Metzudat David','Psalms','147:10',0,'Condemns the person who places trust in a horse’s strength for pursuit in war, clarifying that the object is misplaced reliance.'),
('Malbim','Psalms','20:8',0,'The psalmic speaker, seeing salvation above nature, says he will make no further military preparations. This stronger claim belongs to Malbim’s local exposition, not a universal halakhic rule.'),
('Ibn Ezra','Isaiah','31:3',0,'Glosses רוח as an angel (Isaiah 48:16 parallel). The contrast is flesh and angelic spirit; the comment itself does not establish literal spirit-horses.'),
('Malbim','Isaiah','31:3',0,'Contrasts Egyptian human warriors and fleshly horses with God and the angelic spirits serving as his instruments of war. Does not identify the Egyptian horses as angels or assert transport.'),
('Rashi','Deuteronomy','20:1',2,'The entire enemy cavalry is as one horse in God’s eyes; Rashi supports the singular wording with Judges 6 and Exodus 15. This is scaling of divine power, not numerical census.'),
('Or HaChaim','Deuteronomy','20:1',1,'In a explicitly tentative allegorical reading (אולי at opening), horse means the battle-trained evil inclination, chariot the person’s composition, and large host acquired evil powers. Divine help enables purification; not an equine vehicle between worlds.'),
('Kli Yakar','Deuteronomy','20:1',1,'The united enemy is initially as one horse/chariot; God then divides the alliance. Horse/chariot language becomes an image of political cohesion and providential disunion.'),
('Rashi','Exodus','15:1',2,'Horse and rider remain bound as waters lift them and bring them into depth; attributed locally to Mekhilta. Physical drowning motif; the final רמה gloss adds up/down imagery without an otherworldly destination.'),
('Kli Yakar','Exodus','15:1',3,'Rider’s elevation over his horse is read as pride and a larger fall, supporting the theme of God humbling the proud.'),
]
base={'Job':'job','Song of Songs':'song','Psalms':'ps','Isaiah':'isa','Deuteronomy':'deut','Exodus':'exod'}
existing={json.loads(l)['id'] for l in open('horse-check/data/sources.jsonl')}
records=[]
for a,b,v,i,interp in sel:
 x=next(x for x in xs if (x['author'],x['book'],x['verse'])==(a,b,v));d=x['data'];hs=d['he'];assert i<len(hs),(x['ref'],len(hs),i)
 bid='tanakh-wlc-'+base[b]+'-'+v.replace(':','-');bid=bid if bid in existing else bid+'-indirect';assert bid in existing,bid
 q=clean(hs[i]);assert q
 records.append(dict(id='commentary:'+a.replace(' ','-')+':'+base[b]+':'+v,corpus_id='traditional-commentaries',work=d['book'],locator=v+':'+str(i+1),url=x['api_url'],edition=d.get('heVersionTitle','')+'; source '+d.get('heVersionSource',''),language='he',mention_type='indirect' if (a,b,v) in [('Rashi','Job','39:24'),('Ibn Ezra','Isaiah','31:3')] else 'direct',parent_source_id=bid,quote=q,context='Full author-labelled verse response read; quotation is segment '+str(i+1)+' with HTML tags removed. '+('Contains internal allegory labels משל/מליצה.' if b=='Song of Songs' and a=='Malbim' else ''),checks=dict(primary_read=True,quote_verified=True,context_checked=True,attribution_verified=True,commentaries_checked=False,interpretation_prepared=True,independent_reviewed=False),interpretation=interp,epistemic_type='traditional_commentary',reviewers=['COM-002-worker'],task_id='COM-002',limitations=['Online edition attribution accepted; no manuscript/printed-edition collation.','No independent review.'],accessed_at='2026-10-10'))
(p/'COM-002.sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
grid=[]
for x in xs:
 d=x['data'];h=d.get('he');s='present' if h else 'missing' if d.get('error') else 'empty' if 'he' in d else 'unavailable'
 grid.append(dict(author=x['author'],book=x['book'],verse=x['verse'],status=s,meaning='API title/ref not found; not proof of absence in all editions' if s=='missing' else 'No Hebrew segment returned at this reference' if s=='empty' else 'Hebrew returned, but not all units selected/read in depth',api_url=x['api_url'],error=d.get('error') or d.get('fetch_error'),selected=any((a,b,v)==(x['author'],x['book'],x['verse']) for a,b,v,i,j in sel),edition=d.get('heVersionTitle')))
(p/'COM-002.coverage.json').write_text(json.dumps(dict(schema_version=1,task_id='COM-002',cells=grid,counts=dict(collections.Counter(r['status'] for r in grid))),ensure_ascii=False,indent=2))
print(len(records),collections.Counter(r['status'] for r in grid))
for r in records:print(r['id'],r['quote'][:90])
