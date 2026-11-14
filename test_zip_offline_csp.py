"""Reject ZIPs with changed CSP even when their manifest SHA is recomputed.

All sources synthetic. This tests structural CSP compatibility, NOT signing
or publisher/source authenticity and not an independent human security audit.
"""
from __future__ import annotations
import hashlib
import json
import struct
import tempfile
import unittest
import warnings
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_STORED

from data2web_single import deliver_single
from verify_delivery import verify_zip


class ZipOfflineCsp(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.source=self.root/"synthetic.csv"
        original=b"id,title,category\n1,Synthetic,A\n"
        self.source.write_bytes(original)
        delivery=self.root/"delivery"
        deliver_single(self.source,delivery,expected_sha256=hashlib.sha256(original).hexdigest(),
                       id_column="id",title_column="title",category_column="category",
                       confirm="APPROVE",ack_plaintext=True,
                       privacy_classification="NO_PERSONAL_DATA_REVIEWED")
        self.archive=delivery/"delivery.zip"
        with ZipFile(self.archive,"r") as z:
            self.members={name:z.read(name) for name in z.namelist()}

    def rebuild_with_html(self, changed):
        members=dict(self.members)
        members["index.html"]=changed
        manifest=json.loads(members["manifest.json"])
        manifest["html_sha256"]=hashlib.sha256(changed).hexdigest()
        members["manifest.json"]=(json.dumps(
            manifest,sort_keys=True,separators=(",",":"),ensure_ascii=False
        )+"\n").encode("utf-8")
        output=self.root/("modified-"+str(len(list(self.root.glob("modified-*.zip"))))+".zip")
        with ZipFile(output,"w",compression=ZIP_STORED,allowZip64=False) as z:
            for name in ("index.html","manifest.json","README_KO.txt"):
                info=ZipInfo(name,date_time=(1980,1,1,0,0,0))
                info.compress_type=ZIP_STORED
                info.external_attr=0o100600<<16
                z.writestr(info,members[name])
        return output

    def test_valid_exact_offline_csp_and_delivery_verified(self):
        self.assertTrue(verify_zip(self.archive)["verified"])
        self.assertIn(b"script-src 'sha256-",self.members["index.html"])

    def test_zip_crc_corruption_is_rejected(self):
        output=self.root/"crc-corrupted.zip"
        raw=bytearray(self.archive.read_bytes())
        with ZipFile(self.archive,"r") as archive:
            member=archive.getinfo("index.html")
            self.assertEqual(member.compress_type,ZIP_STORED)
            name_length,extra_length=struct.unpack_from(
                "<HH",raw,member.header_offset+26
            )
        data_offset=member.header_offset+30+name_length+extra_length
        raw[data_offset] ^= 1
        output.write_bytes(raw)
        with self.assertRaisesRegex(ValueError,"ZIP CRC failure"):
            verify_zip(output)

    def test_duplicate_zip_member_name_is_rejected(self):
        output=self.root/"duplicate-member.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore",UserWarning)
            with ZipFile(output,"w",compression=ZIP_STORED,allowZip64=False) as archive:
                for name in ("index.html","manifest.json","README_KO.txt","index.html"):
                    info=ZipInfo(name,date_time=(1980,1,1,0,0,0))
                    info.compress_type=ZIP_STORED
                    info.external_attr=0o100600<<16
                    archive.writestr(info,self.members[name])
        with self.assertRaisesRegex(ValueError,"duplicated or unsafe ZIP members"):
            verify_zip(output)

    def test_tampered_network_policy_with_recomputed_manifest_is_rejected(self):
        html=self.members["index.html"].replace(
            b"connect-src 'none'",b"connect-src https:"
        )
        self.assertNotEqual(html,self.members["index.html"])
        with self.assertRaisesRegex(ValueError,"Offline CSP"):
            verify_zip(self.rebuild_with_html(html))

    def test_relaxed_unsafe_inline_with_recomputed_manifest_is_rejected(self):
        import re
        html=re.sub(rb"script-src 'sha256-[^']+'",
                    b"script-src 'unsafe-inline'",self.members["index.html"],count=1)
        self.assertNotEqual(html,self.members["index.html"])
        with self.assertRaisesRegex(ValueError,"Offline CSP"):
            verify_zip(self.rebuild_with_html(html))

    def test_modified_executable_script_with_manifest_rehash_is_rejected(self):
        html=self.members["index.html"].replace(b"<script>",b"<script>window.UNAPPROVED=1;",1)
        with self.assertRaisesRegex(ValueError,"Offline CSP"):
            verify_zip(self.rebuild_with_html(html))

    def test_removed_policy_with_recomputed_manifest_is_rejected(self):
        import re
        html=re.sub(rb'<meta http-equiv="Content-Security-Policy" content="[^"]+">',
                    b"",self.members["index.html"],count=1)
        with self.assertRaisesRegex(ValueError,"script or CSP structure"):
            verify_zip(self.rebuild_with_html(html))

    def test_duplicate_executable_script_with_recomputed_manifest_is_rejected(self):
        html=self.members["index.html"].replace(b"</body>",b"<script>0</script></body>",1)
        self.assertNotEqual(html,self.members["index.html"])
        with self.assertRaisesRegex(ValueError,"script or CSP structure"):
            verify_zip(self.rebuild_with_html(html))


if __name__=="__main__":
    unittest.main()
