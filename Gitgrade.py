import tkinter as tk
from tkinter import ttk, messagebox
import requests, ast, os
from math import log
from datetime import datetime

BG = "#fff7ed"
CARD = "#ffffff"
TEXT = "#3f2d20"
ACCENT = "#ea580c"
GOOD = "#15803d"
BAD = "#b91c1c"

_api_cache = {}
_branch_cache = {}

def api_get(url):
    if url in _api_cache:
        return _api_cache[url]
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200 and r.text.strip():
            data = r.json()
        else:
            data = None
    except:
        data = None
    _api_cache[url] = data
    return data

def get_text(url):
    try:
        r = requests.get(url, timeout=10)
        return r.text if r.status_code == 200 else ""
    except:
        return ""

def parse_url(url):
    url = url.split("?")[0].rstrip("/")
    if "github.com" in url:
        parts = url.replace("https://github.com/", "").split("/")
        return parts[0], parts[1] if len(parts) > 1 else None
    return url, None

def get_repos(user):
    repos = api_get(f"https://api.github.com/users/{user}/repos") or []
    repos.sort(key=lambda r: r.get("updated_at", ""), reverse=True)
    return repos[:5]

def get_default_branch(user, repo):
    key = f"{user}/{repo}"
    if key in _branch_cache:
        return _branch_cache[key]
    data = api_get(f"https://api.github.com/repos/{user}/{repo}") or {}
    branch = data.get("default_branch", "main")
    _branch_cache[key] = branch
    return branch

def detect_languages(user, repo, tree):
    langs = api_get(f"https://api.github.com/repos/{user}/{repo}/languages")
    if langs:
        return list(langs.keys())

    found = set()
    for f in tree:
        ext = os.path.splitext(f["path"])[1]
        if ext == ".py": found.add("Python")
        if ext == ".js": found.add("JavaScript")
        if ext == ".java": found.add("Java")
        if ext == ".cpp": found.add("C++")
        if ext == ".c": found.add("C")
        if ext == ".html": found.add("HTML")
        if ext == ".css": found.add("CSS")
    return list(found) or ["Mixed / Unknown"]

def analyze_python(code):
    try:
        t = ast.parse(code)
    except:
        return 0, 0, 0
    funcs = [n for n in ast.walk(t) if isinstance(n, ast.FunctionDef)]
    classes = [n for n in ast.walk(t) if isinstance(n, ast.ClassDef)]
    lens = [len(f.body) for f in funcs] or [0]
    return len(funcs), len(classes), sum(lens)/len(lens)

