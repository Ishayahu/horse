import json,pathlib,collections
p=pathlib.Path('horse-check/research/commentaries');raw=[json.loads(l) for l in (p/'COM-003.discoveries.jsonl').read_text().splitlines()];lookup={(r['author'],r['book'],r['verse']):r for r in raw}
sel=[
('Rashi','Genesis','49:17',1,'Snake dislodges horse rider without directly touching him; the image is applied to Samson bringing down those on the roof.'),
('Rashi','Exodus','14:23',0,'Singular Pharaoh horse is explained as the entire cavalry counting as one horse before God; locally attributed to Mekhilta.'),
('Ibn Ezra','Exodus','14:9',1,'The cavalry came together rather than dispersed; this explains the collective wording.'),
('Ibn Ezra','Exodus','15:1',2,'Both proud powerful horse and powerful rider are cast into the sea; physical defeat expresses divine greatness.'),
('Ibn Ezra','Exodus','15:19',1,'Pronoun refers to horse, chariots and cavalry, with Pharaoh included in the drowning; cited psalmic parallel is part of the argument.'),
('Rashi','Judges','5:22',0,'Star heat boils the mud, causing hoof coverings to detach. Supernatural battle assistance affects ordinary horses; no transport between worlds is asserted.'),
('Metzudat David','Judges','5:22',0,'Flight from the flooding river and forceful galloping break horses heels; alternatively the strong ones are the horses themselves.'),
('Metzudat Zion','Joshua','11:6',0,'Hamstringing is interpreted as cutting the legs, the animal’s supporting foundation.'),
('Rashi','I Kings','10:28',1,'Reports an Egyptian horse trade controlled by Solomon’s merchants; explicitly marks the explanation as something heard, not independently established economic history.'),
('Rashi','I Kings','10:29',0,'Infers four horses for a chariot from relative purchase prices; preserve as commentator inference.'),
('Rashi','II Kings','7:6',0,'The Arameans seemed to hear the army sound; the comment interprets the miracle as apparent perception.'),
('Rashi','II Kings','23:11',0,'Horses were prepared to meet the sun each morning by sun worshippers; solar ritual association, not stated celestial travel.'),
('Metzudat David','II Kings','23:11',0,'Kings dedicated horses to sun worship and riding out to meet the sun in the morning; the location is earthly temple precincts.'),
('Metzudat David','II Kings','6:17',0,'Opening the servant’s eyes means seeing a spiritual thing. The wording requires independent review alongside the fire-horse context.'),
('Metzudat David','II Kings','6:17',1,'The vision quiets the servant to prevent his cries exposing Elisha; actual aid comes through the attackers’ blindness. It is a protective vision, not an asserted equine journey.'),
('Metzudat Zion','Isaiah','31:3',0,'Spirit is glossed as angel by an Isaiah parallel. It does not identify Egyptian fleshly horses as spirits.'),
('Metzudat David','Isaiah','63:13',0,'Israel traverses the sea depth as an unimpeded horse runs on level wilderness; horse is the simile of smooth passage.'),
('Metzudat David','Isaiah','66:20',0,'Foreign nations bring dispersed Israelites by ordinary mounts and vehicles after the Gog and Magog event; transport destination is Jerusalem, not another world.'),
('Rashi','Jeremiah','12:5',1,'Preserves two readings: threatening Judah’s leaders beyond local priests; rabbinic comparison of Nebuchadnezzar’s few steps and reward to righteous people running like horses. No literal spirit mount.'),
('Metzudat David','Jeremiah','5:8',0,'Well-fed horses at dawn illustrate adulterers’ satisfied desire and rejoicing.'),
('Metzudat David','Jeremiah','8:6',2,'Warhorse rushing into danger is a simile for people rushing into evil and destroying themselves.'),
('Metzudat David','Jeremiah','51:27',2,'Horse hair stiffening is interpreted as a battle trait of strong courageous horses; animal behaviour in military imagery.'),
('Rashi','Ezekiel','23:20',2,'Equine emission imagery means abundant sexual activity; sexual metaphor, not a mystical vehicle.'),
('Metzudat Zion','Ezekiel','27:14',1,'Mules are defined as offspring of ass and horse, clarifying species in the trade list.'),
('Metzudat David','Ezekiel','39:20',0,'Birds and beasts eat horses fallen in battle and their riders; battlefield consumption imagery.'),
]
records=[]
for a,b,v,i,interp in sel:
 r=lookup[a,b,v];q=r['segments'][i];assert q
 cache=json.load(open('/tmp/horse-com003-cache/'+r['title'].replace(' ','_')+'.json'));d=cache['data'];hv=[x for x in d.get('versions',[]) if x.get('language')=='he']
 edition='Sefaria default Hebrew book response; available version metadata: '+' | '.join(x.get('versionTitle','') for x in hv)
 records.append(dict(id='commentary:'+a.replace(' ','-')+':'+r['parent_source_id'].removeprefix('tanakh-wlc-')+':seg'+str(i+1),corpus_id='traditional-commentaries',work=r['title'],locator=v+':'+str(i+1),url=r['api_url'],edition=edition,language='he',mention_type='direct' if any(x in q for x in ['סוס','סּוּס']) else 'indirect',parent_source_id=r['parent_source_id'],quote=q,context='Entire verse commentary cell read. Exact segment '+str(i+1)+' after HTML removal; explicit index title '+str(r['index_title'])+'. Index URL '+r['index_url'],checks=dict(primary_read=True,quote_verified=True,context_checked=True,attribution_verified=True,commentaries_checked=False,interpretation_prepared=True,independent_reviewed=False),interpretation=interp,epistemic_type='traditional_commentary',reviewers=['COM-003 worker'],task_id='COM-003',limitations=['Default API Hebrew response may combine available digital versions; metadata list does not identify a collated print witness.','No independent review.'],accessed_at='2026-10-10'))
(p/'COM-003.sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records));print(len(records))
