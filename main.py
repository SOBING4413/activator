#!/usr/bin/env python3
"""
Activator Pro - enterprise license readiness and activation assistant.

The application helps administrators audit Windows/Office licensing state and, when
used with an organisation-owned KMS endpoint, apply public Microsoft GVLK keys in a
controlled workflow. It defaults to dry-run mode and never ships with a third-party
KMS host configured.
"""

from __future__ import annotations

import ctypes
import logging
import os
import platform
import queue
import re
import subprocess
import threading
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterable

import tkinter as tk
from tkinter import messagebox, ttk

APP_NAME = "Activator Pro"
APP_VERSION = "3.0"
PRODUCT_KEY_RE = re.compile(r"^[A-Z0-9]{5}(?:-[A-Z0-9]{5}){4}$")
HOST_RE = re.compile(r"^(?=.{1,253}$)(?!-)[A-Za-z0-9.-]+(?<!-)(?::\d{1,5})?$")
LOG_DIR = Path(os.getenv("LOCALAPPDATA", Path.home())) / "ActivatorPro"
LOG_FILE = LOG_DIR / "activator.log"

WINDOWS_KEYS = {
    "Windows 11/10 Pro": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
    "Windows 11/10 Pro N": "MH37W-N47XK-V7XM9-C7227-GCQG9",
    "Windows 11/10 Enterprise": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
    "Windows 11/10 Education": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
    "Windows 10 Home": "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
    "Windows Server 2025 Standard": "TVRH6-WHNXV-R9WG3-9XRFY-MY832",
    "Windows Server 2025 Datacenter": "D764K-2NDRG-47T6Q-P8T8W-YP6DF",
    "Windows Server 2022 Standard": "N2KJX-J94YW-TQVFB-DG9YT-724CC",
    "Windows Server 2022 Datacenter": "6NMRW-2C8FM-D24W7-TQWMY-CWH2D",
    "Windows Server 2019 Standard": "N69G4-B89J2-4G8F4-WWYCC-J464C",
    "Windows Server 2019 Datacenter": "WMDGN-G9PQG-XVVXX-R3X43-63DFG",
}

OFFICE_KEYS = {
    "Office LTSC Professional Plus 2024": "XJ2XN-FW8RK-P4HMP-DKDBV-GCVGB",
    "Office LTSC Standard 2024": "V28N4-JG22K-W66P8-VTMGK-H6HGR",
    "Project Professional 2024": "FQQ23-N4YCY-73HQ3-FM9WC-76HF4",
    "Visio LTSC Professional 2024": "B7TN8-FJ8V3-7QYCP-HQPMV-YY89G",
    "Office LTSC Professional Plus 2021": "FXYTK-NJJ8C-GB6DW-3DYQT-6F7TH",
    "Office LTSC Standard 2021": "KDX7X-BNVR8-TXXGX-4Q7Y8-78VT3",
    "Office Professional Plus 2019": "NMMKJ-6RK4F-KMJVX-8D9MJ-6MWKP",
    "Office Standard 2019": "6NWWJ-YQWMR-QKGCB-6TMB3-9D9HK",
    "Office Professional Plus 2016": "XQNVK-8JYDB-WJ9W3-YJ8YR-WFG99",
    "Office Standard 2016": "JNRGM-WHDWX-FJJG3-K47QV-DRTFM",
}

@dataclass(frozen=True)
class Palette:
    bg: str = "#0f172a"
    surface: str = "#111827"
    surface_2: str = "#1f2937"
    border: str = "#334155"
    text: str = "#e5e7eb"
    muted: str = "#94a3b8"
    accent: str = "#38bdf8"
    success: str = "#22c55e"
    warning: str = "#f59e0b"
    danger: str = "#ef4444"
    input_bg: str = "#020617"

@dataclass(frozen=True)
class CommandResult:
    command: tuple[str, ...]
    output: str
    returncode: int
    skipped: bool = False

