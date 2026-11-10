from cad_common import *
p=ROOT/'cad_editorial_changes.json'; a=json.loads(p.read_text())
fix={'within20':'within 20','CLP1500':'CLP 1500','demand2672':'demand 2672','two2500':'two 2500','seven1140':'seven 1140','normally-open4P':'normally-open 4P','rear1000':'rear 1000','front1800':'front 1800','sides750':'sides 750','terminals900':'terminals 900','front1500':'front 1500','rear990':'rear 990','width7980':'width 7980','Proposed2':'Proposed 2','FFL150':'FFL 150','opening4000':'opening 4000','openings3000':'openings 3000','height2800':'height 2800','at90':'at 90','B:630':'B: 630','/30':'/ 30','/700':'/ 700','each4500':'each 4500','at70':'at 70','at1 ':'at 1 ','B:600':'B: 600','x2000':'x 2000','total1.20':'total 1.20','ducts:900':'ducts: 900','x750':'x 750','Task1':'Task 1','current14':'current 14','TM63D70':'TM63D 70','Task3':'Task 3','Controls:20':'Controls: 20','LIGHTING:92':'LIGHTING: 92','/2256':'/ 2256','Task2':'Task 2','four38':'four 38','at2.2':'at 2.2','controls20':'controls 20','/LED':'/ LED','/4C35':'/ 4C35','+CPC16':'+ CPC16'}
for c in a['text_changes']:
 e=doc.HandleToObject(c['handle']); t=e.TextString
 for x,y in fix.items():t=t.replace(x,y)
 settext(c['handle'],t);c['after']=t
finish('rev04_spacing');p.write_text(json.dumps(a,indent=2))
