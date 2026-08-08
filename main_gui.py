"""
Student Management System — Lavish Edition (GUI)
====================================================
A polished Tkinter front-end built on top of the existing backend
data model (Student.py + Student.json + data.json).

This file talks directly to the same JSON files your console app
uses (Student.json for students, data.json for user accounts) so
data stays fully compatible between the console version and this
GUI. It re-implements the same validation rules as your original
StudentManager / auth / forgot modules, just driven by widgets
instead of input().

Run with:  python3 main_gui.py
(Student.py must be in the same folder.)
"""
import json
import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox

from Student import Student
import theme as T

# ---------------------------------------------------------------------------
# Paths / constants  (same filenames as the original console app)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENT_FILE = os.path.join(BASE_DIR, "data/Student.json")
USER_FILE = os.path.join(BASE_DIR, "data/data.json")

GENDERS = ["Male", "Female", "Other"]
DEPARTMENTS = ["Software Engineering", "Computer Science",
               "Artifical Inteligence", "Computer Engineering"]
SEMESTERS = [str(i) for i in range(1, 9)]
ADMIN_USER, ADMIN_PASS = "admin", "admin"
DELETE_PIN = "1122"

# Make sure the JSON files exist so first run never blows up.
if not os.path.exists(STUDENT_FILE):
    with open(STUDENT_FILE, "w") as f:
        json.dump([], f)
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump([], f)


# ---------------------------------------------------------------------------
# Data helpers (mirrors StudentManager / auth logic, no input()/print())
# ---------------------------------------------------------------------------
def load_students():
    try:
        with open(STUDENT_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_students(students):
    with open(STUDENT_FILE, "w") as f:
        json.dump(students, f, indent=4)


def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)


def is_valid_name(v):
    return bool(v) and v.replace(" ", "").isalpha()


def is_valid_email(v):
    return "@" in v and "." in v


def is_valid_phone(v):
    return v.isdigit() and len(v) == 11


# ---------------------------------------------------------------------------
# Small reusable widgets — rounded gold buttons, styled entries, cards
# ---------------------------------------------------------------------------
def round_points(x1, y1, x2, y2, r):
    return [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]


class GButton(tk.Canvas):
    """A rounded, hover-aware button drawn on a Canvas for a premium feel."""

    def __init__(self, parent, text, command=None, width=220, height=44,
                 bg=T.ACCENT, hover_bg=T.ACCENT_SOFT, fg=T.BG_MAIN,
                 font=T.FONT_BTN, outline=""):
        super().__init__(parent, width=width, height=height,
                          bg=parent["bg"] if isinstance(parent, (tk.Frame, tk.Canvas)) else T.BG_PANEL,
                          highlightthickness=0, bd=0)
        self.command = command
        self.bg_color = bg
        self.hover_color = hover_bg
        self.fg = fg
        self.font = font
        self.width = width
        self.height = height
        self.outline = outline
        self.text = text
        self._draw(bg)
        self.bind("<Enter>", lambda e: self._draw(self.hover_color))
        self.bind("<Leave>", lambda e: self._draw(self.bg_color))
        self.bind("<Button-1>", self._on_click)

    def _draw(self, color):
        self.delete("all")
        pts = round_points(2, 2, self.width - 2, self.height - 2, 12)
        self.create_polygon(pts, smooth=True, fill=color, outline=self.outline)
        self.create_text(self.width / 2, self.height / 2, text=self.text,
                          fill=self.fg, font=self.font)

    def _on_click(self, event):
        if self.command:
            self.command()

    def set_enabled(self, enabled):
        if enabled:
            self.bind("<Button-1>", self._on_click)
            self._draw(self.bg_color)
        else:
            self.unbind("<Button-1>")
            self._draw(T.TEXT_MUTED)


def styled_entry(parent, show=None, width=28):
    e = tk.Entry(parent, font=T.FONT_BODY, bg=T.BG_PANEL_2, fg=T.TEXT_LIGHT,
                 insertbackground=T.ACCENT, relief="flat", width=width,
                 highlightthickness=1, highlightbackground=T.ACCENT_DARK,
                 highlightcolor=T.ACCENT, show=show if show else "")
    e.configure(borderwidth=8)
    return e


def styled_combo(parent, values, width=26):
    cb = ttk.Combobox(parent, values=values, state="readonly",
                       font=T.FONT_BODY, width=width, style="Gold.TCombobox")
    return cb


def field_label(parent, text):
    return tk.Label(parent, text=text, font=T.FONT_BODY_B, bg=parent["bg"], fg=T.ACCENT_SOFT,
                     anchor="w")


def section_title(parent, text, sub=None):
    box = tk.Frame(parent, bg=parent["bg"])
    tk.Label(box, text=text, font=T.FONT_H2, bg=parent["bg"], fg=T.ACCENT).pack(anchor="w")
    if sub:
        tk.Label(box, text=sub, font=T.FONT_SMALL, bg=parent["bg"], fg=T.TEXT_MUTED).pack(anchor="w")
    tk.Frame(box, bg=T.ACCENT_DARK, height=2).pack(fill="x", pady=(6, 0))
    return box


def card(parent):
    outer = tk.Frame(parent, bg=T.ACCENT_DARK, padx=1, pady=1)
    inner = tk.Frame(outer, bg=T.BG_PANEL, padx=24, pady=20)
    inner.pack(fill="both", expand=True)
    return outer, inner


