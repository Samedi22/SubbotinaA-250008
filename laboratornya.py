import tkinter as tk
from tkinter import ttk
import math
from datetime import datetime

# ══════════════════════════════════════════════════════════
#                       ЦВЕТА
# ══════════════════════════════════════════════════════════
BG         = "#1e1e2e"
SIDEBAR    = "#181825"
CARD       = "#252537"
CARD_HOVER = "#2d2d44"
BORDER     = "#313244"
ACCENT     = "#89b4fa"
ACCENT_L   = "#b4befe"
ACCENT_2   = "#a6e3a1"
ACCENT_3   = "#f9e2af"
ACCENT_4   = "#cba6f7"
ERROR      = "#f38ba8"
TEXT       = "#cdd6f4"
SUBTEXT    = "#7f849c"
ENTRY_BG   = "#313244"
MUTED_BTN  = "#45475a"

FONT_H1     = ("Segoe UI", 20, "bold")
FONT_LABEL  = ("Segoe UI", 10)
FONT_INPUT  = ("Segoe UI", 11)
FONT_RESULT = ("Segoe UI", 15, "bold")
FONT_SMALL  = ("Segoe UI", 9)
FONT_TINY   = ("Segoe UI", 8)
FONT_NAV    = ("Segoe UI", 11)
FONT_MONO   = ("Consolas", 11, "bold")


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def mix(c1, c2, t):
    a, b = hex_rgb(c1), hex_rgb(c2)
    return "#{:02x}{:02x}{:02x}".format(
        *[int(a[i] + (b[i] - a[i]) * t) for i in range(3)])


# ══════════════════════════════════════════════════════════
#                         ВИДЖЕТЫ
# ══════════════════════════════════════════════════════════
def divider(parent, pady=10, color=BORDER):
    tk.Frame(parent, bg=color, height=1).pack(fill="x", pady=pady)


def styled_entry(parent, width=18):
    wrap = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
    e = tk.Entry(wrap, font=FONT_INPUT, bg=ENTRY_BG, fg=TEXT,
                 insertbackground=ACCENT, relief="flat", width=width)
    e.pack(ipady=6, ipadx=4)
    return wrap, e


def styled_button(parent, text, command, color=ACCENT, hover=None):
    hover = hover or ACCENT_L
    btn = tk.Button(parent, text=text, command=command,
                    font=("Segoe UI", 10, "bold"),
                    bg=color, fg="#1e1e2e",
                    activebackground=hover, activeforeground="#1e1e2e",
                    relief="flat", cursor="hand2",
                    padx=18, pady=8, borderwidth=0)
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


def circle_badge(parent, text, size=30, bg=None):
    bg = bg or BG
    cv = tk.Canvas(parent, width=size, height=size, bg=bg,
                   highlightthickness=0, bd=0)
    r = size // 2
    cv.create_oval(1, 1, size - 1, size - 1,
                   fill=ACCENT, outline=ACCENT_L, width=1)
    cv.create_text(r, r, text=text, fill="#1e1e2e",
                   font=("Segoe UI", 10, "bold"))
    return cv


def section_header(parent, num, title):
    box = tk.Frame(parent, bg=BG)
    box.pack(fill="x", padx=45, pady=(38, 0))

    top = tk.Frame(box, bg=BG)
    top.pack(anchor="w")
    circle_badge(top, num, 32).pack(side="left", padx=(0, 14))
    tk.Label(top, text=title, bg=BG, fg=TEXT, font=FONT_H1).pack(side="left")

    tk.Frame(box, bg=ACCENT, height=2, width=52).pack(anchor="w", pady=(14, 0))


def card_container(parent, subtitle=None, padx=28, pady=22):
    outer = tk.Frame(parent, bg=BORDER)
    outer.pack(fill="x", padx=45, pady=20)
    inner = tk.Frame(outer, bg=CARD, padx=padx, pady=pady)
    inner.pack(fill="both", expand=True, padx=1, pady=1)

    if subtitle:
        head = tk.Frame(inner, bg=CARD)
        head.pack(fill="x", pady=(0, 14))

        tk.Frame(head, bg=ACCENT, width=3, height=16).pack(side="left", padx=(0, 10))

        tk.Label(head, text=subtitle, bg=CARD, fg=SUBTEXT,
                 font=("Segoe UI", 9, "italic"),
                 anchor="w", justify="left", wraplength=680)\
            .pack(side="left", fill="x", expand=True)

        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=(0, 18))

    return inner