class LicenseService:
    """Runs activation commands safely with platform checks, timeouts, and masking."""

    def __init__(self, dry_run: Callable[[], bool], logger: Callable[[str, str], None]):
        self.dry_run = dry_run
        self.logger = logger

    @staticmethod
    def is_windows() -> bool:
        return platform.system().lower() == "windows"

    @staticmethod
    def is_admin() -> bool:
        if not LicenseService.is_windows():
            return False
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False

    def run(self, command: Iterable[str], timeout: int = 45) -> CommandResult:
        args = tuple(command)
        safe = " ".join(self.mask(arg) for arg in args)
        if self.dry_run():
            self.logger(f"Dry-run: {safe}", "info")
            return CommandResult(args, "Dry-run enabled; command was not executed.", 0, True)
        if not self.is_windows():
            return CommandResult(args, "Command skipped: activation commands require Windows.", 1, True)
        if not self.is_admin():
            return CommandResult(args, "Command skipped: run the application as Administrator.", 1, True)
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            completed = subprocess.run(args, capture_output=True, text=True, timeout=timeout, startupinfo=startupinfo, check=False)
            return CommandResult(args, (completed.stdout + completed.stderr).strip(), completed.returncode)
        except subprocess.TimeoutExpired:
            return CommandResult(args, "Command timed out.", 124)
        except OSError as exc:
            return CommandResult(args, f"Unable to start command: {exc}", 1)

    @staticmethod
    def mask(value: str) -> str:
        return PRODUCT_KEY_RE.sub("*****-*****-*****-*****-*****", value)

class ActivatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.palette = Palette()
        self.events: queue.Queue[tuple[str, str]] = queue.Queue()
        self.busy = False
        self._setup_logging()
        self.service = LicenseService(lambda: self.dry_run_var.get(), self.log)
        self._configure_window()
        self._configure_styles()
        self._build_ui()
        self._poll_events()
        self.log(f"{APP_NAME} {APP_VERSION} ready. Dry-run is enabled by default.", "success")

    def _setup_logging(self) -> None:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    def _configure_window(self) -> None:
        self.root.title(f"{APP_NAME} - Enterprise License Assistant")
        self.root.geometry("1120x760")
        self.root.minsize(980, 680)
        self.root.configure(bg=self.palette.bg)

    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.palette.bg)
        style.configure("Card.TFrame", background=self.palette.surface, bordercolor=self.palette.border, relief="solid")
        style.configure("TLabel", background=self.palette.bg, foreground=self.palette.text, font=("Segoe UI", 10))
        style.configure("Muted.TLabel", foreground=self.palette.muted, background=self.palette.bg)
        style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"), foreground=self.palette.text, background=self.palette.bg)
        style.configure("TNotebook", background=self.palette.bg, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.palette.surface, foreground=self.palette.muted, padding=(18, 10), font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.palette.surface_2)], foreground=[("selected", self.palette.text)])
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(14, 9), background=self.palette.accent, foreground="#06202e")
        style.configure("TButton", font=("Segoe UI", 10), padding=(12, 8), background=self.palette.surface_2, foreground=self.palette.text)
        style.configure("TCheckbutton", background=self.palette.bg, foreground=self.palette.text)
        style.configure("Horizontal.TProgressbar", background=self.palette.accent, troughcolor=self.palette.surface_2)

    def _build_ui(self) -> None:
        self.dry_run_var = tk.BooleanVar(value=True)
        self.kms_var = tk.StringVar(value="")
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.IntVar(value=0)

        header = tk.Frame(self.root, bg=self.palette.bg, padx=24, pady=18)
        header.pack(fill=tk.X)
        logo = tk.Canvas(header, width=46, height=46, bg=self.palette.bg, highlightthickness=0)
        logo.create_oval(4, 4, 42, 42, fill=self.palette.surface_2, outline=self.palette.accent, width=2)
        logo.create_text(23, 23, text="AP", fill=self.palette.accent, font=("Segoe UI", 14, "bold"))
        logo.pack(side=tk.LEFT, padx=(0, 14))
        titles = tk.Frame(header, bg=self.palette.bg)
        titles.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(titles, text=APP_NAME, style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(titles, text="Enterprise license readiness, status audit, and controlled KMS activation", style="Muted.TLabel").pack(anchor=tk.W)
        ttk.Checkbutton(header, text="Dry-run mode", variable=self.dry_run_var).pack(side=tk.RIGHT)

        controls = tk.Frame(self.root, bg=self.palette.bg, padx=24)
        controls.pack(fill=tk.X)
        ttk.Label(controls, text="KMS host").pack(side=tk.LEFT)
        self.kms_entry = tk.Entry(controls, textvariable=self.kms_var, bg=self.palette.input_bg, fg=self.palette.text, insertbackground=self.palette.text, relief=tk.FLAT, width=42)
        self.kms_entry.pack(side=tk.LEFT, padx=10, ipady=7)
        ttk.Button(controls, text="Validate environment", style="Accent.TButton", command=self.audit_environment).pack(side=tk.LEFT, padx=6)
        ttk.Button(controls, text="Check Windows status", command=self.check_windows_status).pack(side=tk.LEFT, padx=6)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=24, pady=18)
        self._catalog_tab("Windows", WINDOWS_KEYS, self.activate_windows)
        self._catalog_tab("Office", OFFICE_KEYS, self.activate_office)
        self._build_log_tab()

        footer = tk.Frame(self.root, bg=self.palette.bg, padx=24, pady=10)
        footer.pack(fill=tk.X)
        ttk.Label(footer, textvariable=self.status_var, style="Muted.TLabel").pack(side=tk.LEFT)
        ttk.Progressbar(footer, variable=self.progress_var, maximum=100, length=220).pack(side=tk.RIGHT)

    def _catalog_tab(self, title: str, catalog: dict[str, str], action: Callable[[str, str], None]) -> None:
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=title)
        tk.Label(tab, text=f"{title} product catalog", bg=self.palette.bg, fg=self.palette.text, font=("Segoe UI", 16, "bold")).pack(anchor=tk.W, padx=18, pady=(18, 6))
        search = tk.Entry(tab, bg=self.palette.input_bg, fg=self.palette.text, insertbackground=self.palette.text, relief=tk.FLAT)
        search.pack(fill=tk.X, padx=18, ipady=8)
        columns = ("product", "key")
        tree = ttk.Treeview(tab, columns=columns, show="headings", height=16)
        tree.heading("product", text="Product")
        tree.heading("key", text="GVLK key")
        tree.column("product", width=520)
        tree.column("key", width=260)
        tree.pack(fill=tk.BOTH, expand=True, padx=18, pady=12)
        def refresh(*_):
            term = search.get().lower().strip()
            tree.delete(*tree.get_children())
            for product, key in sorted(catalog.items()):
                if term in product.lower() or term in key.lower():
                    tree.insert("", tk.END, values=(product, key))
        search.bind("<KeyRelease>", refresh)
        refresh()
        ttk.Button(tab, text=f"Activate selected {title}", style="Accent.TButton", command=lambda: self._activate_selected(tree, action)).pack(anchor=tk.E, padx=18, pady=(0, 18))

    def _build_log_tab(self) -> None:
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Audit log")
        self.log_txt = tk.Text(tab, bg=self.palette.input_bg, fg=self.palette.text, insertbackground=self.palette.text, relief=tk.FLAT, wrap=tk.WORD, font=("Cascadia Mono", 10))
        self.log_txt.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)
        self.log_txt.config(state=tk.DISABLED)
        ttk.Button(tab, text="Clear log", command=self.clear_log).pack(anchor=tk.E, padx=18, pady=(0, 18))

    def _activate_selected(self, tree: ttk.Treeview, action: Callable[[str, str], None]) -> None:
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Selection required", "Select a product before continuing.")
            return
        product, key = tree.item(selected[0], "values")
        action(product, key)

    def log(self, message: str, level: str = "info") -> None:
        safe = LicenseService.mask(message)
        logging.log(getattr(logging, level.upper(), logging.INFO), safe)
        self.events.put((safe, level))

    def _poll_events(self) -> None:
        colors = {"info": self.palette.text, "success": self.palette.success, "warning": self.palette.warning, "error": self.palette.danger}
        while not self.events.empty():
            message, level = self.events.get_nowait()
            self.log_txt.config(state=tk.NORMAL)
            tag = level
            self.log_txt.tag_config(tag, foreground=colors.get(level, self.palette.text))
            self.log_txt.insert(tk.END, f"{datetime.now():%H:%M:%S} [{level.upper()}] {message}\n", tag)
            self.log_txt.see(tk.END)
            self.log_txt.config(state=tk.DISABLED)
        self.root.after(100, self._poll_events)

    def clear_log(self) -> None:
        self.log_txt.config(state=tk.NORMAL)
        self.log_txt.delete("1.0", tk.END)
        self.log_txt.config(state=tk.DISABLED)

    def validate_kms(self) -> str | None:
        host = self.kms_var.get().strip()
        if not host or not HOST_RE.match(host):
            messagebox.showerror("Invalid KMS host", "Enter a valid organisation-owned KMS host, for example kms.company.com:1688.")
            return None
        return host

    def set_busy(self, busy: bool, status: str) -> None:
        self.busy = busy
        self.status_var.set(status)
        self.progress_var.set(35 if busy else 0)

    def background(self, status: str, task: Callable[[], None]) -> None:
        if self.busy:
            messagebox.showinfo("Operation in progress", "Please wait for the current operation to finish.")
            return
        self.set_busy(True, status)
        def runner():
            try:
                task()
            except Exception as exc:
                self.log(f"Unexpected error: {exc}", "error")
            finally:
                self.root.after(0, lambda: self.set_busy(False, "Ready"))
        threading.Thread(target=runner, daemon=True).start()

    def audit_environment(self) -> None:
        def task():
            self.log(f"Platform: {platform.platform()}", "info")
            self.log(f"Windows detected: {self.service.is_windows()}", "info")
            self.log(f"Administrator privileges: {self.service.is_admin()}", "info")
            self.find_office_paths()
            self.log(f"Persistent log: {LOG_FILE}", "info")
        self.background("Auditing environment", task)

    def check_windows_status(self) -> None:
        self.background("Checking Windows status", lambda: self.log(self.service.run(("cscript", "//nologo", "slmgr.vbs", "/xpr")).output, "info"))

    def activate_windows(self, product: str, key: str) -> None:
        host = self.validate_kms()
        if not host:
            return
        def task():
            self.log(f"Preparing Windows activation for {product}.", "info")
            for command in (("cscript", "//nologo", "slmgr.vbs", "/ipk", key), ("cscript", "//nologo", "slmgr.vbs", "/skms", host), ("cscript", "//nologo", "slmgr.vbs", "/ato"), ("cscript", "//nologo", "slmgr.vbs", "/xpr")):
                result = self.service.run(command)
                self.log(result.output or f"Return code: {result.returncode}", "success" if result.returncode == 0 else "warning")
        self.background("Activating Windows", task)

    def activate_office(self, product: str, key: str) -> None:
        host = self.validate_kms()
        if not host:
            return
        def task():
            paths = self.find_office_paths()
            if not paths:
                self.log("No Office ospp.vbs installation was found in standard locations.", "warning")
                return
            ospp = str(paths[0] / "ospp.vbs")
            self.log(f"Preparing Office activation for {product} using {paths[0]}.", "info")
            for command in (("cscript", "//nologo", ospp, f"/inpkey:{key}"), ("cscript", "//nologo", ospp, f"/sethst:{host}"), ("cscript", "//nologo", ospp, "/act"), ("cscript", "//nologo", ospp, "/dstatus")):
                result = self.service.run(command)
                self.log(result.output or f"Return code: {result.returncode}", "success" if result.returncode == 0 else "warning")
        self.background("Activating Office", task)

    def find_office_paths(self) -> list[Path]:
        roots = [os.getenv("ProgramFiles", ""), os.getenv("ProgramFiles(x86)", "")]
        versions = ("Office16", "Office15", "Office14")
        found: list[Path] = []
        for root in filter(None, roots):
            for version in versions:
                path = Path(root) / "Microsoft Office" / version
                if (path / "ospp.vbs").exists():
                    found.append(path)
                    self.log(f"Office detected: {path}", "success")
        if not found:
            self.log("Office not detected in standard installation paths.", "warning")
        return found

def main() -> None:
    root = tk.Tk()
    ActivatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
