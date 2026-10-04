#!/usr/bin/env python3
"""PDF checks for the anonymous example fixture; not university certification.
Requires PyMuPDF. Run after `python build.py --test`.
"""
import json,re,sys,hashlib
from pathlib import Path
from typing import Any
import pymupdf as fitz
ROOT=Path(__file__).resolve().parent
norm=lambda s:re.sub(r'\s+','',s)
def lines(page):
    result=[]
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            result.append({'text':''.join(s['text'] for s in l['spans']),'size':sorted(set(round(s['size'],3) for s in l['spans'])),'bbox_pt':list(l['bbox'])})
    return result

def main():
    pdf=ROOT/'build/example.pdf';d: Any=fitz.open(pdf);texts: list[str]=[str(p.get_text()) for p in d]
    body=next(i for i,t in enumerate(texts) if '첫등장문헌은' in norm(t))
    ko=next(i for i,t in enumerate(texts) if '\n요약\n' in t)
    en=next(i for i,t in enumerate(texts) if 'Example Author' in t)
    bib=next(i for i,t in enumerate(texts) if 'Flavio Cioli' in t)
    toc=next(i for i,t in enumerate(texts) if '\n목차\n' in t)
    lot=next(i for i,t in enumerate(texts) if t.splitlines()[1:2]==['표목차'])
    lof=next(i for i,t in enumerate(texts) if t.splitlines()[1:2]==['그림목차'])
    footer=lambda p: p.get_text(clip=fitz.Rect(0,790,p.rect.width,p.rect.height)).strip()
    out=[];records=[];embedded={};counts={}
    for i,p in enumerate(d):
        bad=[w[:5] for w in p.get_text('words') if w[0]<-0.5 or w[1]<-0.5 or w[2]>p.rect.width+0.5 or w[3]>p.rect.height+0.5]
        out.extend([{'page':i+1,'word':x} for x in bad])
        records.append({'page':i+1,'footer':footer(p),'characters':len(texts[i]),'links':len(p.get_links())})
        for ft in p.get_fonts():
            if ft[0] not in embedded:
                content=d.extract_font(ft[0]);embedded[ft[0]]={'name':ft[3],'embedded':bool(content[3])}
    lcover=lines(d[0]);lapproval=lines(d[2]);lko=lines(d[ko]);len_=lines(d[en])
    def sizes_of(items,marker):return [v for x in items if marker in norm(x['text']) for v in x['size']]
    def exact(values,size):return bool(values) and all(abs(v-size)<0.03 for v in values)
    bbl=(ROOT/'build/example.bbl').read_text()
    log=(ROOT/'build/example.log').read_text()
    warnings=[l for l in log.splitlines() if any(s in l for s in ['Overfull','Missing character','undefined','Font Warning'])]
    tests={
     'A4_all_pages':all(abs(p.rect.width*25.4/72-210)<0.1 and abs(p.rect.height*25.4/72-297)<0.1 for p in d),
     'blank_after_cover':not texts[1].strip() and not d[1].get_images() and not d[1].get_drawings(),
     'cover_degree_16bp':exact(sizes_of(lcover,'박사학위논문')[:1],16),
     'cover_title_22bp':exact(sizes_of(lcover,'부산대학교의학과공통'),22),
     'cover_author_16bp':exact(sizes_of(lcover,'예시저자'),16),
     'cover_affiliation_16bp':exact(sizes_of(lcover,'부산대학교대학원'),16),
     'cover_text_black':all(s['color']==0 for b in d[0].get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['size']>8.1),
     'approval_title_22bp':exact(sizes_of(lapproval,'부산대학교의학과공통'),22),
     'approval_affiliation_14bp':exact(sizes_of(lapproval,'부산대학교대학원'),14),
     'ko_abstract_title_14bp':exact(sizes_of(lko,'부산대학교의학과공통'),14),
     'ko_abstract_author_12bp':exact(sizes_of(lko,'예시저자'),12),
     'ko_abstract_affiliation_11bp':exact(sizes_of(lko,'부산대학교대학원'),11),
     'ko_abstract_heading_12bp':exact([v for x in lko if norm(x['text'])=='요약' for v in x['size']],12),
     'en_abstract_title_14bp':exact(sizes_of(len_,'AnExampleforVerifying'),14),
     'en_abstract_author_12bp':exact(sizes_of(len_,'ExampleAuthor'),12),
     'en_abstract_affiliation_11bp':exact(sizes_of(len_,'DepartmentofExampleStudies'),11),
     'en_abstract_heading_12bp':exact([v for x in len_ if norm(x['text'])=='Abstract' for v in x['size']],12),
     'approval_submission_16bp':exact(sizes_of(lapproval,'제출함'),16),
     'approval_statement_16bp':exact(sizes_of(lapproval,'인준함'),16),
     'committee_5_rows':sum(1 for x in lapproval if norm(x['text']) in ['위원','위원장'])==5,
     'committee_14bp':exact([s for x in lapproval if norm(x['text']) in ['위원','위원장'] for s in x['size']],14),
     'ko_abstract_body_11bp':exact(sizes_of(lko,'이문서는연구결과가아니라'),11),
     'en_abstract_body_11bp':exact(sizes_of(len_,'Thisdocumentisananonymous'),11),
     'required_order':0<1<2<toc<lot<lof<ko<body<bib<en,
     'body_starts_1':footer(d[body])=='1',
     'body_numbers_contiguous':all(footer(d[i])==str(i-body+1) for i in range(body,len(d))),
     'front_roman':footer(d[toc])=='I' and bool(re.fullmatch('[IVXLCDM]+',footer(d[ko]))),
     'cite_first_appearance':bbl.index('{cioli2022}')<bbl.index('{salonitis2016}'),
     'crossrefs_resolved':all('??' not in t for t in texts),
     'hyperlinks_present':sum(x['links'] for x in records)>0,
     'raster_image_not_suppressed':sum(len(p.get_images()) for p in d)>0,
     'no_outside_text':not out,
     'fonts_embedded':all(x['embedded'] for x in embedded.values()),
     'no_font_or_overfull_warnings':not warnings,
     'abstract_reported_limits':'PNU-ABSTRACT-ko-PAGES=1' in log and 'PNU-ABSTRACT-en-PAGES=1' in log
    }
    measurements={str(i+1):lines(d[i]) for i in [0,2,ko,en]}
    result={'scope':'anonymous example fixture only; no official certification','pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':len(d),'tests':tests,'passed':all(tests.values()),'pages_detail':records,'font_embeddings':list(embedded.values()),'warnings':warnings,'outside_text':out,'front_measurements':measurements}
    (ROOT/'build/pdf-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({k:result[k] for k in ['pages','tests','passed']},ensure_ascii=False,indent=2))
    return 0 if result['passed'] else 1
if __name__=='__main__':sys.exit(main())