# ══════════════════════════════════════════════════════════
#                    ЛОГОТИП С ОРБИТОЙ
# ══════════════════════════════════════════════════════════
class LogoBadge(tk.Canvas):
    def __init__(self, parent, size=92):
        super().__init__(parent, width=size, height=size, bg=SIDEBAR,
                         highlightthickness=0, bd=0)
        self.size = size
        self.angle = 0
        self._build()
        self._animate()

    def _build(self):
        s, r = self.size, self.size // 2
        self.create_oval(2, 2, s - 2, s - 2, outline=BORDER, width=1)
        inner_r = r - 12
        for i in range(inner_r, 0, -1):
            t = 1 - i / inner_r
            self.create_oval(r - i, r - i, r + i, r + i,
                             fill=mix(ACCENT, ACCENT_4, t), outline="")
        self.create_text(r, r, text="01", fill="#1e1e2e",
                         font=("Segoe UI", 24, "bold"))
        self.dot = self.create_oval(0, 0, 0, 0, fill=ACCENT_L, outline="")

    def _animate(self):
        s, r = self.size, self.size // 2
        orbit = r - 5
        rad = math.radians(self.angle)
        cx = r + orbit * math.cos(rad)
        cy = r + orbit * math.sin(rad)
        self.coords(self.dot, cx - 4, cy - 4, cx + 4, cy + 4)
        self.angle = (self.angle + 6) % 360
        self.after(60, self._animate)

# ══════════════════════════════════════════════════════════
#                    ПЛИТКА-ПРАВИЛО
# ══════════════════════════════════════════════════════════
def rule_tile(parent, condition, verdict, accent):
    outer = tk.Frame(parent, bg=BORDER)
    outer.pack(side="left", fill="both", expand=True, padx=4)

    tile = tk.Frame(outer, bg=CARD_HOVER, padx=14, pady=14)
    tile.pack(fill="both", expand=True, padx=1, pady=1)
    tk.Frame(tile, bg=accent, height=3).pack(fill="x", pady=(0, 12))

    tk.Label(tile, text=condition, bg=CARD_HOVER, fg=TEXT,
             font=FONT_MONO, justify="center").pack()

    tk.Label(tile, text="↓", bg=CARD_HOVER, fg=SUBTEXT,
             font=("Segoe UI", 13, "bold")).pack(pady=6)
    pill = tk.Frame(tile, bg=accent)
    pill.pack()
    tk.Label(pill, text=verdict, bg=accent, fg="#1e1e2e",
             font=("Segoe UI", 9, "bold"),
             padx=12, pady=4).pack()

