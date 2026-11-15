# R32 offline Windows preview verification guide — 2026-11-15

## Scope

This guide covers the unsigned, folder-based Python launcher preview produced by `package_windows_bundle.py`. It is an engineering preview only: **no installer, no signed executable, no commercial distribution permission, and no release approval**. It does not change the official score or release hold.

The package uses Python 3.11+ already installed by the examiner. Tcl/Tk is required only for the desktop GUI. It does not install Python, download dependencies, create services, write registry entries, or configure startup. No customer files belong in the bundle or hosted CI artifacts.

## Build on an authorized Windows 10 or Windows 11 test machine

Use a clean checkout of the exact source commit under test and a new empty destination directory. Keep each OS run separate.

```powershell
py -3.11 --version
py -3.11 -m unittest test_windows_bundle -v
$target = Join-Path ([System.IO.Path]::GetTempPath()) ("data2web-bundle-" + [guid]::NewGuid().ToString("N"))
py -3.11 package_windows_bundle.py create $target
py -3.11 package_windows_bundle.py verify $target
Get-FileHash (Join-Path $target "BUNDLE_MANIFEST.json") -Algorithm SHA256
Get-FileHash (Join-Path $target "DATA2WEB.pyz") -Algorithm SHA256
```

The destination must not exist. The creator is create-only; if it reports an existing target or fails partway, preserve that directory for inspection and do not overwrite or automatically remove it. Record the tested 40-character source commit, Windows version, Python patch version, test result, and manifest/runtime SHA-256 values in the authorized private test record. Do not record a person's identity, account, device serial, username, local path, source data, or screenshots in a public report.

The two `Get-FileHash` commands are local integrity values. The manifest hashes the bundle's other fixed members; it does not authenticate its own origin. Compare the manifest SHA with a separately authenticated value only if an owner has approved an authorized channel for that purpose. SHA-256 alone is not a signature or proof of legal rights.

## Runtime and verification

From a newly created copy:

1. Run `RUN_SELFCHECK.cmd`. It exercises the synthetic local preview and checks installed Chrome/Edge when available. A missing browser is a HOLD for that browser; hosted CI does not replace a real-device run.
2. Run `RUN_DESKTOP.cmd` with only the synthetic fixture unless separate per-order rights, consent, and plaintext notice have been verified. Confirm the user sees a local file chooser and that output is create-only.
3. Run `VERIFY_CUSTOMER.cmd "<authorized local delivery folder>"` only against a separately authorized local delivery. This checks a customer delivery folder; it is not the portable-bundle verifier.
4. To check the portable bundle manifest from an available clean source checkout, use `py -3.11 package_windows_bundle.py verify <bundle-directory>`. This checks exact member names and member hashes against the manifest. It does not establish that the manifest or source was published by a particular person.

Do not bypass a Windows security warning to claim acceptance. Record a blocked launch as `NOT_RUN` or `HOLD`, together with the non-identifying test step only.

## Reproducibility and install/uninstall boundary

Build twice from the same exact source SHA into two different new directories on the same OS and Python patch version. Compare every member's bytes (including `BUNDLE_MANIFEST.json`); the focused test `test_identical_bundle_bytes_in_independent_folders` already checks deterministic output in separate temporary folders. If the bytes differ, stop and investigate before calling the build reproducible. Cross-OS or cross-Python-patch byte identity is not inferred from that test.

There is no app installer or uninstaller in this preview. The examiner installs no application-level files; the bundle runs from its folder. To end a test, close DATA2WEB processes and preserve the original bundle, source, generated output, and evidence until the examiner has reconciled them. Any later manual cleanup is an owner/operator action and must target only the exact newly created test bundle after review. The application never deletes customer source or existing output.

## Acceptance boundary

A hosted Windows runner is an implementation smoke test. It does not establish Windows 10 or Windows 11 customer compatibility, installed Chrome/Edge behavior on the buyer's device, code-signing rights, redistribution rights, or sale approval. Those remain `EXTERNAL_PENDING` or `OWNER_PENDING` until independently evidenced. Current product packaging remains unsigned and `RELEASE HOLD / SALE NO-GO`.
