"""Verify integrity, then rerun the exact checks without modifying this packet."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

base=Path(__file__).resolve().parent
manifest=json.loads((base/'MANIFEST.json').read_text())
for name,record in manifest['files'].items():
    data=(base/name).read_bytes()
    assert len(data)==record['bytes'] and hashlib.sha256(data).hexdigest()==record['sha256'], name
with tempfile.TemporaryDirectory(prefix='decoding proof ') as tmp:
    work=Path(tmp)
    for sub in ['root','independent','family','family-independent']:
        shutil.copytree(base/sub,work/sub)
    for name in ['root/verify.py','root/verify_rrs.py','independent/independent_replay.py','family/certificate.py','family-independent/check.py']:
        subprocess.run([sys.executable,'-I','-B',str(work/name)],check=True,capture_output=True,text=True,cwd=tmp)
    for name in ['root/REPLAY.json','root/RRS-REPLAY.json','independent/REPLAY.json']:
        assert json.loads((base/name).read_text())==json.loads((work/name).read_text()), name
    ignored={'cpu_seconds','script_sha256','original_manifest_sha256','original_packet_unchanged','source_pdf_sha256','declared_source_pdf_sha256'}
    for name in ['family/RESULT.json','family-independent/RESULT.json']:
        expected={k:v for k,v in json.loads((base/name).read_text()).items() if k not in ignored}
        actual={k:v for k,v in json.loads((work/name).read_text()).items() if k not in ignored}
        assert expected==actual, name
addon_run=subprocess.run([sys.executable,'-I','-B',str(base/'addendum/verify_all.py')],check=True,capture_output=True,text=True)
addon_result=json.loads(addon_run.stdout)
assert addon_result['status']=='PASS_PORTABLE_REPAIR_AND_RELEVANCE_CHECKS'
print(json.dumps({'status':'PASS_ORIGINAL_FAMILY_REPAIR_AND_RELEVANCE',
                  'original_formula':'19/20','original_optimum':'1','original_RRS':'191/200',
                  'family_V4_formula':'1','family_V4_optimum':'161/176',
                  'family_V8_formula':'1','family_V8_optimum':'6580499/8230200',
                  'asymptotic_claim':'See family/PROOF.md and family-independent/REVIEW.md; not inferred from finite enumeration',
                  'constructive_repair_and_relevance':addon_result,
                  'paid_compute':0,'source_PDF_reextracted_by_this_command':False,
                  'novelty_and_external_review':'UNVERIFIED'},indent=2))