# ══════════════════════════════════════════════════════════
#                          ЗАДАНИЕ 1.1
# ══════════════════════════════════════════════════════════
def build_triangle(parent, app):
    f = tk.Frame(parent, bg=BG)
    section_header(f, "01", "Площадь треугольника")

    c = card_container(
        f,
        subtitle="Формула Герона:  S = √( p·(p−a)·(p−b)·(p−c) ),   где p = (a+b+c) / 2")

    entries = {}
    for name, sym in [("Сторона a", "a"),
                      ("Сторона b", "b"),
                      ("Сторона c", "c")]:
        row = tk.Frame(c, bg=CARD); row.pack(fill="x", pady=7)
        tk.Label(row, text=name, bg=CARD, fg=TEXT, font=FONT_LABEL,
                 width=12, anchor="w").pack(side="left")
        tk.Label(row, text=f"{sym} =", bg=CARD, fg=SUBTEXT,
                 font=FONT_LABEL).pack(side="left", padx=(0, 8))
        wrap, e = styled_entry(row, width=18)
        wrap.pack(side="left")
        entries[sym] = e

    res_box = tk.Frame(f, bg=BG)
    res_box.pack(fill="x", padx=45, pady=(10, 0))
    res_var = tk.StringVar(value="Введите стороны и нажмите «Вычислить»")
    res_lbl = tk.Label(res_box, textvariable=res_var, bg=BG, fg=SUBTEXT,
                       font=FONT_RESULT, wraplength=760,
                       justify="left", anchor="w")
    res_lbl.pack(fill="x")

    def calc():
        try:
            a = float(entries["a"].get().replace(",", "."))
            b = float(entries["b"].get().replace(",", "."))
            cc = float(entries["c"].get().replace(",", "."))
        except ValueError:
            res_var.set("Введите корректные числа"); res_lbl.config(fg=ERROR)
            app.set_status("Ошибка: нечисловой ввод", "err"); return
        if min(a, b, cc) <= 0:
            res_var.set("Стороны должны быть положительными")
            res_lbl.config(fg=ERROR)
            app.set_status("Ошибка: отрицательные стороны", "err"); return
        if a + b <= cc or a + cc <= b or b + cc <= a:
            res_var.set("Треугольник с такими сторонами не существует")
            res_lbl.config(fg=ERROR)
            app.set_status("Ошибка: неравенство треугольника", "err"); return
        p = (a + b + cc) / 2
        s = math.sqrt(p * (p - a) * (p - b) * (p - cc))
        res_var.set(f"S  =  {s:.2f}"); res_lbl.config(fg=ACCENT_2)
        app.set_status(f"Площадь вычислена: {s:.2f}", "ok")

    def clear():
        for e in entries.values(): e.delete(0, tk.END)
        res_var.set("Введите стороны и нажмите «Вычислить»")
        res_lbl.config(fg=SUBTEXT)
        app.set_status("Поля очищены", "idle")

    row = tk.Frame(f, bg=BG); row.pack(fill="x", padx=45, pady=(24, 0))
    styled_button(row, "Вычислить", calc).pack(side="left")
    styled_button(row, "Очистить", clear,
                  color=MUTED_BTN, hover="#585b70").pack(side="left", padx=8)

    for e in entries.values():
        e.bind("<Return>", lambda ev: calc())

    f.first_input = entries["a"]
    return f

# ══════════════════════════════════════════════════════════
#                          ЗАДАНИЕ 1.2
# ══════════════════════════════════════════════════════════
UNITS = {"км": 1000.0, "м": 1.0, "см": 0.01,
         "мм": 0.001, "мили": 1609.344, "ярды": 0.9144}


