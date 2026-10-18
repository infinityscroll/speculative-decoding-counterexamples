from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
base=Path(__file__).resolve().parent
manifest=json.loads((base/'MANIFEST.json').read_text())
for name,expected in manifest['files'].items():
    data=(base/name).read_bytes()
    assert len(data)==expected['bytes'] and hashlib.sha256(data).hexdigest()==expected['sha256'],name
ignore={'cpu_seconds'}
def stable(d):return {k:v for k,v in d.items() if k not in ignore}
with tempfile.TemporaryDirectory(prefix='decoding addendum ') as tmp:
    work=Path(tmp)
    for folder in ['repair','repair-review','relevance']:
        shutil.copytree(base/folder,work/folder)
    for file,expected_name,output_name in [
        ('repair/check_repair.py','repair/RESULT.json','repair/RESULT.json'),
        ('repair-review/check_independently.py','repair-review/CHECKS.json',None),
        ('relevance/check_constants.py','relevance/RESULT.json','relevance/RESULT.json')]:
        script=work/file
        command=[sys.executable,'-I','-B','-c',"import runpy,sys;sys.path.insert(0,sys.argv[1]);runpy.run_path(sys.argv[2],run_name='__main__')",str(script.parent),str(script)]
        run=subprocess.run(command,cwd=tmp,capture_output=True,text=True,check=True)
        actual=json.loads((work/output_name).read_text()) if output_name else json.loads(run.stdout)
        expected=json.loads((base/expected_name).read_text())
        assert stable(actual)==stable(expected),file
print(json.dumps({'status':'PASS_PORTABLE_REPAIR_AND_RELEVANCE_CHECKS','two_draft_corrected_example':'67/70','arbitrary_vocab_gap_lower_pp':'7.400686735493136','analytic_proofs':'Read repair/PROOF.md and relevance/PROOF.md; not inferred from finite tests','external_human_review':'UNVERIFIED','paid_compute':0},indent=2))
