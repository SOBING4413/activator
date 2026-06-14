#!/usr/bin/env python3
"""
Activator Pro - Windows & Office Activation Tool
Created by: ALIF HAKIM
KMS Server: kms8.msguides.com
Version: 2.0
"""

import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

# ==================== WINDOWS GVLK KEYS ====================
WINDOWS_KEYS = {
    "Windows 11/10 Pro": "W269N-WFGWX-YVC9B-4J6C9-T83GX",
    "Windows 11/10 Pro N": "MH37W-N47XK-V7XM9-C7227-GCQG9",
    "Windows 11/10 Pro Workstation": "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J",
    "Windows 11/10 Pro Workstation N": "9FNHH-K3HBT-3W4TD-6383H-6XYWF",
    "Windows 11/10 Pro Education": "6J4XB-F8PXD-7PXPP-8F6RP-46F2T",
    "Windows 11/10 Pro Education N": "YVWGF-BXNMC-HTQYQ-CPQ99-66QFC",
    "Windows 11/10 Enterprise": "NPPR9-FWDCX-D2C8J-H872K-2YT43",
    "Windows 11/10 Enterprise N": "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4",
    "Windows 11/10 Enterprise G": "YYVX9-NTFWV-6MDM3-9PT4T-4M68B",
    "Windows 11/10 Enterprise G N": "44RPN-FTY23-9VTTB-MP9BX-T84FV",
    "Windows 11/10 Education": "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
    "Windows 11/10 Education N": "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ",
    "Windows 11/10 Enterprise LTSC 2021/2019": "M7XTQ-FN8P6-TTKYV-9D4CC-J462D",
    "Windows 11/10 Enterprise N LTSC 2021/2019": "92NFX-8DJQP-P6BBQ-THF9C-7CG2H",
    "Windows 10 Home": "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
    "Windows 10 Home N": "3KHY7-WNT83-DGQKR-F7HPR-844BM",
    "Windows 10 Home Single Language": "7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH",
    "Windows 10 Home Country Specific": "PVMJN-6DFY6-9CCP6-7BKTT-D3WVR",
    "Windows 10 Enterprise LTSB 2016": "DCPHK-NFMTC-H88MJ-PFHPY-QJ4BJ",
    "Windows 10 Enterprise N LTSB 2016": "QFFDN-GRT3P-VKWWX-X7T3R-8B639",
    "Windows 10 Enterprise 2015 LTSB": "WNMTR-4C88C-JK8YV-HQ7T2-76DF9",
    "Windows 10 Enterprise 2015 LTSB N": "2F77B-TNFGY-69QQF-B8YKP-D69TJ",
    "Windows 8.1 Pro": "GCRJD-8NW9H-F2CDX-CCM8D-9D6T9",
    "Windows 8.1 Pro N": "HMCNV-VVBFX-7HMBH-CTY9B-B4FXY",
    "Windows 8.1 Enterprise": "MHF9N-XY6XB-WVXMC-BTDCT-MKKG7",
    "Windows 8.1 Enterprise N": "TT4HM-HN7YT-62K67-RGRQJ-JFFXW",
    "Windows 8 Pro": "NG4HW-VH26C-733KW-K6F98-J8CK4",
    "Windows 8 Enterprise": "32JNW-9KQ84-P47T8-D8GGY-CWCK7",
    "Windows 7 Professional": "FJ82H-XT6CR-J8D7P-XQJJ2-GPDD4",
    "Windows 7 Professional N": "MRPKT-YTG23-K7D7T-X2JMM-QY7MG",
    "Windows 7 Professional E": "W82YF-2Q76Y-63HXB-FGJG9-GF7QX",
    "Windows 7 Enterprise": "33PXH-7Y6KF-2VJC9-XBBR8-HVTHH",
    "Windows 7 Enterprise N": "YDRBP-3D83W-TY26F-D46B2-XCKRJ",
    "Windows 7 Enterprise E": "C29WB-22CC8-VJ326-GHFJW-H9DH4",
    "Windows Server 2025 Standard": "TVRH6-WHNXV-R9WG3-9XRFY-MY832",
    "Windows Server 2025 Datacenter": "D764K-2NDRG-47T6Q-P8T8W-YP6DF",
    "Windows Server 2022 Standard": "N2KJX-J94YW-TQVFB-DG9YT-724CC",
    "Windows Server 2022 Datacenter": "6NMRW-2C8FM-D24W7-TQWMY-CWH2D",
    "Windows Server 2019 Standard": "N69G4-B89J2-4G8F4-WWYCC-J464C",
    "Windows Server 2019 Datacenter": "WMDGN-G9PQG-XVVXX-R3X43-63DFG",
    "Windows Server 2016 Standard": "WC2BQ-8NRM3-FDDYY-2BFGV-KHKQY",
    "Windows Server 2016 Datacenter": "CB7KF-BWN84-R7R2Y-793K2-8XDDG",
    "Windows Server 2012 R2 Standard": "D2N9P-3P6X9-2R39C-7RTCD-MDVKX",
    "Windows Server 2012 R2 Datacenter": "W3GGN-FT8W3-Y4M27-J84CP-Q3VJ9",
    "Windows Server 2012 Standard": "XC9B7-NBPP2-83J2H-RHMBY-92BT4",
    "Windows Server 2012 Datacenter": "48HP8-DN98B-MYWDG-P2PYC-DY2YJ",
    "Windows Server 2008 R2 Standard": "YC6KT-GKW9T-YTKYR-T4X34-R7VHC",
    "Windows Server 2008 R2 Enterprise": "489J6-VHDMP-X63PK-3K798-CPX3Y",
    "Windows Server 2008 R2 Datacenter": "74YFP-3QFB3-KQT8W-PMXWJ-7M648",
}