def evaluate_repo(user, repo):
    branch = get_default_branch(user, repo)

    tree_data = api_get(
        f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"
    ) or {}

    tree = tree_data.get("tree", [])
    tree_size = len(tree)
    sample = tree[:120]

    py_files = [f["path"] for f in sample if f["path"].endswith(".py")]

    tests = any("test" in p.lower() for p in py_files)
    ci = any(".github/workflows" in f["path"] for f in tree)

    class_count = avg_len = 0
    for p in py_files[:3]:
        code = get_text(f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{p}")
        _, c, l = analyze_python(code)
        class_count += c
        avg_len += l
    avg_len /= max(len(py_files[:3]), 1)

    structure = min(30, log(tree_size + 1) * 10 + class_count)
    quality = min(30, 30 - abs(avg_len - 12) * 2)
    readiness = (10 if tests else 0) + (15 if ci else 0)

    readme = api_get(f"https://api.github.com/repos/{user}/{repo}/readme")
    docs = min(15, len(readme.get("content", "")) // 300) if readme else 0

    total = round(structure + quality + readiness + docs, 1)

    return {
        "repo": repo,
        "languages": detect_languages(user, repo, sample),
        "total": total,
        "structure": structure,
        "quality": quality,
        "tests": tests,
        "ci": ci,
        "docs": docs,
        "size": tree_size
    }

def developer_level(score):
    if score >= 80: return "Advanced"
    if score >= 50: return "Intermediate"
    return "Beginner"

def strengths(d):
    s = [f"Uses {', '.join(d['languages'])}"]
    if d["structure"] >= 18: s.append("Well-organized project structure")
    if d["tests"]: s.append("Includes test files")
    if d["ci"]: s.append("CI pipeline configured")
    if d["docs"] >= 8: s.append("Readable documentation")
    return s

def suggestions(d):
    s = []
    if "Python" in d["languages"] and d["quality"] < 18:
        s.append("Refactor Python code and follow PEP8")
    if d["size"] < 30:
        s.append("Expand project scope with more features")
    if not d["tests"]:
        s.append("Add unit tests")
    if not d["ci"]:
        s.append("Add GitHub Actions CI")
    if d["docs"] < 8:
        s.append("Improve README documentation")
    return s

def roadmap(level):
    if level == "Beginner":
        return ["Learn clean structuring", "Practice testing", "Understand CI/CD"]
    if level == "Intermediate":
        return ["Improve coverage", "Use design patterns", "Automate pipelines"]
    return ["Optimize performance", "Contribute to open source", "Architect scalable systems"]

class GitGradeApp:
    def __init__(self, root):
        self.root = root
        root.title("GitGrade")
        root.geometry("980x800")
        root.configure(bg=BG)

        tk.Label(root, text="GitGrade", bg=BG, fg=ACCENT,
                 font=("Helvetica", 26, "bold")).pack(pady=6)

        top = tk.Frame(root, bg=BG)
        top.pack()

        self.url = tk.Entry(top, width=55)
        self.url.pack(side="left", padx=6)

        tk.Button(top, text="Analyze", bg=ACCENT, fg="white",
                  command=self.analyze).pack(side="left")

        self.loading = tk.Label(root, bg=BG, fg=ACCENT)
        self.loading.pack()

        self.summary = tk.LabelFrame(root, text="Profile Summary",
                                     bg=CARD, fg=TEXT)
        self.summary.pack(fill="x", padx=14, pady=6)
        self.summary_label = tk.Label(self.summary, bg=CARD, fg=TEXT)
        self.summary_label.pack(anchor="w", padx=10, pady=4)

        info = tk.LabelFrame(root, text="What GitGrade Evaluates",
                             bg=CARD, fg=TEXT)
        info.pack(fill="x", padx=14, pady=6)

        tk.Label(
            info,
            text=(
                "• Project structure (files & folders)\n"
                "• Code quality heuristics (sampled files)\n"
                "• Documentation presence (README)\n"
                "• Engineering signals (tests & CI workflows)\n\n"
                "Note: Analysis is based on public GitHub data and sampling."
            ),
            bg=CARD,
            fg=TEXT,
            justify="left",
            wraplength=900
        ).pack(anchor="w", padx=10, pady=6)

        self.canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
        self.scroll = ttk.Scrollbar(root, orient="vertical",
                                   command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=BG)

        self.inner.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0,0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

    def analyze(self):
        self.loading.config(text="Analyzing repositories (this may take a few seconds)…")
        self.root.update_idletasks()

        for w in self.inner.winfo_children():
            w.destroy()

        user, repo = parse_url(self.url.get())
        repos = [{"name": repo}] if repo else get_repos(user)

        if not repos:
            messagebox.showerror(
                "Error",
                "No repositories found.\n\n"
                "GitHub may have rate-limited the request.\n"
                "Try again after some time."
            )
            self.loading.config(text="")
            return

        results = [evaluate_repo(user, r["name"]) for r in repos]
        avg = round(sum(r["total"] for r in results)/len(results), 1)
        level = developer_level(avg)

        timestamp = datetime.now().strftime("%d %b %Y, %H:%M")
        self.summary_label.config(
            text=(
                f"Overall Score: {avg} / 100    |    Developer Level: {level}\n"
                f"Repositories Analyzed: {len(results)}    |    Time: {timestamp}"
            )
        )

        for d in results:
            box = tk.LabelFrame(self.inner,
                text=f"{d['repo']} — {d['total']} / 100",
                bg=CARD, fg=TEXT)
            box.pack(fill="x", padx=8, pady=6)

            for s in strengths(d):
                tk.Label(box, text="✔ " + s, bg=CARD, fg=GOOD).pack(anchor="w", padx=10)

            for s in suggestions(d):
                tk.Label(box, text="⚠ " + s, bg=CARD, fg=BAD).pack(anchor="w", padx=10)

        end = tk.LabelFrame(self.inner, text="Roadmap",
                            bg=CARD, fg=TEXT)
        end.pack(fill="x", padx=8, pady=10)
        for i, step in enumerate(roadmap(level), 1):
            tk.Label(end, text=f"{i}. {step}",
                     bg=CARD, fg=TEXT).pack(anchor="w", padx=10)

        self.loading.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    GitGradeApp(root)
    root.mainloop()
