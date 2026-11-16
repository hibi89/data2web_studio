"""Windows hosted GUI render smoke (real Tk widgets, no customer file or network).

Performs a single synthetic control creation/render check in a short-lived UI,
automatically closes it; not equivalent to physical Windows10/11 user sign-off.
"""
from __future__ import annotations

import os
import tkinter as tk
from unittest.mock import patch
from data2web_desktop import desktop_main

def main():
    real_tk=tk.Tk
    evidence={"rendered":False}
    def create_root(*args,**kwargs):
        root=real_tk(*args,**kwargs)
        def verify():
            controls=[]
            def visit(widget):
                for x in widget.winfo_children():
                    controls.append(x)
                    visit(x)
            visit(root)
            text=root.title()
            evidence["rendered"]=(
                "DATA2WEB Studio" in text and
                sum(isinstance(c,tk.Widget) for c in controls)>=20 and
                root.winfo_width()>=700 and root.winfo_height()>=500
            )
            evidence["widget_count"]=len(controls)
            root.destroy()
        root.after(900,verify)
        # A watchdog prevents an unattended CI desktop from staying open.
        root.after(5000,lambda:root.destroy() if root.winfo_exists() else None)
        return root
    with patch.object(tk,"Tk",new=create_root):
        desktop_main()
    assert evidence["rendered"],"Tk window or review form failed to render on hosted Windows"
    print("HOSTED_WINDOWS_TK_RENDER_PASS widgets="+str(evidence["widget_count"])+
          " (hosted GUI smoke only, not customer Windows10/11 acceptance)")

if __name__=="__main__":
    main()