def build_converter(parent, app):
    f = tk.Frame(parent, bg=BG)
    section_header(f, "02", "Конвертер расстояний")

    c = card_container(
        f,
        subtitle="Поддерживаемые единицы:  километры · метры · сантиметры · миллиметры · мили · ярды")

    row1 = tk.Frame(c, bg=CARD); row1.pack(fill="x", pady=7)
    tk.Label(row1, text="Значение", bg=CARD, fg=TEXT, font=FONT_LABEL,
             width=12, anchor="w").pack(side="left")
    wrap, val_entry = styled_entry(row1, width=22)
    wrap.pack(side="left")

    row2 = tk.Frame(c, bg=CARD); row2.pack(fill="x", pady=7)
    tk.Label(row2, text="Из", bg=CARD, fg=TEXT, font=FONT_LABEL,
             width=12, anchor="w").pack(side="left")
    from_var = tk.StringVar(value="км")
    ttk.Combobox(row2, textvariable=from_var, values=list(UNITS.keys()),
                 state="readonly", font=FONT_INPUT, width=20).pack(side="left")

    arrow = tk.Frame(c, bg=CARD); arrow.pack(fill="x", pady=2)
    tk.Label(arrow, text="↓", bg=CARD, fg=ACCENT,
             font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=110)

    row3 = tk.Frame(c, bg=CARD); row3.pack(fill="x", pady=7)
    tk.Label(row3, text="В", bg=CARD, fg=TEXT, font=FONT_LABEL,
             width=12, anchor="w").pack(side="left")
    to_var = tk.StringVar(value="м")
    ttk.Combobox(row3, textvariable=to_var, values=list(UNITS.keys()),
                 state="readonly", font=FONT_INPUT, width=20).pack(side="left")

    res_box = tk.Frame(f, bg=BG)
    res_box.pack(fill="x", padx=45, pady=(10, 0))
    res_var = tk.StringVar(value="Введите значение и нажмите «Конвертировать»")
    res_lbl = tk.Label(res_box, textvariable=res_var, bg=BG, fg=SUBTEXT,
                       font=FONT_RESULT, wraplength=760,
                       justify="left", anchor="w")
    res_lbl.pack(fill="x")

    def convert():
        try:
            v = float(val_entry.get().replace(",", "."))
        except ValueError:
            res_var.set("Введите корректное число"); res_lbl.config(fg=ERROR)
            app.set_status("Ошибка: нечисловой ввод", "err"); return
        res = (v * UNITS[from_var.get()]) / UNITS[to_var.get()]
        res_var.set(f"{v:g} {from_var.get()}   =   {res:.6g} {to_var.get()}")
        res_lbl.config(fg=ACCENT_2)
        app.set_status(f"{from_var.get()} → {to_var.get()}: {res:.6g}", "ok")

    def clear():
        val_entry.delete(0, tk.END)
        res_var.set("Введите значение и нажмите «Конвертировать»")
        res_lbl.config(fg=SUBTEXT)
        app.set_status("Поля очищены", "idle")

    row = tk.Frame(f, bg=BG); row.pack(fill="x", padx=45, pady=(24, 0))
    styled_button(row, "Конвертировать", convert).pack(side="left")
    styled_button(row, "Очистить", clear,
                  color=MUTED_BTN, hover="#585b70").pack(side="left", padx=8)

    val_entry.bind("<Return>", lambda ev: convert())
    f.first_input = val_entry
    return f

# ══════════════════════════════════════════════════════════
#                          ЗАДАНИЕ 1.3
# ══════════════════════════════════════════════════════════
def build_leap(parent, app):
    f = tk.Frame(parent, bg=BG)
    section_header(f, "03", "Високосный год?")

    c = card_container(
        f,
        subtitle="Год делится на 4, но не на 100 — кроме случаев деления на 400")
    row = tk.Frame(c, bg=CARD); row.pack(fill="x")
    tk.Label(row, text="Год", bg=CARD, fg=TEXT, font=FONT_LABEL,
             width=12, anchor="w").pack(side="left")
    wrap, year_entry = styled_entry(row, width=18)
    wrap.pack(side="left")

    divider(c, pady=18)
    tk.Label(c, text="ПРАВИЛА", bg=CARD, fg=SUBTEXT,
             font=("Segoe UI", 9, "bold"), anchor="w")\
        .pack(fill="x", pady=(0, 10))

    tiles = tk.Frame(c, bg=CARD)
    tiles.pack(fill="x")

    rule_tile(tiles, "год % 400 == 0",       "ВИСОКОСНЫЙ",  ACCENT_2)
    rule_tile(tiles, "год % 100 == 0\nи % 400 ≠ 0", "НЕ ВИСОКОСНЫЙ", ERROR)
    rule_tile(tiles, "год % 4 == 0",         "ВИСОКОСНЫЙ",  ACCENT_2)

    res_box = tk.Frame(f, bg=BG)
    res_box.pack(fill="x", padx=45, pady=(24, 0))
    res_var = tk.StringVar(value="Введите год")
    res_lbl = tk.Label(res_box, textvariable=res_var, bg=BG, fg=SUBTEXT,
                       font=("Segoe UI", 18, "bold"),
                       wraplength=760, justify="left", anchor="w")
    res_lbl.pack(fill="x")

    def check(event=None):
        try:
            y = int(year_entry.get().strip())
            if y < 1: raise ValueError
        except ValueError:
            res_var.set("Введите корректный год"); res_lbl.config(fg=ERROR)
            app.set_status("Ошибка: некорректный год", "err"); return
        if y % 400 == 0 or (y % 4 == 0 and y % 100 != 0):
            res_var.set(f"{y}  —  високосный"); res_lbl.config(fg=ACCENT_2)
            app.set_status(f"{y} — високосный", "ok")
        else:
            res_var.set(f"{y}  —  не високосный"); res_lbl.config(fg=ACCENT_3)
            app.set_status(f"{y} — не високосный", "idle")

    def clear():
        year_entry.delete(0, tk.END)
        res_var.set("Введите год"); res_lbl.config(fg=SUBTEXT)
        app.set_status("Поля очищены", "idle")

    btn_row = tk.Frame(f, bg=BG); btn_row.pack(fill="x", padx=45, pady=(24, 0))
    styled_button(btn_row, "Проверить", check).pack(side="left")
    styled_button(btn_row, "Очистить", clear,
                  color=MUTED_BTN, hover="#585b70").pack(side="left", padx=8)

    year_entry.bind("<Return>", check)
    f.first_input = year_entry
    return f

