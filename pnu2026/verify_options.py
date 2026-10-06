#!/usr/bin/env python3
"""Validate synthetic body/spine PDFs. Requires PyMuPDF; no official certification."""
import hashlib,json,re,sys
from pathlib import Path
from typing import Any
import pymupdf as fitz
ROOT=Path(__file__).resolve().parent
BUILD=ROOT/'build'
MM=72/25.4

def spans(p):
    return [s for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans']]

def main():
    docs: dict[str,Any]={n:fitz.open(BUILD/(n+'.pdf')) for n in ['spine-example','body-options-example','_test_body-defaults','_test_heading-keep']}
    s=docs['spine-example'];b=docs['body-options-example'];p=s[0]
    t=[x.get_text() for x in b]
    tests={}
    tests['spine_single_page']=len(s)==1
    tests['spine_test_width_20mm_not_a_rule']=abs(p.rect.width/MM-20)<.02
    tests['spine_height_297mm']=abs(p.rect.height/MM-297)<.02
    words=p.get_text('words')
    left=sorted([w for w in words if w[0]<20],key=lambda w:w[1])
    right=sorted([w for w in words if w[0]>29],key=lambda w:w[1])
    tests['spine_right_column_first']=''.join(w[4] for w in right)=='익명서식검증을위한세로제목'
    tests['spine_left_column_second']=''.join(w[4] for w in left)=='책등배치검증용가상논문제목'
    middle=sorted([w for w in words if 20<=w[0]<=29],key=lambda w:w[1])
    tests['spine_name_then_award_year_month']=''.join(w[4] for w in middle)=='예시자2099.2'
    tests['spine_upright_glyphs']=all(abs(l['dir'][0]-1)<.001 and abs(l['dir'][1])<.001 for block in p.get_text('dict')['blocks'] for l in block.get('lines',[]))
    tests['spine_black_text']=all(x['color']==0 for x in spans(p))
    tests['spine_fixture_font_12bp']=all(abs(x['size']-12)<.02 for x in spans(p))
    # TeX box geometry is the convention. Ink margins differ by font metrics.
    title=left+right;author=middle[:3];date=middle[3:]
    bbox=lambda ws:fitz.Rect(min(w[0] for w in ws),min(w[1] for w in ws),max(w[2] for w in ws),max(w[3] for w in ws))
    titlebox=bbox(title);authorbox=bbox(author);datebox=bbox(date)
    measurements={'ink_top_mm':titlebox.y0/MM,'ink_bottom_mm':(p.rect.height-datebox.y1)/MM,'ink_title_author_gap_mm':(authorbox.y0-titlebox.y1)/MM,'ink_author_date_gap_mm':(datebox.y0-authorbox.y1)/MM}
    tests['spine_top_20mm_with_font_metric_tolerance']=abs(measurements['ink_top_mm']-20)<1
    tests['spine_bottom_20mm_with_font_metric_tolerance']=abs(measurements['ink_bottom_mm']-20)<1
    tests['spine_title_name_10mm_with_font_metric_tolerance']=abs(measurements['ink_title_author_gap_mm']-10)<1.5
    tests['spine_name_date_10mm_with_font_metric_tolerance']=abs(measurements['ink_author_date_gap_mm']-10)<1.5
    log=(BUILD/'spine-example.log').read_text()
    dims={k:float(v)*72/72.27 for k,v in re.findall(r'PNU-SPINE-([A-Z-]+)-PT=([\d.]+)',log)}
    tests['spine_exact_box_height_budget']=abs(dims['TITLE-HEIGHT']+dims['AUTHOR-HEIGHT']+dims['DATE-HEIGHT']+60*MM-297*MM)<.02
    tests['body_seven_pages']=len(b)==7
    tests['body_first_section_with_chapter']='제1장' in t[0] and 'FIRST SECTION' in t[0]
    tests['body_second_section_new_page']='SECOND SECTION' in t[1] and 'FIRST SECTION' not in t[1]
    tests['chapter_two_first_section_with_heading']='제2장' in t[5] and 'THIRD SECTION' in t[5]
    tests['chapter_bib_one_local_entry']='Synthetic Alpha' in t[4] and 'Synthetic Beta' not in t[4]
    tests['chapter_bib_two_local_entries']='Synthetic Alpha' in t[6] and 'Synthetic Beta' in t[6]
    tests['chapter_citation_numbering']='citation [1]' in t[0] and 'Reuse [1] and another source [2]' in t[5]
    tests['figure_and_table_references']='Figure 1.1' in t[3] and '표1.1' in t[3]
    tests['english_footnote_present']='An English footnote' in t[0]
    tests['english_footnote_embedded_roman_and_italic']=any('Termes-Italic' in f[3] for f in b[0].get_fonts()) and any('Termes-Regular' in f[3] for f in b[0].get_fonts())
    tests['body_contiguous_page_numbers']=all(x.get_text(clip=fitz.Rect(0,790,x.rect.width,x.rect.height)).strip()==str(i+1) for i,x in enumerate(b))
    drawings=b[2].get_drawings();obj=max((x['rect'] for x in drawings),key=lambda x:x.height)
    caption=next(fitz.Rect(x['bbox']) for x in spans(b[2]) if 'Anonymous tall' in x['text'])
    tests['large_object_horizontal_center']=abs((obj.x0+obj.x1)/2-b[2].rect.width/2)<.1
    tests['large_object_vertical_center_in_text_area']=abs((obj.y0+caption.y1)/2-((35*MM)+(297-25)*MM)/2)<5
    tests['large_object_not_scaled']=abs(obj.height-.6*(297-35-25)*MM)<.05
    default=docs['_test_body-defaults']
    tests['default_options_preserve_same_page_sections']=len(default)==1 and all(x in default[0].get_text() for x in ['DEFAULT FIRST','DEFAULT SECOND','DEFAULT STARRED'])
    keep=docs['_test_heading-keep']
    tests['heading_reservation_moves_heading_and_paragraph']=len(keep)==2 and 'Kept heading' in keep[1].get_text() and 'KEPT WITH HEADING' in keep[1].get_text()
    fonts=[];outside=[];warnings=[]
    for name,d in docs.items():
        tests[name+'_anonymous_metadata']=not d.metadata.get('author') and not any(x in str(d.metadata) for x in ['/home/','/mnt/','C:\\','F:\\'])
        for i,page in enumerate(d):
            for word in page.get_text('words'):
                if not page.rect.contains(fitz.Rect(word[:4])):outside.append([name,i+1,word[4]])
            for font in page.get_fonts():
                fonts.append({'document':name,'font':font[3],'embedded':bool(d.extract_font(font[0])[3])})
        for line in (BUILD/(name+'.log')).read_text().splitlines():
            if any(x in line for x in ['Overfull','Missing character','undefined','Font Warning']):warnings.append([name,line])
    tests['all_fonts_embedded']=all(x['embedded'] for x in fonts)
    tests['no_outside_text']=not outside
    tests['no_unresolved_or_font_or_overflow_warnings']=not warnings
    result={'scope':'Synthetic fixtures only; width/font are test values, not PNU rules','tests':tests,'passed':all(tests.values()),'measurements':measurements,'spine_box_dimensions_bp':dims,'pages':{n:len(d) for n,d in docs.items()},'sha256':{n:hashlib.sha256((BUILD/(n+'.pdf')).read_bytes()).hexdigest() for n in docs},'fonts':fonts,'outside_text':outside,'warnings':warnings}
    (BUILD/'options-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({'tests':tests,'passed':result['passed'],'measurements':measurements},ensure_ascii=False,indent=2))
    return 0 if result['passed'] else 1
if __name__=='__main__':sys.exit(main())