# ==================== OFFICE GVLK KEYS ====================
OFFICE_KEYS = {
    "Office LTSC Professional Plus 2024": "XJ2XN-FW8RK-P4HMP-DKDBV-GCVGB",
    "Office LTSC Standard 2024": "V28N4-JG22K-W66P8-VTMGK-H6HGR",
    "Project Professional 2024": "FQQ23-N4YCY-73HQ3-FM9WC-76HF4",
    "Project Standard 2024": "PD3TT-NTHQQ-VC7CY-MFXK3-G87F8",
    "Visio LTSC Professional 2024": "B7TN8-FJ8V3-7QYCP-HQPMV-YY89G",
    "Visio LTSC Standard 2024": "JMMVY-XFNQC-KK4HK-9H7R3-WQQTV",
    "Access LTSC 2024": "82FTR-NCHR7-W3944-MGRHM-JMCWD",
    "Excel LTSC 2024": "F4DYN-89BP2-WQTWJ-GR8YC-CKGJG",
    "Outlook LTSC 2024": "D2F8D-N3Q3B-J28PV-X27HD-RJWB9",
    "PowerPoint LTSC 2024": "CW94N-K6GJH-9CTXY-MG2VC-FYCWP",
    "Word LTSC 2024": "MQ84N-7VYDM-FXV7C-6K7CC-VFW9J",
    "Office LTSC Professional Plus 2021": "FXYTK-NJJ8C-GB6DW-3DYQT-6F7TH",
    "Office LTSC Standard 2021": "KDX7X-BNVR8-TXXGX-4Q7Y8-78VT3",
    "Project Professional 2021": "FTNWT-C6WBT-8HMGF-K9PRX-QV9H8",
    "Project Standard 2021": "J2JDC-NJCYY-9RGQ4-YXWMH-T3D4T",
    "Visio LTSC Professional 2021": "KNH8D-FGHT4-T8RK3-CTDYJ-K2HT4",
    "Visio LTSC Standard 2021": "MJVNY-BYWPY-CWV6J-2RKRT-4M8QG",
    "Access LTSC 2021": "WM8YG-YNGDD-4JHDC-PG3F4-FC4T4",
    "Excel LTSC 2021": "NWG3X-87C9K-TC7YY-BC2G7-G6RVC",
    "Outlook LTSC 2021": "C9FM6-3N72F-HFJXB-TM3V9-T86R9",
    "PowerPoint LTSC 2021": "TY7XF-NFRBR-KJ44C-G83KF-GX27K",
    "Publisher LTSC 2021": "2MW9D-N4BXM-9VBPG-Q7W6M-KFBGQ",
    "Word LTSC 2021": "TN8H9-M34D3-Y64V9-TR72V-X79KV",
    "Office Professional Plus 2019": "NMMKJ-6RK4F-KMJVX-8D9MJ-6MWKP",
    "Office Standard 2019": "6NWWJ-YQWMR-QKGCB-6TMB3-9D9HK",
    "Project Professional 2019": "B4NPR-3FKK7-T2MBV-FRQ4W-PKD2B",
    "Project Standard 2019": "C4F7P-NCP8C-6CQPT-MQHV9-JXD2M",
    "Visio Professional 2019": "9BGNQ-K37YR-RQHF2-38RQ3-7VCBB",
    "Visio Standard 2019": "7TQNQ-K3YQQ-3PFH7-CCPPM-X4VQ2",
    "Access 2019": "9N9PT-27V4Y-VJ2PD-YXFMF-YTFQT",
    "Excel 2019": "TMJWT-YYNMB-3BKTF-644FC-RVXBD",
    "Outlook 2019": "7HD7K-N4PVK-BHBCQ-YWQRW-XW4VK",
    "PowerPoint 2019": "RRNCX-C64HY-W2MM7-MCH9G-TJHMQ",
    "Publisher 2019": "G2KWX-3NW6P-PY93R-JXK2T-C9Y9V",
    "Word 2019": "PBX3G-NWMT6-Q7XBW-PYJGG-WXD33",
    "Office Professional Plus 2016": "XQNVK-8JYDB-WJ9W3-YJ8YR-WFG99",
    "Office Standard 2016": "JNRGM-WHDWX-FJJG3-K47QV-DRTFM",
    "Project Professional 2016": "YG9NW-3K39V-2T3HJ-93F3Q-G83KT",
    "Project Standard 2016": "GNFHQ-F6YQM-KQDGJ-327XX-KQBVC",
    "Visio Professional 2016": "PD3PC-RHNGV-FXJ29-8JK7D-RJRJK",
    "Visio Standard 2016": "7WHWN-4T7MP-G96JF-G33KR-W8GF4",
    "Access 2016": "GNH9Y-D2J4T-FJHGG-QRVH7-QPFDW",
    "Excel 2016": "9C2PK-NWTVB-JMPW8-BFT28-7FTBF",
    "Outlook 2016": "R69KK-NTPKF-7M3Q4-QYBHW-6MT9B",
    "PowerPoint 2016": "J7MQP-HNJ4Y-WJ7YM-PFYGF-BY6C6",
    "Publisher 2016": "F47MM-N3XJP-TQXJ9-BP99D-8K837",
    "Word 2016": "WXY84-JN2Q9-RBCCQ-3Q3J3-3PFJ6",
}

