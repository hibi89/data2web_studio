"""Reject rehashed offline HTML mutations and keep saved DOM compatible.

All sources synthetic. This tests the shipping verifier's reviewed static
surface, NOT publisher/source authenticity or an external human security audit.
"""
from __future__ import annotations
import base64
import hashlib
import re
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

    def test_browser_saved_dynamic_dom_remains_verifiable(self):
        # Browser "Save page" serializes the rendered table, chart and controls.
        html=self.members["index.html"].replace(
            b'<tbody id="body"></tbody>',
            b'<tbody id="body"><tr tabindex="0" aria-label="Synthetic">'
            b'<td>synthetic</td><td>&lt;/script&gt;</td></tr></tbody>',1)
        chart=(b'<div class="chart-row"><span class="chart-key">A</span>'
               b'<div class="bar-track"><div class="bar-fill" '
               b'style="width: 25%;"></div></div>'
               b'<span class="chart-value">1</span></div>')
        html,n=re.subn(rb'(<div id="chart-bars"[^>]*>)',
                       lambda match:match.group(1)+chart,html,count=1)
        self.assertEqual(n,1)
        html=html.replace(
            b'</select>',
            b'<option data-all="true" value="" selected="">All</option></select>',1)
        html=html.replace(
            b'<button id="prev" type="button">',
            b'<button id="prev" type="button" disabled="">',1)
        html=html.replace(b'class="warning" hidden>',
                          b'class="warning" hidden="">',1)
        html=html.replace(
            "인쇄는 현재 화면의 최대 50행만 포함합니다. 전체 자료는 오프라인 HTML에서 확인하세요.".encode(),
            "인쇄 범위: 1건 중 화면 1/1 페이지의 최대 50행. 전체 데이터는 오프라인 HTML을 이용하세요.".encode(),
            1)
        self.assertTrue(verify_zip(self.rebuild_with_html(html))["verified"])

    def test_rehashed_navigation_and_layout_mutations_are_rejected(self):
        html=self.members["index.html"]
        mutations=[]
        mutations.append(html.replace(
            b"</head>",
            b'<meta http-equiv="refresh" content="0;url=https://invalid.example/">'
            b"</head>",1))
        csp=re.search(rb'<meta http-equiv="Content-Security-Policy" content="[^"]+">',
                      html)
        self.assertIsNotNone(csp)
        moved=html.replace(csp.group(0),b"",1)
        mutations.append(moved.replace(b"<body>",b"<body>"+csp.group(0),1))
        script=re.search(rb"<script>.*?</script>",html,flags=re.DOTALL)
        self.assertIsNotNone(script)
        moved=html.replace(script.group(0),b"",1)
        mutations.append(moved.replace(b"<main>",script.group(0)+b"<main>",1))
        for index,changed in enumerate(mutations):
            with self.subTest(mutation_index=index):
                with self.assertRaises(ValueError):
                    verify_zip(self.rebuild_with_html(changed))

    def test_rehashed_script_with_matching_csp_is_rejected(self):
        html=self.members["index.html"].replace(
            b"<script>",b"<script>window.unapproved_test=true;",1)
        script=re.search(rb"<script>(.*?)</script>",html,flags=re.DOTALL)
        self.assertIsNotNone(script)
        digest=base64.b64encode(hashlib.sha256(script.group(1)).digest())
        html,n=re.subn(rb"script-src 'sha256-[^']+'",
                       b"script-src 'sha256-"+digest+b"'",html,count=1)
        self.assertEqual(n,1)
        with self.assertRaises(ValueError):
            verify_zip(self.rebuild_with_html(html))

    def test_rehashed_style_change_is_rejected(self):
        html=self.members["index.html"].replace(
            b"<style>",b"<style>body{background:url(https://invalid.example/)}",1)
        with self.assertRaises(ValueError):
            verify_zip(self.rebuild_with_html(html))

    def test_shadowed_dataset_identity_is_rejected(self):
        html=self.members["index.html"].replace(
            b"</main>",
            b'<div id="dataset">{"contract":"DATA2WEB_HTML_V1","rows":[]}</div>'
            b"</main>",1)
        with self.assertRaises(ValueError):
            verify_zip(self.rebuild_with_html(html))

    def test_changed_import_warning_or_ack_semantics_is_rejected(self):
        warning=(
            "현재 데이터는 브라우저에서 교체한 로컬 CSV입니다. "
            "원본 SHA·이전 납품 ZIP 무결성 증거가 새 데이터에 적용되지 않습니다. "
            "배포 전 판매자 재검증이 필요합니다."
        ).encode()
        changed_warning=self.members["index.html"].replace(
            warning,"데이터는 이미 판매자가 검증했습니다.".encode(),1)
        self.assertNotEqual(changed_warning,self.members["index.html"])
        with self.assertRaises(ValueError):
            verify_zip(self.rebuild_with_html(changed_warning))
        changed_ack=self.members["index.html"].replace(
            b'id="ack" type="checkbox"',b'id="ack" type="text"',1)
        self.assertNotEqual(changed_ack,self.members["index.html"])
        with self.assertRaises(ValueError):
            verify_zip(self.rebuild_with_html(changed_ack))

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
        with self.assertRaisesRegex(ValueError,"Unexpected, duplicated, or unsafe ZIP members"):
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
