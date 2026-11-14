"""Hosted Windows-only acceptance of an unsigned PyInstaller onedir preview.

Generates synthetic files in TemporaryDirectory and never uploads source data.
Passing here does not establish Windows 10/11 customer, signature or sale approval.
"""
from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
import platform
import subprocess
import tempfile
import time
from pathlib import Path

STATUS = "UNSIGNED_PRIVATE_PREVIEW_ONLY_RELEASE_HOLD"
def _run(executable, args, *, expected=0, env=None):
    process = subprocess.run([str(executable), *map(str, args)], text=True,
                             encoding="utf-8", errors="replace",
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=100, check=False, env=env)
    if process.returncode != expected:
        # Only synthetic smoke commands are used by this hosted test. Report
        # bounded, allow-listed status fields rather than raw stdout/stderr,
        # which could expose source records or machine/user paths.
        try:
            diagnostic = json.loads(process.stdout.strip())
            status = diagnostic.get("status") if isinstance(diagnostic,dict) else None
            browsers = diagnostic.get("browser_results") if isinstance(diagnostic,dict) else None
            if status not in ("PARTIAL_HOLD","HOLD","PASS_SYNTHETIC_ONLY"):
                status = "OTHER_OR_MISSING"
            if not isinstance(browsers,dict):
                browsers = {}
            allow = {"HOLD_EXECUTION_FAILED","HOLD_NONZERO_EXIT",
                     "HOLD_BROWSER_NOT_INSTALLED","HOLD_BROWSER_RENDER_NOT_CONFIRMED",
                     "HOLD_BROWSER_CONTENT_NOT_VISIBLE","PASS_SYNTHETIC_LOCAL_FILE"}
            browsers = {key:val if val in allow else "UNKNOWN"
                        for key,val in browsers.items() if key in ("chrome","edge")}
        except (ValueError,TypeError):
            status,browsers = "INVALID_JSON",{}
        raise AssertionError(
            f"Native command exit {process.returncode}, expected {expected}; "
            f"action={args[0]}; status={status}; synthetic_browser_results={browsers}"
        )
    try:
        result = json.loads(process.stdout.strip())
    except json.JSONDecodeError as exc:
        raise AssertionError("Native command did not provide valid redacted JSON") from exc
    if "LOCAL-SYNTHETIC-ITEM" in process.stdout:
        raise AssertionError("Synthetic private cell echoed to stdout")
    return result

def _desktop_window(executable):
    """Find an actual Tk top-level window associated with *this* native process."""
    if os.name != "nt":
        raise RuntimeError("Native desktop test requires Windows")
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows.argtypes = [callback_type, wintypes.LPARAM]
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
    user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    process = subprocess.Popen([str(executable), "desktop"], stdin=subprocess.DEVNULL,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline = time.monotonic() + 18
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise AssertionError("Native desktop exited before displaying a window")
            windows = []
            @callback_type
            def inspect(hwnd, unused):
                pid = wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                if pid.value == process.pid:
                    length = user32.GetWindowTextLengthW(hwnd)
                    buf = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buf, len(buf))
                    if "DATA2WEB Studio" in buf.value:
                        windows.append(hwnd)
                return True
            user32.EnumWindows(inspect, 0)
            if windows:
                user32.PostMessageW(windows[0], 0x0010, 0, 0)
                process.wait(timeout=8)
                if process.returncode != 0:
                    raise AssertionError("Native desktop did not close cleanly")
                return True
            time.sleep(0.3)
        raise AssertionError("Native Tk desktop window not visible within guard")
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)