KMS_SERVER = "kms8.msguides.com"


class ActivatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Activator Pro - Windows & Office Activator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)

        self.bg_color = "#1a1a2e"
        self.fg_color = "#e0e0e0"
        self.accent_color = "#0f3460"
        self.button_color = "#16213e"
        self.success_color = "#4ecca3"
        self.warn_color = "#e84545"

        self.root.configure(bg=self.bg_color)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.button_color, foreground=self.fg_color,
                        padding=[15, 5], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.accent_color)])
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 10))
        style.configure("TButton", background=self.button_color, foreground=self.fg_color,
                        font=("Segoe UI", 10, "bold"), borderwidth=0, padding=8)
        style.map("TButton", background=[("active", self.accent_color)])

        self.build_ui()
        self.log("Activator Pro v2.0 - Created by ALIF HAKIM", "info")

    def build_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color, pady=15)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="ACTIVATOR PRO", font=("Segoe UI", 22, "bold"),
                 fg="#4ecca3", bg=self.bg_color).pack()
        tk.Label(header_frame, text="Windows & Office Activation Tool | KMS: kms8.msguides.com",
                 font=("Segoe UI", 10), fg=self.fg_color, bg=self.bg_color).pack()

        # Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tab Windows
        self.win_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.win_tab, text="Windows Activation")
        self.build_windows_tab()

        # Tab Office
        self.off_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.off_tab, text="Office Activation")
        self.build_office_tab()

        # Tab Auto
        self.auto_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.auto_tab, text="Auto Activate")
        self.build_auto_tab()

        # Tab Log
        self.log_tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_tab_frame, text="Log")
        self.build_log_tab()

        # Footer
        footer_frame = tk.Frame(self.root, bg=self.bg_color, pady=8)
        footer_frame.pack(fill=tk.X)
        tk.Label(footer_frame, text="Created by ALIF HAKIM  |  Activator Pro v2.0",
                 font=("Segoe UI", 9), fg=self.fg_color, bg=self.bg_color).pack()
        tk.Label(footer_frame, text="Run as Administrator for best results",
                 font=("Segoe UI", 9), fg=self.warn_color, bg=self.bg_color).pack()

    # ========== WINDOWS TAB ==========
    def build_windows_tab(self):
        frame = ttk.Frame(self.win_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Search
        sf = tk.Frame(frame, bg=self.bg_color)
        sf.pack(fill=tk.X, pady=(0, 10))
        tk.Label(sf, text="Search:", font=("Segoe UI", 10),
                fg=self.fg_color, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        self.win_search = tk.Entry(sf, font=("Segoe UI", 10), bg="#2a2a4e", fg=self.fg_color,
                                   insertbackground=self.fg_color, relief=tk.FLAT, bd=5)
        self.win_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.win_search.bind("<KeyRelease>", lambda e: self.filter_win_list())

        # List
        lf = tk.Frame(frame, bg=self.bg_color)
        lf.pack(fill=tk.BOTH, expand=True)
        scroll = tk.Scrollbar(lf, orient=tk.VERTICAL)
        self.win_list = tk.Listbox(lf, yscrollcommand=scroll.set, font=("Consolas", 9),
                                   bg="#0d0d1a", fg=self.fg_color, selectbackground=self.accent_color,
                                   borderwidth=0, highlightthickness=0)
        scroll.config(command=self.win_list.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.win_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.win_items = sorted(WINDOWS_KEYS.keys())
        for item in self.win_items:
            self.win_list.insert(tk.END, f"{item:55s} | {WINDOWS_KEYS[item]}")

        # Buttons
        bf = tk.Frame(frame, bg=self.bg_color)
        bf.pack(fill=tk.X, pady=10)
        tk.Button(bf, text="ACTIVATE SELECTED", font=("Segoe UI", 11, "bold"),
                  bg="#4ecca3", fg="#1a1a2e", padx=20, pady=8, bd=0, cursor="hand2",
                  command=self.activate_windows).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="CHECK STATUS", font=("Segoe UI", 10),
                  bg=self.button_color, fg=self.fg_color, padx=15, pady=8, bd=0, cursor="hand2",
                  command=self.check_windows_status).pack(side=tk.LEFT, padx=5)

    def filter_win_list(self):
        s = self.win_search.get().lower()
        self.win_list.delete(0, tk.END)
        for item in self.win_items:
            if s in item.lower() or s in WINDOWS_KEYS[item].lower():
                self.win_list.insert(tk.END, f"{item:55s} | {WINDOWS_KEYS[item]}")

    # ========== OFFICE TAB ==========
    def build_office_tab(self):
        frame = ttk.Frame(self.off_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        sf = tk.Frame(frame, bg=self.bg_color)
        sf.pack(fill=tk.X, pady=(0, 10))
        tk.Label(sf, text="Search:", font=("Segoe UI", 10),
                fg=self.fg_color, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        self.off_search = tk.Entry(sf, font=("Segoe UI", 10), bg="#2a2a4e", fg=self.fg_color,
                                   insertbackground=self.fg_color, relief=tk.FLAT, bd=5)
        self.off_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.off_search.bind("<KeyRelease>", lambda e: self.filter_off_list())

        lf = tk.Frame(frame, bg=self.bg_color)
        lf.pack(fill=tk.BOTH, expand=True)
        scroll = tk.Scrollbar(lf, orient=tk.VERTICAL)
        self.off_list = tk.Listbox(lf, yscrollcommand=scroll.set, font=("Consolas", 9),
                                   bg="#0d0d1a", fg=self.fg_color, selectbackground=self.accent_color,
                                   borderwidth=0, highlightthickness=0)
        scroll.config(command=self.off_list.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.off_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.off_items = sorted(OFFICE_KEYS.keys())
        for item in self.off_items:
            self.off_list.insert(tk.END, f"{item:50s} | {OFFICE_KEYS[item]}")

        bf = tk.Frame(frame, bg=self.bg_color)
        bf.pack(fill=tk.X, pady=10)
        tk.Button(bf, text="ACTIVATE SELECTED", font=("Segoe UI", 11, "bold"),
                  bg="#4ecca3", fg="#1a1a2e", padx=20, pady=8, bd=0, cursor="hand2",
                  command=self.activate_office).pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="AUTO DETECT OFFICE", font=("Segoe UI", 10),
                  bg=self.button_color, fg=self.fg_color, padx=15, pady=8, bd=0, cursor="hand2",
                  command=self.auto_detect_office).pack(side=tk.LEFT, padx=5)

    def filter_off_list(self):
        s = self.off_search.get().lower()
        self.off_list.delete(0, tk.END)
        for item in self.off_items:
            if s in item.lower() or s in OFFICE_KEYS[item].lower():
                self.off_list.insert(tk.END, f"{item:50s} | {OFFICE_KEYS[item]}")

    # ========== AUTO TAB ==========
    def build_auto_tab(self):
        frame = ttk.Frame(self.auto_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=20)

        tk.Label(frame, text="AUTO DETECT & ACTIVATE", font=("Segoe UI", 16, "bold"),
                fg="#4ecca3", bg=self.bg_color).pack(pady=(0, 10))
        tk.Label(frame, text="Automatically detect installed Windows & Office and activate them.", 
                font=("Segoe UI", 11), fg=self.fg_color, bg=self.bg_color).pack(pady=10)

        bf = tk.Frame(frame, bg=self.bg_color)
        bf.pack(pady=15)
        tk.Button(bf, text="ACTIVATE WINDOWS", font=("Segoe UI", 12, "bold"),
                  bg="#0f3460", fg=self.fg_color, padx=25, pady=12, bd=0, cursor="hand2",
                  command=self.auto_activate_windows).pack(side=tk.LEFT, padx=10)
        tk.Button(bf, text="ACTIVATE OFFICE", font=("Segoe UI", 12, "bold"),
                  bg="#0f3460", fg=self.fg_color, padx=25, pady=12, bd=0, cursor="hand2",
                  command=self.auto_activate_office).pack(side=tk.LEFT, padx=10)

        tk.Button(frame, text="ACTIVATE ALL (Windows + Office)", font=("Segoe UI", 14, "bold"),
                  bg="#4ecca3", fg="#1a1a2e", padx=35, pady=15, bd=0, cursor="hand2",
                  command=self.auto_activate_all).pack(pady=15)

    # ========== LOG TAB ==========
    def build_log_tab(self):
        frame = ttk.Frame(self.log_tab_frame)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        tk.Label(frame, text="Activation Log", font=("Segoe UI", 12, "bold"),
                fg="#4ecca3", bg=self.bg_color).pack(anchor=tk.W, pady=(0, 8))

        lf = tk.Frame(frame, bg=self.bg_color)
        lf.pack(fill=tk.BOTH, expand=True)
        self.log_txt = tk.Text(lf, font=("Consolas", 10), bg="#0d0d1a", fg="#00ff00",
                               insertbackground=self.fg_color, borderwidth=0, highlightthickness=0,
                               state=tk.DISABLED, wrap=tk.WORD)
        scroll = tk.Scrollbar(lf, orient=tk.VERTICAL, command=self.log_txt.yview)
        self.log_txt.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Button(frame, text="Clear Log", font=("Segoe UI", 9),
                  bg=self.button_color, fg=self.fg_color, padx=10, pady=3, bd=0, cursor="hand2",
                  command=self.clear_log).pack(pady=5, anchor=tk.E)

    def log(self, msg, level="info"):
        self.log_txt.config(state=tk.NORMAL)
        colors = {"info": "#00ff00", "success": "#4ecca3", "error": "#ff4444", "warn": "#ffaa00"}
        tags = {"info": "info", "success": "success", "error": "error", "warn": "warn"}
        color = colors.get(level, "#00ff00")
        tag = tags.get(level, "info")
        bold = "bold" if level == "success" else "normal"
        self.log_txt.tag_config(tag, foreground=color, font=("Consolas", 10, bold))
        self.log_txt.insert(tk.END, f"[{level.upper()}] {msg}\n", tag)
        self.log_txt.see(tk.END)
        self.log_txt.config(state=tk.DISABLED)
        self.root.update_idletasks()

    def clear_log(self):
        self.log_txt.config(state=tk.NORMAL)
        self.log_txt.delete(1.0, tk.END)
        self.log_txt.config(state=tk.DISABLED)

    def run_cmd(self, cmd, timeout=30):
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, startupinfo=si)
            return r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            return "Command timed out."
        except Exception as e:
            return str(e)

    def disable_btns(self):
        for child in self.root.winfo_children():
            self._disable_recursive(child)
        self.root.update_idletasks()

    def _disable_recursive(self, widget):
        if isinstance(widget, (tk.Button, ttk.Button)):
            try:
                widget.config(state=tk.DISABLED)
            except:
                pass
        try:
            for c in widget.winfo_children():
                self._disable_recursive(c)
        except:
            pass

    def enable_btns(self):
        for child in self.root.winfo_children():
            self._enable_recursive(child)
        self.root.update_idletasks()

    def _enable_recursive(self, widget):
        if isinstance(widget, (tk.Button, ttk.Button)):
            try:
                widget.config(state=tk.NORMAL)
            except:
                pass
        for c in widget.winfo_children():
            self._enable_recursive(c)

    # ========== ACTIVATION FUNCTIONS ==========
    def activate_windows(self):
        sel = self.win_list.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a Windows edition.")
            return
        line = self.win_list.get(sel[0])
        parts = line.split(" | ")
        if len(parts) < 2:
            return
        name = parts[0].strip()
        key = parts[1].strip()

        self.log(f"Activating Windows: {name} (Key: {key})", "info")
        self.log(f"KMS: {KMS_SERVER}", "info")
        self.log("-" * 50, "info")

        def run():
            self.disable_btns()
            try:
                self.log("Step 1: Installing product key...", "info")
                o = self.run_cmd(f'slmgr /ipk {key}')
                self.log(o, "info")

                self.log("Step 2: Setting KMS server...", "info")
                o = self.run_cmd(f'slmgr /skms {KMS_SERVER}')
                self.log(o, "info")

                self.log("Step 3: Activating...", "info")
                o = self.run_cmd('slmgr /ato')
                self.log(o, "info")

                st = self.run_cmd('slmgr /xpr')
                self.log(st, "info")

                if "activated" in (o + st).lower() or "successful" in o.lower():
                    self.log("WINDOWS ACTIVATED SUCCESSFULLY!", "success")
                    messagebox.showinfo("Success", f"Windows ({name}) activated!")
                else:
                    messagebox.showinfo("Check Log", "Please check the Log tab for details.")
            except Exception as e:
                self.log(f"Error: {str(e)}", "error")
            finally:
                self.enable_btns()

        threading.Thread(target=run, daemon=True).start()

    def activate_office(self):
        sel = self.off_list.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select an Office edition.")
            return
        line = self.off_list.get(sel[0])
        parts = line.split(" | ")
        if len(parts) < 2:
            return
        name = parts[0].strip()
        key = parts[1].strip()

        self.log(f"Activating Office: {name}", "info")
        self.log(f"Key: {key} | KMS: {KMS_SERVER}", "info")
        self.log("-" * 50, "info")

        def run():
            self.disable_btns()
            try:
                paths = [
                    os.path.expandvars(r"%ProgramFiles%\Microsoft Office\Office16"),
                    os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft Office\Office16"),
                    os.path.expandvars(r"%ProgramFiles%\Microsoft Office\Office15"),
                    os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft Office\Office15"),
                    os.path.expandvars(r"%ProgramFiles%\Microsoft Office\Office14"),
                    os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft Office\Office14"),
                ]
                osp = None
                for p in paths:
                    if os.path.exists(os.path.join(p, "ospp.vbs")):
                        osp = p
                        self.log(f"Office found at: {p}", "info")
                        break

                if osp:
                    self.log("Step 1: Installing product key...", "info")
                    o = self.run_cmd(f'cd /d "{osp}" && cscript ospp.vbs /inpkey:{key}')
                    self.log(o, "info")

                    self.log("Step 2: Setting KMS server...", "info")
                    o = self.run_cmd(f'cd /d "{osp}" && cscript ospp.vbs /sethst:{KMS_SERVER}')
                    self.log(o, "info")

                    self.log("Step 3: Activating...", "info")
                    o = self.run_cmd(f'cd /d "{osp}" && cscript ospp.vbs /act')
                    self.log(o, "info")

                    if "successful" in o.lower() or "product activation successful" in o.lower():
                        self.log("OFFICE ACTIVATED SUCCESSFULLY!", "success")
                        messagebox.showinfo("Success", f"Office ({name}) activated!")
                    else:
                        messagebox.showinfo("Check Log", "Please check the Log tab for details.")
                else:
                    self.log("Office not found. Please install Office first.", "error")
                    messagebox.showerror("Not Found", "Office installation not detected.")
            except Exception as e:
                self.log(f"Error: {str(e)}", "error")
            finally:
                self.enable_btns()

        threading.Thread(target=run, daemon=True).start()

    def check_windows_status(self):
        self.log("Checking Windows activation status...", "info")
        def run():
            self.disable_btns()
            try:
                o = self.run_cmd('slmgr /xpr')
                self.log(o, "info")
                if "activated" in o.lower():
                    self.log("Windows is activated.", "success")
                else:
                    self.log("Windows is NOT activated.", "warn")
            except Exception as e:
                self.log(f"Error: {str(e)}", "error")
            finally:
                self.enable_btns()
        threading.Thread(target=run, daemon=True).start()

    def auto_detect_office(self):
        self.log("Auto-detecting Office...", "info")
        def run():
            self.disable_btns()
            try:
                found = False
                for base in [os.path.expandvars(r"%ProgramFiles%"), os.path.expandvars(r"%ProgramFiles(x86)%")]:
                    for ver in ["Office16", "Office15", "Office14"]:
                        p = os.path.join(base, "Microsoft Office", ver, "ospp.vbs")
                        if os.path.exists(p):
                            found = True
                            path = os.path.dirname(p)
                            self.log(f"Office found at: {path}", "info")
                            o = self.run_cmd(f'cd /d "{path}" && cscript ospp.vbs /dstatus')
                            self.log(o, "info")
                            o = self.run_cmd(f'cd /d "{path}" && cscript ospp.vbs /sethst:{KMS_SERVER}')
                            self.log(o, "info")
                            o = self.run_cmd(f'cd /d "{path}" && cscript ospp.vbs /act')
                            self.log(o, "info")
                            if "successful" in o.lower():
                                self.log("OFFICE ACTIVATED!", "success")
                                messagebox.showinfo("Success", "Office activated!")
                            else:
                                self.log("Office activation attempted - check log.", "info")
                            break
                    if found:
                        break
                if not found:
                    self.log("Office not found in standard locations.", "warn")
                    messagebox.showwarning("Not Found", "Office installation not detected.")
            except Exception as e:
                self.log(f"Error: {str(e)}", "error")
            finally:
                self.enable_btns()
        threading.Thread(target=run, daemon=True).start()

    def auto_activate_windows(self):
        self.log("Auto-activating Windows...", "info")
        def run():
            self.disable_btns()
            try:
                keys_to_try = [
                    ("W269N-WFGWX-YVC9B-4J6C9-T83GX", "Windows 10/11 Pro"),
                    ("TX9XD-98N7V-6WMQ6-BX7FG-H8Q99", "Windows 10 Home"),
                    ("NPPR9-FWDCX-D2C8J-H872K-2YT43", "Windows 10/11 Enterprise"),
                    ("NW6C2-QMPVW-D7KKK-3GKT6-VCFB2", "Windows 10/11 Education"),
                ]
                activated = False
                for key, name in keys_to_try:
                    self.log(f"Trying {name}...", "info")
                    self.run_cmd(f'slmgr /ipk {key}')
                    self.run_cmd(f'slmgr /skms {KMS_SERVER}')
                    o = self.run_cmd('slmgr /ato')
                    self.log(o, "info")
                    if "successful" in o.lower() or "activated" in o.lower():
                        activated = True
                        self.log(f"Windows activated with {name} key!", "success")
                        break
                if activated:
                    self.run_cmd('slmgr /xpr')
                    messagebox.showinfo("Success", "Windows activated!")
                else:
                    messagebox.showwarning("Manual Needed", "Please select your Windows edition manually.")
            except Exception as e:
                self.log(f"Error: {str(e)}", "error")
            finally:
                self.enable_btns()
        threading.Thread(target=run, daemon=True).start()

    def auto_activate_office(self):
        self.log("Auto-activating Office...", "info")
        def run():
            self.disable_btns()
            try:
                found = False
                for base in [os.path.expandvars(r"%ProgramFiles%"), os.path.expandvars(r"%ProgramFiles(x86)%")]:
                    for ver in ["Office16", "Office15", "Office14"]:
                        p = os.path.join(base, "Microsoft Office", ver, "ospp.vbs")
                        if os.path.exists(p):
                            found = True
                            path = os.path.dirname(p)
                            self.log(f"Office at: {path}", "info")
                            self.run_cmd(f'cd /d "{path}" && cscript ospp.vbs /sethst:{KMS_SERVER}')
                            o = self.run_cmd(f'cd /d "{path}" && cscript ospp.vbs /act')
                            self.log(o, "info")
                            if "successful" in o.lower():
                                self.log("OFFICE ACTIVATED!", "success")
                                messagebox.showinfo("Success", "Office activated!")
                            else:
                                self.log("Office activation attempted.", "info")
                            break
                    if found:
                        break
                if not found:
                    messagebox.showwarning("Not Found", "Office not detected.")
            except Exception as e:
                self.log(f"Error: {str(e)}", "error")
            finally:
                self.enable_btns()
        threading.Thread(target=run, daemon=True).start()

    def auto_activate_all(self):
        self.log("=" * 50, "info")
        self.log("ACTIVATING ALL...", "info")
        self.log("=" * 50, "info")
        def run():
            self.disable_btns()
            try:
                # Windows
                keys = [
                    ("W269N-WFGWX-YVC9B-4J6C9-T83GX", "Pro"),
                    ("TX9XD-98N7V-6WMQ6-BX7FG-H8Q99", "Home"),
                    ("NPPR9-FWDCX-D2C8J-H872K-2YT43", "Enterprise"),
                ]
                win_ok = False
                for k, n in keys:
                    self.run_cmd(f'slmgr /ipk {k}')
                    self.run_cmd(f'slmgr /skms {KMS_SERVER}')
                    o = self.run_cmd('slmgr /ato')
                    if "successful" in o.lower() or "activated" in o.lower():
                        win_ok = True
                        self.log(f"Windows ({n}) activated!", "success")
                        break
                if win_ok:
                    st = self.run_cmd('slmgr /xpr')
                    self.log(st, "info")

                # Office
                off_ok = False
                for base in [os.path.expandvars(r"%ProgramFiles%"), os.path.expandvars(r"%ProgramFiles(x86)%")]:
                    for ver in ["Office16", "Office15", "Office14"]:
                        p = os.path.join(base, "Microsoft Office", ver, "ospp.vbs")
                        if os.path.exists(p):
                            path = os.path.dirname(p)
                            self.run_cmd(f'cd /d "{path}" && cscript ospp.vbs /sethst:{KMS_SERVER}')
                            o = self.run_cmd(f'cd /d "{path}" && cscript ospp.vbs /act')
                            if "successful" in o.lower():
                                off_ok = True
                                self.log("Office activated!", "success")
                            break

                self.log("=" * 50, "info")
                if win_ok:
                    self.log("Windows: ACTIVATED", "success")
                else:
                    self.log("Windows: Manual selection needed", "error")
                if off_ok:
                    self.log("Office: ACTIVATED", "success")
                else:
                    self.log("Office: Not found or manual needed", "error")
                self.log("=" * 50, "info")

                messagebox.showinfo("Done",
                    f"Windows: {'Activated' if win_ok else 'Manual needed'}\n"
                    f"Office: {'Activated' if off_ok else 'Not found/manual needed'}")
            except Exception as e:
                self.log(f"Error: {str(e)}", "error")
            finally:
                self.enable_btns()
        threading.Thread(target=run, daemon=True).start()


def main():
    root = tk.Tk()
    app = ActivatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()