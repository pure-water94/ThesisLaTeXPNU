#!/usr/bin/env python3
"""Build with Tectonic (BibTeX included); never enables shell escape.
python build.py --tectonic /path/to/tectonic --test
python build.py --tectonic /path/to/tectonic --input main.tex
python build.py --tectonic /path/to/tectonic --final
"""
import argparse,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def run(engine, source, expected_error=None):
    out=ROOT/'build';out.mkdir(exist_ok=True)
    wrapper=None
    engine_source=source
    if Path(source).parent != Path('.'):
        wrapper=ROOT/('_test_'+Path(source).stem+'.tex')
        if wrapper.exists():raise FileExistsError(wrapper)
        wrapper.write_text('\\input{'+source+'}\n')
        engine_source=wrapper.name
    try:
        result=subprocess.run([engine,'--untrusted','--keep-logs','--keep-intermediates','--outdir','build',engine_source],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
    finally:
        if wrapper:wrapper.unlink(missing_ok=True)
    text=result.stdout
    (out/(Path(source).stem+'.console.txt')).write_text(text,encoding='utf-8')
    passed=(result.returncode==0) if expected_error is None else (result.returncode!=0 and expected_error in text)
    report={'source':source,'exit_code':result.returncode,'expected_error':expected_error,'passed':passed}
    print(json.dumps(report,ensure_ascii=False))
    if not passed:print(text)
    return report

def run_chapters(engine, source):
    """Run real BibTeX via Tectonic drivers for literal chapterbib includes.

    Tectonic 0.17 does not automatically process chapter .aux bibliographies.
    Never overwrite an existing .bbl; temporary drivers/results are removed.
    """
    first=run(engine,source)
    if not first['passed']:return first
    aux=ROOT/'build'/(Path(source).stem+'.aux')
    children=re.findall(r'\\@input\{([^{}]+\.aux)\}',aux.read_text())
    created=[]
    try:
        for child in children:
            relative=Path(child)
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('Only relative in-project chapter paths are supported')
            text=(ROOT/'build'/relative).read_text()
            data=re.findall(r'\\bibdata\{([^{}]+)\}',text)
            if not data:continue
            styles=re.findall(r'\\bibstyle\{([^{}]+)\}',text)
            cites=re.findall(r'\\citation\{([^{}]+)\}',text)
            if len(data)!=1 or len(styles)!=1 or not cites:
                raise ValueError('Expected one BibTeX database/style and citations per chapter')
            target=(ROOT/relative).with_suffix('.bbl')
            if not target.resolve().is_relative_to(ROOT):
                raise ValueError('Chapter path resolves outside the project')
            if target.exists():raise FileExistsError('Refusing to overwrite an existing chapter .bbl')
            with tempfile.NamedTemporaryFile(mode='w',prefix='_test_bib_',suffix='.tex',dir=ROOT,delete=False) as f:
                driver=Path(f.name)
                f.write('\\documentclass{article}\n\\begin{document}\n'+
                        '\\nocite{'+','.join(cites)+'}\n\\bibliographystyle{'+styles[0]+'}\n'+
                        '\\bibliography{'+data[0]+'}\n\\end{document}\n')
            try:
                result=run(engine,driver.name)
                if not result['passed']:return result
                target.write_bytes((ROOT/'build'/driver.with_suffix('.bbl').name).read_bytes())
                created.append(target)
            finally:driver.unlink(missing_ok=True)
        if not created:raise ValueError('No chapter bibliographies found')
        report=run(engine,source)
        log=(ROOT/'build'/(Path(source).stem+'.log')).read_text()
        unresolved=bool(re.search(r'(?:Citation|Reference).*undefined|There were undefined',log))
        report['unresolved_references']=unresolved
        report['passed']=report['passed'] and not unresolved
        report['chapter_bibliographies']=len(created)
        return report
    finally:
        for target in created:target.unlink(missing_ok=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--tectonic',default=os.environ.get('TECTONIC') or shutil.which('tectonic'));ap.add_argument('--input',default='example.tex');ap.add_argument('--test',action='store_true');ap.add_argument('--final',action='store_true');ap.add_argument('--chapter-bib',action='store_true');args=ap.parse_args()
    if not args.tectonic:ap.error('Install Tectonic, then set --tectonic or TECTONIC. See README.')
    engine=str(Path(args.tectonic).resolve()) if Path(args.tectonic).exists() else args.tectonic
    if args.test and args.final:ap.error('--test and --final cannot be combined')
    if args.test:
        cases=[('example.tex',None),('main.tex',None),('tests/two-page-abstracts.tex',None),('tests/missing-metadata.tex','Missing final metadata'),('tests/abstract-too-long.tex','exceeds two pages'),('tests/title-overflow.tex','Cover title overlaps author area'),('tests/missing-department.tex','Missing final metadata: department-ko')]
        cases.extend([('spine-example.tex',None),('tests/body-defaults.tex',None),('tests/heading-keep.tex',None),('tests/spine-missing-width.tex','Missing positive spine width'),('tests/spine-missing-font.tex','Missing positive spine font-size'),('tests/spine-too-narrow.tex','Spine too narrow'),('tests/spine-too-long.tex','Title column exceeds available height'),('tests/object-too-tall.tex','Object exceeds text height'),('spine.tex','Missing local-spine.tex')])
        reports=[run(engine,*case) for case in cases]
        reports.append(run_chapters(engine,'body-options-example.tex'))
        (ROOT/'build/test-results.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
        return 0 if all(x['passed'] for x in reports) else 1
    if args.final:
        wrapper=ROOT/'release-main.tex'
        if wrapper.exists():ap.error('release-main.tex already exists; refusing to overwrite')
        wrapper.write_text('\\def\\PNUFinal{1}\n\\input{main.tex}\n')
        try:
            runner=run_chapters if args.chapter_bib else run
            return 0 if runner(engine,wrapper.name)['passed'] else 1
        finally:wrapper.unlink(missing_ok=True)
    runner=run_chapters if args.chapter_bib else run
    return 0 if runner(engine,args.input)['passed'] else 1
if __name__=='__main__':sys.exit(main())