def flash_status(label, text, ok=True):
    label.config(text=text, fg=T.SUCCESS if ok else T.DANGER)


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System — Lavish Edition")
        self.geometry("1080x700")
        self.minsize(960, 640)
        self.configure(bg=T.BG_MAIN)
        self._build_styles()

        self.current_user = None  # username string, for the user dashboard

        self.container = tk.Frame(self, bg=T.BG_MAIN)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for Page in (HomePage, AdminLoginPage, UserLoginPage, SignUpPage,
                     ForgotPage, AdminDashboard, UserDashboard):
            page = Page(self.container, self)
            self.pages[Page.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show("HomePage")

    def _build_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Gold.TCombobox",
                         fieldbackground=T.BG_PANEL_2, background=T.BG_PANEL_2,
                         foreground=T.TEXT_LIGHT, arrowcolor=T.ACCENT,
                         bordercolor=T.ACCENT_DARK, lightcolor=T.BG_PANEL_2,
                         darkcolor=T.BG_PANEL_2)
        style.map("Gold.TCombobox", fieldbackground=[("readonly", T.BG_PANEL_2)],
                   foreground=[("readonly", T.TEXT_LIGHT)])
        self.option_add("*TCombobox*Listbox.background", T.BG_PANEL_2)
        self.option_add("*TCombobox*Listbox.foreground", T.TEXT_LIGHT)
        self.option_add("*TCombobox*Listbox.selectBackground", T.ACCENT_DARK)
        self.option_add("*TCombobox*Listbox.font", T.FONT_BODY)

        style.configure("Treeview", background=T.BG_PANEL_2, fieldbackground=T.BG_PANEL_2,
                         foreground=T.TEXT_LIGHT, rowheight=28, borderwidth=0,
                         font=T.FONT_BODY)
        style.configure("Treeview.Heading", background=T.ACCENT_DARK, foreground=T.BG_MAIN,
                         font=T.FONT_H3, relief="flat")
        style.map("Treeview.Heading", background=[("active", T.ACCENT)])
        style.map("Treeview", background=[("selected", T.ACCENT_DARK)],
                   foreground=[("selected", T.BG_MAIN)])

        style.configure("Vertical.TScrollbar", background=T.BG_PANEL_2,
                         troughcolor=T.BG_MAIN, bordercolor=T.BG_MAIN, arrowcolor=T.ACCENT)

    def show(self, name, **kwargs):
        page = self.pages[name]
        if hasattr(page, "on_show"):
            page.on_show(**kwargs)
        page.tkraise()


# ---------------------------------------------------------------------------
# Home / landing page
# ---------------------------------------------------------------------------
class HomePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=T.BG_MAIN)
        self.app = app

        wrap = tk.Frame(self, bg=T.BG_MAIN)
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(wrap, text="✦", font=(T.FONT_FAMILY, 22), bg=T.BG_MAIN, fg=T.ACCENT).pack()
        tk.Label(wrap, text="Student Management System", font=T.FONT_TITLE,
                 bg=T.BG_MAIN, fg=T.ACCENT).pack(pady=(4, 0))
        tk.Label(wrap, text="Excellence  ·  Elegance  ·  Efficiency", font=T.FONT_SUB,
                 bg=T.BG_MAIN, fg=T.TEXT_MUTED).pack(pady=(2, 30))

        btns = tk.Frame(wrap, bg=T.BG_MAIN)
        btns.pack()

        options = [
            ("Admin Login", lambda: app.show("AdminLoginPage")),
            ("User Login", lambda: app.show("UserLoginPage")),
            ("Sign Up", lambda: app.show("SignUpPage")),
            ("Forgot Password", lambda: app.show("ForgotPage")),
            ("Exit", self._exit),
        ]
        for i, (text, cmd) in enumerate(options):
            b = GButton(btns, text, command=cmd, width=280, height=48)
            b.grid(row=i, column=0, pady=8)

    def _exit(self):
        if messagebox.askyesno("Exit", "Thank you very much. Exit the application?"):
            self.app.destroy()


# ---------------------------------------------------------------------------
# Admin login
# ---------------------------------------------------------------------------
class AdminLoginPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=T.BG_MAIN)
        self.app = app
        outer, inner = card(self)
        outer.place(relx=0.5, rely=0.5, anchor="center", width=420)

        section_title(inner, "Admin Login", "Restricted access").pack(fill="x", pady=(0, 20))

        field_label(inner, "Username").pack(fill="x")
        self.user_e = styled_entry(inner, width=30)
        self.user_e.pack(fill="x", pady=(2, 12))

        field_label(inner, "Password").pack(fill="x")
        self.pass_e = styled_entry(inner, show="•", width=30)
        self.pass_e.pack(fill="x", pady=(2, 6))

        self.status = tk.Label(inner, text="", font=T.FONT_SMALL, bg=T.BG_PANEL)
        self.status.pack(fill="x", pady=(4, 10))

        GButton(inner, "Login", command=self._login, width=200, height=42).pack(pady=(4, 8))
        tk.Label(inner, text="← Back to menu", font=T.FONT_SMALL, bg=T.BG_PANEL, fg=T.TEXT_MUTED,
                 cursor="hand2").pack()
        inner.winfo_children()[-1].bind("<Button-1>", lambda e: app.show("HomePage"))

    def on_show(self):
        self.user_e.delete(0, "end")
        self.pass_e.delete(0, "end")
        self.status.config(text="")

    def _login(self):
        u, p = self.user_e.get().strip(), self.pass_e.get().strip()
        if u == ADMIN_USER and p == ADMIN_PASS:
            self.app.show("AdminDashboard")
        else:
            flash_status(self.status, "Admin login failed. Try again.", ok=False)


