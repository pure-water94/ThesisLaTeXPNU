#!/usr/bin/env python3
"""Build with Tectonic (BibTeX included); never enables shell escape.
python build.py --tectonic /path/to/tectonic --test
python build.py --tectonic /path/to/tectonic --input main.tex
python build.py --tectonic /path/to/tectonic --final
"""
import argparse,json,os,shutil,subprocess,sys
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

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--tectonic',default=os.environ.get('TECTONIC') or shutil.which('tectonic'));ap.add_argument('--input',default='example.tex');ap.add_argument('--test',action='store_true');ap.add_argument('--final',action='store_true');args=ap.parse_args()
    if not args.tectonic:ap.error('Install Tectonic, then set --tectonic or TECTONIC. See README.')
    engine=str(Path(args.tectonic).resolve()) if Path(args.tectonic).exists() else args.tectonic
    if args.test and args.final:ap.error('--test and --final cannot be combined')
    if args.test:
        cases=[('example.tex',None),('main.tex',None),('tests/two-page-abstracts.tex',None),('tests/missing-metadata.tex','Missing final metadata'),('tests/abstract-too-long.tex','exceeds two pages'),('tests/title-overflow.tex','Cover title overlaps author area'),('tests/missing-department.tex','Missing final metadata: department-ko')]
        reports=[run(engine,*case) for case in cases]
        (ROOT/'build/test-results.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
        return 0 if all(x['passed'] for x in reports) else 1
    if args.final:
        wrapper=ROOT/'release-main.tex'
        if wrapper.exists():ap.error('release-main.tex already exists; refusing to overwrite')
        wrapper.write_text('\\def\\PNUFinal{1}\n\\input{main.tex}\n')
        try:return 0 if run(engine,wrapper.name)['passed'] else 1
        finally:wrapper.unlink(missing_ok=True)
    return 0 if run(engine,args.input)['passed'] else 1
if __name__=='__main__':sys.exit(main())