# ══════════════════════════════════════════════════════════
#                            APP
# ══════════════════════════════════════════════════════════
class App:
    def __init__(self, root):
        self.root = root
        self.active = None

        root.title("Лабораторная работа №01")
        root.configure(bg=BG)
        root.geometry("1120x740")
        root.minsize(1000, 680)

        root.option_add("*TCombobox*Listbox.background", ENTRY_BG)
        root.option_add("*TCombobox*Listbox.foreground", TEXT)
        root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
        root.option_add("*TCombobox*Listbox.selectForeground", "#1e1e2e")
        root.option_add("*TCombobox*Listbox.font", FONT_INPUT)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=ENTRY_BG, background=ENTRY_BG,
                        foreground=TEXT, arrowcolor=ACCENT, borderwidth=0)
        style.map("TCombobox",
                  fieldbackground=[("readonly", ENTRY_BG)],
                  foreground=[("readonly", TEXT)],
                  selectbackground=[("readonly", ENTRY_BG)],
                  selectforeground=[("readonly", TEXT)],
                  arrowcolor=[("readonly", ACCENT)])

        try:
            from ctypes import windll, byref, sizeof, c_int
            HWND = windll.user32.GetParent(root.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(
                HWND, 20, byref(c_int(1)), sizeof(c_int))
        except Exception:
            pass

        self._build_sidebar()

        self.main = tk.Frame(root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self.pages = {
            "tri":  build_triangle(self.main, self),
            "conv": build_converter(self.main, self),
            "leap": build_leap(self.main, self),
        }

        self._bind_hotkeys()
        self._tick_clock()
        self.show("tri")

    def _build_sidebar(self):
        side = tk.Frame(self.root, bg=SIDEBAR, width=290)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        self.sidebar = side

        logo_box = tk.Frame(side, bg=SIDEBAR)
        logo_box.pack(fill="x", pady=(36, 0))
        LogoBadge(logo_box, size=96).pack()

        tk.Label(logo_box, text="ЛАБОРАТОРНАЯ", bg=SIDEBAR, fg=SUBTEXT,
                 font=("Segoe UI", 10, "bold")).pack(pady=(18, 2))
        tk.Label(logo_box, text="№01", bg=SIDEBAR, fg=TEXT,
                 font=("Segoe UI", 22, "bold")).pack()
        tk.Label(logo_box, text="Ввод/вывод · Условия", bg=SIDEBAR, fg=SUBTEXT,
                 font=FONT_SMALL).pack(pady=(4, 0))

        divider(side, pady=26)

        tk.Label(side, text="ЗАДАНИЯ", bg=SIDEBAR, fg=SUBTEXT,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=32)

        self.nav = {}
        for key, num, title in [
            ("tri",  "01", "Площадь треугольника"),
            ("conv", "02", "Конвертер"),
            ("leap", "03", "Високосный год"),
        ]:
            self._make_nav(side, key, num, title)

        footer = tk.Frame(side, bg=SIDEBAR)
        footer.pack(side="bottom", fill="x", padx=28, pady=(0, 20))
        divider(side, pady=0, color="#11111b")

        status_row = tk.Frame(footer, bg=SIDEBAR)
        status_row.pack(fill="x", pady=(14, 6))
        self.status_dot = tk.Label(status_row, text="●", bg=SIDEBAR,
                                    fg=SUBTEXT, font=("Segoe UI", 10))
        self.status_dot.pack(side="left", padx=(0, 8))
        self.status_lbl = tk.Label(status_row, text="Готово",
                                    bg=SIDEBAR, fg=SUBTEXT,
                                    font=FONT_SMALL, anchor="w")
        self.status_lbl.pack(side="left", fill="x", expand=True)

        info_row = tk.Frame(footer, bg=SIDEBAR)
        info_row.pack(fill="x", pady=(2, 0))
        self.clock_lbl = tk.Label(info_row, text="--:--:--", bg=SIDEBAR,
                                  fg=SUBTEXT, font=FONT_SMALL)
        self.clock_lbl.pack(side="right")
        tk.Label(info_row, text="Ctrl+1/2/3", bg=SIDEBAR, fg=SUBTEXT,
                 font=FONT_SMALL).pack(side="left")

    def _make_nav(self, parent, key, num, title):
        row = tk.Frame(parent, bg=SIDEBAR, cursor="hand2")
        row.pack(fill="x", padx=16, pady=2)

        indicator = tk.Frame(row, bg=SIDEBAR, width=3)
        indicator.pack(side="left", fill="y")

        body = tk.Frame(row, bg=SIDEBAR)
        body.pack(side="left", fill="x", expand=True, padx=(14, 12), pady=11)

        badge = tk.Label(body, text=num, bg=SIDEBAR, fg=SUBTEXT,
                         font=("Segoe UI", 10, "bold"),
                         width=3, padx=4, pady=3)
        badge.pack(side="left", padx=(0, 14))

        txt = tk.Label(body, text=title, bg=SIDEBAR, fg=SUBTEXT,
                       font=FONT_NAV, anchor="w")
        txt.pack(side="left", fill="x", expand=True)

        widgets = [row, body, badge, txt, indicator]

        def on_click(_e=None, k=key): self.show(k)
        def on_enter(_e):
            if self.active == key: return
            for w in (row, body, badge, txt): w.config(bg=CARD_HOVER)
            badge.config(fg=ACCENT); txt.config(fg=TEXT)
        def on_leave(_e):
            if self.active == key: return
            for w in (row, body, badge, txt): w.config(bg=SIDEBAR)
            badge.config(fg=SUBTEXT); txt.config(fg=SUBTEXT)

        for w in widgets:
            w.bind("<Button-1>", on_click)
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)

        self.nav[key] = (row, body, badge, txt, indicator)

    def set_status(self, text, kind="idle"):
        colors = {"idle": SUBTEXT, "ok": ACCENT_2,
                  "err": ERROR, "busy": ACCENT_3}
        self.status_dot.config(fg=colors.get(kind, SUBTEXT))
        self.status_lbl.config(text=text)

    def _tick_clock(self):
        self.clock_lbl.config(text=datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self._tick_clock)

    def _bind_hotkeys(self):
        self.root.bind("<Control-Key-1>", lambda e: self.show("tri"))
        self.root.bind("<Control-Key-2>", lambda e: self.show("conv"))
        self.root.bind("<Control-Key-3>", lambda e: self.show("leap"))

    def show(self, key):
        for k, page in self.pages.items():
            page.pack_forget()
            row, body, badge, txt, ind = self.nav[k]
            ind.config(bg=SIDEBAR)
            for w in (row, body, badge, txt): w.config(bg=SIDEBAR)
            badge.config(bg=SIDEBAR, fg=SUBTEXT)
            txt.config(fg=SUBTEXT)

        self.pages[key].pack(fill="both", expand=True)

        row, body, badge, txt, ind = self.nav[key]
        ind.config(bg=ACCENT)
        for w in (row, body, badge, txt): w.config(bg=CARD_HOVER)
        badge.config(bg=ACCENT, fg="#1e1e2e")
        txt.config(fg=TEXT)
        self.active = key

        first = getattr(self.pages[key], "first_input", None)
        if first is not None:
            self.root.after(50, first.focus_set)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()