# ---------------------------------------------------------------------------
# User login
# ---------------------------------------------------------------------------
class UserLoginPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=T.BG_MAIN)
        self.app = app
        outer, inner = card(self)
        outer.place(relx=0.5, rely=0.5, anchor="center", width=420)

        section_title(inner, "User Login", "Sign in to your account").pack(fill="x", pady=(0, 20))

        field_label(inner, "Username / Email").pack(fill="x")
        self.user_e = styled_entry(inner, width=30)
        self.user_e.pack(fill="x", pady=(2, 12))

        field_label(inner, "Password").pack(fill="x")
        self.pass_e = styled_entry(inner, show="•", width=30)
        self.pass_e.pack(fill="x", pady=(2, 6))

        self.status = tk.Label(inner, text="", font=T.FONT_SMALL, bg=T.BG_PANEL)
        self.status.pack(fill="x", pady=(4, 10))

        GButton(inner, "Login", command=self._login, width=200, height=42).pack(pady=(4, 8))
        tk.Label(inner, text="← Back to menu", font=T.FONT_SMALL, bg=T.BG_PANEL, fg=T.TEXT_MUTED,
                 cursor="hand2").pack()
        inner.winfo_children()[-1].bind("<Button-1>", lambda e: app.show("HomePage"))

    def on_show(self):
        self.user_e.delete(0, "end")
        self.pass_e.delete(0, "end")
        self.status.config(text="")

    def _login(self):
        u, p = self.user_e.get().strip(), self.pass_e.get().strip()
        users = load_users()
        for user in users:
            if user.get("username") == u and user.get("password") == p:
                self.app.current_user = u
                self.app.show("UserDashboard")
                return
        flash_status(self.status, "User not found — check your details.", ok=False)


# ---------------------------------------------------------------------------
# Sign up  (mirrors sigin())
# ---------------------------------------------------------------------------
class SignUpPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=T.BG_MAIN)
        self.app = app
        outer, inner = card(self)
        outer.place(relx=0.5, rely=0.5, anchor="center", width=460)

        section_title(inner, "Create Account", "A few details to get you started").pack(fill="x", pady=(0, 16))

        rows = [("First Name", "name_e", {}), ("Father's Name", "father_e", {}),
                ("Email (used as username)", "email_e", {}),
                ("Password (min 8 characters)", "pass_e", {"show": "•"}),
                ("Re-enter Password", "pass2_e", {"show": "•"})]
        for label, attr, opts in rows:
            field_label(inner, label).pack(fill="x")
            e = styled_entry(inner, width=32, **opts)
            e.pack(fill="x", pady=(2, 10))
            setattr(self, attr, e)

        self.status = tk.Label(inner, text="", font=T.FONT_SMALL, bg=T.BG_PANEL, wraplength=380, justify="left")
        self.status.pack(fill="x", pady=(2, 10))

        GButton(inner, "Create Account", command=self._submit, width=220, height=42).pack(pady=(2, 8))
        tk.Label(inner, text="← Back to menu", font=T.FONT_SMALL, bg=T.BG_PANEL, fg=T.TEXT_MUTED,
                 cursor="hand2").pack()
        inner.winfo_children()[-1].bind("<Button-1>", lambda e: app.show("HomePage"))

    def on_show(self):
        for attr in ("name_e", "father_e", "email_e", "pass_e", "pass2_e"):
            getattr(self, attr).delete(0, "end")
        self.status.config(text="")

    def _submit(self):
        name = self.name_e.get().strip()
        fathername = self.father_e.get().strip()
        email = self.email_e.get().strip()
        pw = self.pass_e.get()
        pw2 = self.pass2_e.get()

        if not is_valid_name(name):
            return flash_status(self.status, "First name must contain letters only.", ok=False)
        if not is_valid_name(fathername):
            return flash_status(self.status, "Father's name must contain letters only.", ok=False)
        if not is_valid_email(email):
            return flash_status(self.status, "Please enter a valid email address.", ok=False)
        if len(pw) < 8:
            return flash_status(self.status, "Password must be at least 8 characters.", ok=False)
        if pw != pw2:
            return flash_status(self.status, "Passwords do not match.", ok=False)

        users = load_users()
        if any(u.get("username") == email for u in users):
            return flash_status(self.status, "An account with that email already exists.", ok=False)

        users.append({"name": name, "fathername": fathername, "password": pw, "username": email})
        save_users(users)
        flash_status(self.status, "Account created successfully! You can log in now.", ok=True)


# ---------------------------------------------------------------------------
# Forgot password (mirrors forgot())
# ---------------------------------------------------------------------------
class ForgotPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=T.BG_MAIN)
        self.app = app
        outer, inner = card(self)
        outer.place(relx=0.5, rely=0.5, anchor="center", width=420)

        section_title(inner, "Forgot Password", "Reset your account password").pack(fill="x", pady=(0, 18))

        field_label(inner, "Username / Email").pack(fill="x")
        self.user_e = styled_entry(inner, width=30)
        self.user_e.pack(fill="x", pady=(2, 12))

        field_label(inner, "New Password").pack(fill="x")
        self.pass_e = styled_entry(inner, show="•", width=30)
        self.pass_e.pack(fill="x", pady=(2, 6))

        self.status = tk.Label(inner, text="", font=T.FONT_SMALL, bg=T.BG_PANEL, wraplength=350)
        self.status.pack(fill="x", pady=(4, 10))

        GButton(inner, "Reset Password", command=self._reset, width=220, height=42).pack(pady=(2, 8))
        tk.Label(inner, text="← Back to menu", font=T.FONT_SMALL, bg=T.BG_PANEL, fg=T.TEXT_MUTED,
                 cursor="hand2").pack()
        inner.winfo_children()[-1].bind("<Button-1>", lambda e: app.show("HomePage"))

    def on_show(self):
        self.user_e.delete(0, "end")
        self.pass_e.delete(0, "end")
        self.status.config(text="")

    def _reset(self):
        u = self.user_e.get().strip()
        newpw = self.pass_e.get()
        if not newpw:
            return flash_status(self.status, "Please enter a new password.", ok=False)
        users = load_users()
        for user in users:
            if user.get("username") == u:
                user["password"] = newpw
                save_users(users)
                return flash_status(self.status, "Password changed successfully!", ok=True)
        flash_status(self.status, "User not found.", ok=False)