def acceptance(executable, manifest_path):
    exe = Path(executable).resolve(strict=True)
    if os.name != "nt" or exe.suffix.lower() != ".exe":
        raise ValueError("Windows EXE required")
    if exe.parent.name != "DATA2WEB-LOCAL":
        raise ValueError("Unexpected private onedir preview layout")
    if manifest_path.exists():
        raise FileExistsError("Preview manifest must be create-only")
    with tempfile.TemporaryDirectory(prefix="data2web-native-preview-") as scratch:
        root = Path(scratch)
        # This PATH deliberately contains no Python executable: native CLI must
        # execute with the embedded interpreter, not installed Python on runner.
        env = os.environ.copy()
        win = env.get("SystemRoot", "C:\\Windows")
        env["PATH"] = win + "\\System32;" + win
        env.pop("PYTHONHOME", None)
        env.pop("PYTHONPATH", None)
        self_result = _run(exe, ["self-check", "--browsers"], env=env)
        if self_result["status"] != "PASS_SYNTHETIC_ONLY" or (
            self_result["browser_results"] != {
                "chrome":"PASS_SYNTHETIC_LOCAL_FILE",
                "edge":"PASS_SYNTHETIC_LOCAL_FILE",
            }):
            raise AssertionError("Native file browser self-check failed")
        source = root / "synthetic.csv"
        source.write_text("id,title,category,amount\n"
                          "A1,LOCAL-SYNTHETIC-ITEM,A,12\n", encoding="utf-8")
        original = source.read_bytes()
        digest = hashlib.sha256(original).hexdigest()
        dest = root / "private-delivery"
        _run(exe, ["deliver", source, dest, "--source-sha256", digest,
                   "--id", "id", "--title", "title", "--category", "category",
                   "--confirm", "APPROVE", "--ack-plaintext",
                   "--privacy-classification", "NO_PERSONAL_DATA_REVIEWED"], env=env)
        if source.read_bytes() != original:
            raise AssertionError("Owner source was modified")
        receipt = _run(exe, ["verify-customer", dest], env=env)
        if receipt.get("verified") is not True or receipt.get("sale_approved") is not False:
            raise AssertionError("Native delivery integrity or release gate failure")
        _run(exe, ["deliver", source, dest, "--source-sha256", digest,
                   "--id", "id", "--title", "title", "--category", "category",
                   "--confirm", "APPROVE", "--ack-plaintext",
                   "--privacy-classification", "NO_PERSONAL_DATA_REVIEWED"],
             expected=2, env=env)
        if source.read_bytes() != original:
            raise AssertionError("Existing customer input was modified")
        with (dest / "receipt.json").open("ab") as stream:
            stream.write(b"mutated")
        hold = _run(exe, ["verify-customer", dest], expected=2, env=env)
        if hold.get("status") != "HOLD":
            raise AssertionError("Mutated customer receipt was accepted")
        desktop_ok = _desktop_window(exe)
    # Hash the private generated folder without embedding synthetic user records.
    files = {}
    for member in sorted(exe.parent.rglob("*")):
        if not member.is_file():
            continue
        key = member.relative_to(exe.parent).as_posix()
        files[key] = {"sha256":hashlib.sha256(member.read_bytes()).hexdigest(),
                      "bytes":member.stat().st_size}
    report = {
        "contract":"DATA2WEB_NATIVE_WINDOWS_PREVIEW_V1",
        "status":STATUS,
        "source_sha":os.environ.get("GITHUB_SHA", "NOT_SET"),
        "build_platform":platform.system(),
        "exe_sha256":files[exe.name]["sha256"],
        "files":files,
        "offline_native_command":True,
        "synthetic_delivery_verified":True,
        "tamper_rejected":True,
        "existing_output_preserved":True,
        "native_tk_window_seen":desktop_ok,
        "customer_source_included":False,
        "customer_pc_windows_10_or_11_verified":False,
        "signed_executable":False,
        "commercial_rights_verified":False,
        "sale_approved":False,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=True, sort_keys=True, indent=2)
        stream.write("\n")
    return {"status":"PASS_SYNTHETIC_HOSTED_ONLY", "preview_sha256":report["exe_sha256"],
            "file_count":len(files), "native_tk_window_seen":desktop_ok,
            "customer_pc_verified":False,"sale_approved":False}

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--exe",type=Path,required=True)
    parser.add_argument("--manifest",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(acceptance(args.exe,args.manifest),ensure_ascii=True,sort_keys=True))
