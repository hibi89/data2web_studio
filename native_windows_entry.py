"""Native Windows test-only entrypoint for the existing offline studio CLI/GUI.

No customer content, new network endpoints or commercial permissions are added.
The executable must stay RELEASE HOLD until owner/customer/legal acceptance.
"""
from studio import main

if __name__ == "__main__":
    raise SystemExit(main())