# ---------------------------------------------------------------------------
# Shared dashboard scaffold: top bar (with logout, always visible) +
# sidebar nav + swappable content area
# ---------------------------------------------------------------------------
class DashboardBase(tk.Frame):
    NAV_ITEMS = []  # list of (label, builder_method_name)
    ICONS = {}      # optional label -> glyph map, purely cosmetic

    def __init__(self, parent, app, heading, role_label="Admin"):
        super().__init__(parent, bg=T.BG_MAIN)
        self.app = app
        self.role_label = role_label

        # ---------------- Top bar (always visible, holds Logout) ----------
        topbar = tk.Frame(self, bg=T.BG_TOPBAR, height=60)
        topbar.pack(side="top", fill="x")
        topbar.pack_propagate(False)

        left = tk.Frame(topbar, bg=T.BG_TOPBAR)
        left.pack(side="left", padx=22)
        tk.Label(left, text="Student Management System", font=T.FONT_H3,
                 bg=T.BG_TOPBAR, fg=T.TEXT_LIGHT).pack(anchor="w", pady=(11, 0))
        tk.Label(left, text=heading, font=T.FONT_SMALL,
                 bg=T.BG_TOPBAR, fg=T.TEXT_MUTED).pack(anchor="w")

        right = tk.Frame(topbar, bg=T.BG_TOPBAR)
        right.pack(side="right", padx=18, pady=10)

        who = self.app.current_user if self.app.current_user else "admin"
        badge = tk.Frame(right, bg=T.BG_PANEL_2, padx=12, pady=6)
        badge.pack(side="left", padx=(0, 12))
        self.badge_label = tk.Label(badge, text=f"●  {role_label}: {who}", font=T.FONT_SMALL,
                                     bg=T.BG_PANEL_2, fg=T.ACCENT_SOFT)
        self.badge_label.pack()

        GButton(right, "⏻  Logout", command=self._logout, width=130, height=38,
                bg=T.DANGER, hover_bg=T.DANGER_HOVER, fg=T.WHITE).pack(side="left")

        tk.Frame(self, bg=T.BORDER, height=1).pack(side="top", fill="x")

        # ---------------- Body: sidebar + content --------------------------
        body = tk.Frame(self, bg=T.BG_MAIN)
        body.pack(side="top", fill="both", expand=True)

        sidebar = tk.Frame(body, bg=T.BG_SIDEBAR, width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        self.nav_frame = tk.Frame(sidebar, bg=T.BG_SIDEBAR)
        self.nav_frame.pack(fill="x", pady=(16, 0))

        content_outer = tk.Frame(body, bg=T.BG_MAIN)
        content_outer.pack(side="left", fill="both", expand=True)
        self.content = tk.Frame(content_outer, bg=T.BG_MAIN)
        self.content.pack(fill="both", expand=True, padx=30, pady=26)

        self._nav_buttons = {}
        self._active_method = None
        self._build_nav()
        self._pages_built = {}

    def _build_nav(self):
        for label, method in self.NAV_ITEMS:
            row = tk.Frame(self.nav_frame, bg=T.BG_SIDEBAR)
            row.pack(fill="x", padx=10, pady=2)

            marker = tk.Frame(row, bg=T.BG_SIDEBAR, width=3)
            marker.pack(side="left", fill="y")

            icon = self.ICONS.get(label, "›")
            b = tk.Label(row, text=f"  {icon}   {label}", font=T.FONT_NAV, bg=T.BG_SIDEBAR,
                         fg=T.TEXT_LIGHT, anchor="w", padx=6, pady=10, cursor="hand2")
            b.pack(side="left", fill="x", expand=True)

            def enter(e, w=b, m=marker, method=method):
                if self._active_method != method:
                    w.config(bg=T.BG_PANEL_2, fg=T.ACCENT_SOFT)
                    m.config(bg=T.BG_PANEL_2)

            def leave(e, w=b, m=marker, method=method):
                if self._active_method != method:
                    w.config(bg=T.BG_SIDEBAR, fg=T.TEXT_LIGHT)
                    m.config(bg=T.BG_SIDEBAR)

            b.bind("<Button-1>", lambda e, m=method: self._open(m))
            row.bind("<Button-1>", lambda e, m=method: self._open(m))
            b.bind("<Enter>", enter)
            b.bind("<Leave>", leave)
            self._nav_buttons[method] = (b, marker)

    def _set_active(self, method_name):
        for m, (lbl, marker) in self._nav_buttons.items():
            if m == method_name:
                lbl.config(bg=T.BG_PANEL_2, fg=T.WHITE, font=T.FONT_H3)
                marker.config(bg=T.ACCENT)
            else:
                lbl.config(bg=T.BG_SIDEBAR, fg=T.TEXT_LIGHT, font=T.FONT_NAV)
                marker.config(bg=T.BG_SIDEBAR)
        self._active_method = method_name

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _open(self, method_name):
        self._clear_content()
        self._set_active(method_name)
        self._add_back_link(self.content)
        getattr(self, method_name)(self.content)

    def _add_back_link(self, parent):
        bar = tk.Frame(parent, bg=T.BG_MAIN)
        bar.pack(fill="x", pady=(0, 18))
        back_btn = GButton(bar, "←  Back to Dashboard", command=self.on_show,
                            width=190, height=36, bg=T.BG_PANEL_2, hover_bg=T.ACCENT_DARK,
                            fg=T.TEXT_LIGHT, font=T.FONT_BODY_B, outline=T.BORDER)
        back_btn.pack(anchor="w")

    def _logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.app.current_user = None
            self.app.show("HomePage")

    def on_show(self):
        self._clear_content()
        self._active_method = None
        for m, (lbl, marker) in self._nav_buttons.items():
            lbl.config(bg=T.BG_SIDEBAR, fg=T.TEXT_LIGHT, font=T.FONT_NAV)
            marker.config(bg=T.BG_SIDEBAR)
        who = self.app.current_user if self.app.current_user else "admin"
        self.badge_label.config(text=f"●  {self.role_label}: {who}")
        self._welcome(self.content)

    def _welcome(self, parent):
        tk.Label(parent, text="Welcome back!", font=T.FONT_TITLE, bg=T.BG_MAIN, fg=T.TEXT_LIGHT).pack(anchor="w")
        tk.Label(parent, text="Choose an action from the menu on the left to get started.",
                 font=T.FONT_BODY, bg=T.BG_MAIN, fg=T.TEXT_MUTED).pack(anchor="w", pady=(6, 0))

    # ---- shared building blocks used by both dashboards -------------
    def _student_table(self, parent, rows, height=14):
        cols = ("id", "name", "father", "age", "dept", "gender", "sem", "cgpa", "phone", "email")
        headers = ["ID", "Name", "Father Name", "Age", "Department", "Gender",
                   "Sem", "CGPA", "Phone", "Email"]
        tv = ttk.Treeview(parent, columns=cols, show="headings", height=height)
        widths = [45, 120, 120, 45, 160, 70, 45, 55, 100, 160]
        for c, h, w in zip(cols, headers, widths):
            tv.heading(c, text=h)
            tv.column(c, width=w, anchor="center" if c not in ("name", "father", "dept", "email") else "w")
        for s in rows:
            tv.insert("", "end", values=(
                s.get("student_id"), s.get("student_name"), s.get("father_name"),
                s.get("age"), s.get("Department", s.get("department", "")), s.get("gender"),
                s.get("semester"), s.get("cgpa"), s.get("phone_no"), s.get("email_address"),
            ))
        return tv

    def _id_lookup_bar(self, parent, on_find):
        bar = tk.Frame(parent, bg=T.BG_MAIN)
        bar.pack(fill="x", pady=(0, 14))
        field_label(bar, "Student ID").pack(side="left", padx=(0, 8))
        e = styled_entry(bar, width=12)
        e.pack(side="left", padx=(0, 10))
        GButton(bar, "Find", command=lambda: on_find(e.get().strip()), width=110, height=36).pack(side="left")
        return e

    # ---------------- View Student (by ID) ----------------
    def page_view_student(self, parent):
        section_title(parent, "View Student", "Look up a student by ID").pack(fill="x", pady=(0, 14))
        result_holder = {}

        def find(sid_text):
            for w in list(result_holder.get("frame", tk.Frame(parent)).winfo_children() if result_holder.get("frame") else []):
                w.destroy()
            if not sid_text.isdigit():
                messagebox.showerror("Invalid ID", "Student ID must be a number.")
                return
            sid = int(sid_text)
            students = load_students()
            found = next((s for s in students if s.get("student_id") == sid), None)
            if "frame" in result_holder:
                result_holder["frame"].destroy()
            frame = self._detail_card(parent, found)
            frame.pack(fill="x", pady=10)
            result_holder["frame"] = frame

        self._id_lookup_bar(parent, find)

    def _detail_card(self, parent, student):
        outer, inner = card(parent)
        if not student:
            tk.Label(inner, text="No student found with that ID.", font=T.FONT_BODY,
                     bg=T.BG_PANEL, fg=T.DANGER).pack()
            return outer
        rows = [
            ("ID", student.get("student_id")),
            ("Name", student.get("student_name")),
            ("Father Name", student.get("father_name")),
            ("Age", student.get("age")),
            ("Department", student.get("Department", student.get("department"))),
            ("Gender", student.get("gender")),
            ("Semester", student.get("semester")),
            ("CGPA", student.get("cgpa")),
            ("Phone", student.get("phone_no")),
            ("Email", student.get("email_address")),
        ]
        for i, (k, v) in enumerate(rows):
            r = tk.Frame(inner, bg=T.BG_PANEL)
            r.pack(fill="x", pady=3)
            tk.Label(r, text=k + ":", font=T.FONT_BODY_B, bg=T.BG_PANEL, fg=T.ACCENT_SOFT,
                     width=14, anchor="w").pack(side="left")
            tk.Label(r, text=str(v), font=T.FONT_BODY, bg=T.BG_PANEL, fg=T.TEXT_LIGHT,
                     anchor="w").pack(side="left")
        return outer

    # ---------------- Search Student (by ID) ----------------
    def page_search_student(self, parent):
        section_title(parent, "Search Student", "Find a student's key details").pack(fill="x", pady=(0, 14))
        holder = {}

        def find(sid_text):
            if "frame" in holder:
                holder["frame"].destroy()
            if not sid_text.isdigit():
                messagebox.showerror("Invalid ID", "Student ID must be a number.")
                return
            sid = int(sid_text)
            students = load_students()
            found = next((s for s in students if s.get("student_id") == sid), None)
            outer, inner = card(parent)
            if not found:
                tk.Label(inner, text="No student found with that ID.", font=T.FONT_BODY,
                         bg=T.BG_PANEL, fg=T.DANGER).pack()
            else:
                for label, val in [("Found ID", found.get("student_id")),
                                    ("Student Name", found.get("student_name")),
                                    ("Department", found.get("Department", found.get("department"))),
                                    ("Current CGPA", found.get("cgpa"))]:
                    r = tk.Frame(inner, bg=T.BG_PANEL)
                    r.pack(fill="x", pady=3)
                    tk.Label(r, text=label + ":", font=T.FONT_BODY_B, bg=T.BG_PANEL, fg=T.ACCENT_SOFT,
                             width=16, anchor="w").pack(side="left")
                    tk.Label(r, text=str(val), font=T.FONT_BODY, bg=T.BG_PANEL, fg=T.TEXT_LIGHT).pack(side="left")
            outer.pack(fill="x", pady=10)
            holder["frame"] = outer

        self._id_lookup_bar(parent, find)

    # ---------------- Update Student ----------------
    def page_update_student(self, parent):
        section_title(parent, "Update Student", "Load a record, edit any field, save").pack(fill="x", pady=(0, 14))
        state = {"student": None}
        form_area = tk.Frame(parent, bg=T.BG_MAIN)

        def find(sid_text):
            for w in form_area.winfo_children():
                w.destroy()
            if not sid_text.isdigit():
                messagebox.showerror("Invalid ID", "Student ID must be a number.")
                return
            sid = int(sid_text)
            students = load_students()
            found = next((s for s in students if s.get("student_id") == sid), None)
            if not found:
                tk.Label(form_area, text="Sorry, that Student ID was not found.",
                         font=T.FONT_BODY, bg=T.BG_MAIN, fg=T.DANGER).pack(anchor="w")
                return
            state["student"] = found
            self._build_update_form(form_area, found)

        self._id_lookup_bar(parent, find)
        form_area.pack(fill="both", expand=True)

    def _build_update_form(self, parent, student):
        outer, inner = card(parent)
        outer.pack(fill="x")

        entries = {}

        def row(label, key, widget_factory):
            r = tk.Frame(inner, bg=T.BG_PANEL)
            r.pack(fill="x", pady=6)
            tk.Label(r, text=label, font=T.FONT_BODY_B, bg=T.BG_PANEL, fg=T.ACCENT_SOFT,
                     width=14, anchor="w").pack(side="left")
            w = widget_factory(r)
            w.pack(side="left", fill="x", expand=True)
            entries[key] = w

        e = styled_entry(inner, width=30)
        row("Name", "student_name", lambda r: styled_entry(r, width=28))
        entries["student_name"].insert(0, student.get("student_name", ""))

        row("Father Name", "father_name", lambda r: styled_entry(r, width=28))
        entries["father_name"].insert(0, student.get("father_name", ""))

        row("Age", "age", lambda r: styled_entry(r, width=28))
        entries["age"].insert(0, str(student.get("age", "")))

        def gender_widget(r):
            cb = styled_combo(r, GENDERS, width=25)
            cb.set(student.get("gender", GENDERS[0]))
            return cb
        row("Gender", "gender", gender_widget)

        def dept_widget(r):
            cb = styled_combo(r, DEPARTMENTS, width=25)
            cb.set(student.get("Department", student.get("department", DEPARTMENTS[0])))
            return cb
        row("Department", "Department", dept_widget)

        def sem_widget(r):
            cb = styled_combo(r, SEMESTERS, width=25)
            cb.set(str(student.get("semester", 1)))
            return cb
        row("Semester", "semester", sem_widget)

        row("CGPA", "cgpa", lambda r: styled_entry(r, width=28))
        entries["cgpa"].insert(0, str(student.get("cgpa", "")))

        row("Phone (11 digits)", "phone_no", lambda r: styled_entry(r, width=28))
        entries["phone_no"].insert(0, str(student.get("phone_no", "")))

        row("Email", "email_address", lambda r: styled_entry(r, width=28))
        entries["email_address"].insert(0, student.get("email_address", ""))

        status = tk.Label(inner, text="", font=T.FONT_SMALL, bg=T.BG_PANEL)
        status.pack(anchor="w", pady=(10, 6))

        def save():
            name = entries["student_name"].get().strip()
            father = entries["father_name"].get().strip()
            age_s = entries["age"].get().strip()
            gender = entries["gender"].get()
            dept = entries["Department"].get()
            sem_s = entries["semester"].get()
            cgpa_s = entries["cgpa"].get().strip()
            phone = entries["phone_no"].get().strip()
            email = entries["email_address"].get().strip()

            if not is_valid_name(name):
                return flash_status(status, "Name must contain letters only.", ok=False)
            if not is_valid_name(father):
                return flash_status(status, "Father name must contain letters only.", ok=False)
            if not age_s.isdigit() or not (15 <= int(age_s) <= 60):
                return flash_status(status, "Age must be a number between 15 and 60.", ok=False)
            try:
                cgpa = float(cgpa_s)
                if not (0.0 <= cgpa <= 4.0):
                    raise ValueError
            except ValueError:
                return flash_status(status, "CGPA must be a number between 0.0 and 4.0.", ok=False)
            if not is_valid_phone(phone):
                return flash_status(status, "Phone number must be exactly 11 digits.", ok=False)
            if not is_valid_email(email):
                return flash_status(status, "Please enter a valid email address.", ok=False)

            students = load_students()
            for s in students:
                if s.get("student_id") == student.get("student_id"):
                    s["student_name"] = name
                    s["father_name"] = father
                    s["age"] = int(age_s)
                    s["gender"] = gender
                    s["Department"] = dept
                    s["semester"] = int(sem_s)
                    s["cgpa"] = cgpa
                    s["phone_no"] = phone
                    s["email_address"] = email
                    break
            save_students(students)
            flash_status(status, "Student record updated successfully!", ok=True)

        GButton(inner, "Save Changes", command=save, width=200, height=42).pack(anchor="w", pady=(4, 0))


# ---------------------------------------------------------------------------
# Admin Dashboard
# ---------------------------------------------------------------------------
class AdminDashboard(DashboardBase):
    NAV_ITEMS = [
        ("Add Student", "page_add_student"),
        ("All Students", "page_all_students"),
        ("View Student", "page_view_student"),
        ("Update Student", "page_update_student"),
        ("Search Student", "page_search_student"),
        ("Delete Student", "page_delete_student"),
        ("Department-wise", "page_department_search"),
        ("Semester-wise", "page_semester_search"),
        ("Highest CGPA", "page_highest_cgpa"),
        ("Lowest CGPA", "page_lowest_cgpa"),
        ("Export to CSV", "page_export_csv"),
    ]

    ICONS = {
        "Add Student": "＋", "All Students": "▤", "View Student": "◎",
        "Update Student": "✎", "Search Student": "🔍", "Delete Student": "🗑",
        "Department-wise": "🏛", "Semester-wise": "📅", "Highest CGPA": "🏆",
        "Lowest CGPA": "⚠", "Export to CSV": "⭳",
    }

    def __init__(self, parent, app):
        super().__init__(parent, app, "Admin Dashboard", role_label="Admin")

    # ---------------- Add Student ----------------
    def page_add_student(self, parent):
        section_title(parent, "Add Student", "Enrol a new student record").pack(fill="x", pady=(0, 14))
        outer, inner = card(parent)
        outer.pack(fill="x")

        entries = {}

        def row(label, key, widget_factory):
            r = tk.Frame(inner, bg=T.BG_PANEL)
            r.pack(fill="x", pady=6)
            tk.Label(r, text=label, font=T.FONT_BODY_B, bg=T.BG_PANEL, fg=T.ACCENT_SOFT,
                     width=16, anchor="w").pack(side="left")
            w = widget_factory(r)
            w.pack(side="left", fill="x", expand=True)
            entries[key] = w

        row("Full Name", "name", lambda r: styled_entry(r, width=30))
        row("Father's Name", "father", lambda r: styled_entry(r, width=30))
        row("Age (15-60)", "age", lambda r: styled_entry(r, width=30))
        row("Gender", "gender", lambda r: styled_combo(r, GENDERS, width=27))
        row("Department", "dept", lambda r: styled_combo(r, DEPARTMENTS, width=27))
        row("CGPA (0.0-4.0)", "cgpa", lambda r: styled_entry(r, width=30))
        row("Email", "email", lambda r: styled_entry(r, width=30))
        row("Phone (11 digits)", "phone", lambda r: styled_entry(r, width=30))
        row("Semester", "sem", lambda r: styled_combo(r, SEMESTERS, width=27))

        status = tk.Label(inner, text="", font=T.FONT_SMALL, bg=T.BG_PANEL, wraplength=420, justify="left")
        status.pack(anchor="w", pady=(10, 6))

        def submit():
            name = entries["name"].get().strip()
            father = entries["father"].get().strip()
            age_s = entries["age"].get().strip()
            gender = entries["gender"].get()
            dept = entries["dept"].get()
            cgpa_s = entries["cgpa"].get().strip()
            email = entries["email"].get().strip()
            phone = entries["phone"].get().strip()
            sem_s = entries["sem"].get()

            if not is_valid_name(name):
                return flash_status(status, "Name must contain letters only.", ok=False)
            if not is_valid_name(father):
                return flash_status(status, "Father's name must contain letters only.", ok=False)
            if not age_s.isdigit() or not (15 <= int(age_s) <= 60):
                return flash_status(status, "Age must be a number between 15 and 60.", ok=False)
            if gender not in GENDERS:
                return flash_status(status, "Please choose a gender.", ok=False)
            if dept not in DEPARTMENTS:
                return flash_status(status, "Please choose a department.", ok=False)
            try:
                cgpa = float(cgpa_s)
                if not (0.0 <= cgpa <= 4.0):
                    raise ValueError
            except ValueError:
                return flash_status(status, "CGPA must be a number between 0.0 and 4.0.", ok=False)
            if not is_valid_email(email):
                return flash_status(status, "Please enter a valid email address.", ok=False)
            if not is_valid_phone(phone):
                return flash_status(status, "Phone number must be exactly 11 digits.", ok=False)
            if sem_s not in SEMESTERS:
                return flash_status(status, "Please choose a semester.", ok=False)

            os.chdir(BASE_DIR)  # Student class reads/writes Student.json via relative path
            new_student = Student(name, father, int(age_s), gender, dept, int(sem_s), cgpa, phone, email)
            new_student.save(new_student.to_dic())
            flash_status(status, f"Student added successfully! Assigned ID: {new_student.student_id}", ok=True)
            for key in ("name", "father", "age", "cgpa", "email", "phone"):
                entries[key].delete(0, "end")

        GButton(inner, "Add Student", command=submit, width=200, height=42).pack(anchor="w", pady=(4, 0))

    # ---------------- All Students (bonus convenience view) ----------------
    def page_all_students(self, parent):
        section_title(parent, "All Students", "Every enrolled student, at a glance").pack(fill="x", pady=(0, 14))
        students = load_students()
        if not students:
            tk.Label(parent, text="No student records yet.", font=T.FONT_BODY,
                     bg=T.BG_MAIN, fg=T.TEXT_MUTED).pack(anchor="w")
            return
        tv = self._student_table(parent, students)
        tv.pack(fill="both", expand=True)

    # ---------------- Delete Student ----------------
    def page_delete_student(self, parent):
        section_title(parent, "Delete Student", "Requires the security PIN").pack(fill="x", pady=(0, 14))
        outer, inner = card(parent)
        outer.pack(fill="x")

        field_label(inner, "Student ID").pack(anchor="w")
        id_e = styled_entry(inner, width=20)
        id_e.pack(anchor="w", pady=(2, 10))

        field_label(inner, "Security PIN").pack(anchor="w")
        pin_e = styled_entry(inner, show="•", width=20)
        pin_e.pack(anchor="w", pady=(2, 10))

        status = tk.Label(inner, text="", font=T.FONT_SMALL, bg=T.BG_PANEL)
        status.pack(anchor="w", pady=(0, 8))

        def do_delete():
            sid_text, pin = id_e.get().strip(), pin_e.get().strip()
            if not sid_text.isdigit():
                return flash_status(status, "Student ID must be a number.", ok=False)
            if pin != DELETE_PIN:
                return flash_status(status, "Incorrect security PIN.", ok=False)
            sid = int(sid_text)
            students = load_students()
            remaining = [s for s in students if s.get("student_id") != sid]
            if len(remaining) == len(students):
                return flash_status(status, "No student found with that ID.", ok=False)
            if not messagebox.askyesno("Confirm Delete", f"Delete student ID {sid}? This cannot be undone."):
                return
            save_students(remaining)
            flash_status(status, f"Student ID {sid} deleted.", ok=True)

        GButton(inner, "Delete Student", command=do_delete, width=200, height=42,
                bg=T.DANGER, hover_bg="#ef7f92").pack(anchor="w")

    # ---------------- Department-wise ----------------
    def page_department_search(self, parent):
        section_title(parent, "Department-wise Students", "").pack(fill="x", pady=(0, 14))
        bar = tk.Frame(parent, bg=T.BG_MAIN)
        bar.pack(fill="x", pady=(0, 12))
        field_label(bar, "Department").pack(side="left", padx=(0, 8))
        cb = styled_combo(bar, DEPARTMENTS, width=28)
        cb.current(0)
        cb.pack(side="left", padx=(0, 10))

        result_area = tk.Frame(parent, bg=T.BG_MAIN)
        result_area.pack(fill="both", expand=True)

        def search():
            for w in result_area.winfo_children():
                w.destroy()
            dept = cb.get()
            students = load_students()
            matches = [s for s in students if s.get("Department", s.get("department")) == dept]
            if not matches:
                tk.Label(result_area, text="No students found in this department.",
                         font=T.FONT_BODY, bg=T.BG_MAIN, fg=T.TEXT_MUTED).pack(anchor="w")
                return
            self._student_table(result_area, matches).pack(fill="both", expand=True)

        GButton(bar, "Search", command=search, width=110, height=36).pack(side="left")

    # ---------------- Semester-wise ----------------
    def page_semester_search(self, parent):
        section_title(parent, "Semester-wise Students", "").pack(fill="x", pady=(0, 14))
        bar = tk.Frame(parent, bg=T.BG_MAIN)
        bar.pack(fill="x", pady=(0, 12))
        field_label(bar, "Semester").pack(side="left", padx=(0, 8))
        cb = styled_combo(bar, SEMESTERS, width=10)
        cb.current(0)
        cb.pack(side="left", padx=(0, 10))

        result_area = tk.Frame(parent, bg=T.BG_MAIN)
        result_area.pack(fill="both", expand=True)

        def search():
            for w in result_area.winfo_children():
                w.destroy()
            sem = int(cb.get())
            students = load_students()
            matches = [s for s in students if s.get("semester") == sem]
            if not matches:
                tk.Label(result_area, text="No students found in this semester.",
                         font=T.FONT_BODY, bg=T.BG_MAIN, fg=T.TEXT_MUTED).pack(anchor="w")
                return
            self._student_table(result_area, matches).pack(fill="both", expand=True)

        GButton(bar, "Search", command=search, width=110, height=36).pack(side="left")

    # ---------------- Highest / Lowest CGPA ----------------
    def page_highest_cgpa(self, parent):
        section_title(parent, "Highest CGPA", "Top-performing student").pack(fill="x", pady=(0, 14))
        students = load_students()
        if not students:
            tk.Label(parent, text="No student records yet.", font=T.FONT_BODY,
                     bg=T.BG_MAIN, fg=T.TEXT_MUTED).pack(anchor="w")
            return
        top = max(students, key=lambda s: s.get("cgpa", 0.0))
        self._detail_card(parent, top).pack(fill="x")

    def page_lowest_cgpa(self, parent):
        section_title(parent, "Lowest CGPA", "Needs the most support").pack(fill="x", pady=(0, 14))
        students = load_students()
        if not students:
            tk.Label(parent, text="No student records yet.", font=T.FONT_BODY,
                     bg=T.BG_MAIN, fg=T.TEXT_MUTED).pack(anchor="w")
            return
        bottom = min(students, key=lambda s: s.get("cgpa", 4.0))
        self._detail_card(parent, bottom).pack(fill="x")

    # ---------------- Export CSV ----------------
    def page_export_csv(self, parent):
        section_title(parent, "Export to CSV", "Save all student records as Students.csv").pack(fill="x", pady=(0, 14))
        outer, inner = card(parent)
        outer.pack(fill="x")
        status = tk.Label(inner, text="", font=T.FONT_SMALL, bg=T.BG_PANEL)
        status.pack(anchor="w", pady=(0, 10))

        def export():
            students = load_students()
            if not students:
                return flash_status(status, "No student records found.", ok=False)
            out_path = os.path.join(BASE_DIR, "Students.csv")
            fieldnames = students[0].keys()
            with open(out_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(students)
            flash_status(status, f"Exported successfully to {out_path}", ok=True)

        GButton(inner, "Export Now", command=export, width=200, height=42).pack(anchor="w")


# ---------------------------------------------------------------------------
# User Dashboard  (View / Update / Search — same permissions as the console app)
# ---------------------------------------------------------------------------
class UserDashboard(DashboardBase):
    NAV_ITEMS = [
        ("View Student", "page_view_student"),
        ("Update Student", "page_update_student"),
        ("Search Student", "page_search_student"),
    ]
    ICONS = {
        "View Student": "◎", "Update Student": "✎", "Search Student": "🔍",
    }

    def __init__(self, parent, app):
        super().__init__(parent, app, "User Dashboard", role_label="User")

    def on_show(self):
        self._clear_content()
        self._active_method = None
        for m, (lbl, marker) in self._nav_buttons.items():
            lbl.config(bg=T.BG_SIDEBAR, fg=T.TEXT_LIGHT, font=T.FONT_NAV)
            marker.config(bg=T.BG_SIDEBAR)
        self.badge_label.config(text=f"●  User: {self.app.current_user or 'Student'}")
        tk.Label(self.content, text=f"Welcome, {self.app.current_user or 'Student'}!",
                 font=T.FONT_TITLE, bg=T.BG_MAIN, fg=T.TEXT_LIGHT).pack(anchor="w")
        tk.Label(self.content, text="Choose an action from the menu on the left.",
                 font=T.FONT_BODY, bg=T.BG_MAIN, fg=T.TEXT_MUTED).pack(anchor="w", pady=(6, 0))


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    os.chdir(BASE_DIR)
    app = App()
    app.mainloop()
