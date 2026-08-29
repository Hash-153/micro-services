import os

def count_lines(directory="."):
    extensions = {
        ".ts", ".js", ".py", ".sql", ".json", ".yaml", ".yml",
        ".md", ".proto", ".sh", ".toml"
    }
    exclude_dirs = {"node_modules", "dist", ".git", ".idea", ".vscode", "coverage", "__pycache__"}
    
    total_lines = 0
    file_counts = {}
    lang_counts = {}
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in extensions or f in {".gitignore", ".env.example", "Dockerfile", "LICENSE"}:
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as file:
                        lines = len(file.readlines())
                        total_lines += lines
                        file_counts[path] = lines
                        lang = ext or f
                        lang_counts[lang] = lang_counts.get(lang, 0) + lines
                except Exception as e:
                    print(f"Error reading {path}: {e}")
                    
    print("=" * 60)
    print(f"TOTAL LINES OF CODE: {total_lines:,}")
    print("=" * 60)
    print("Lines by extension/file type:")
    for lang, count in sorted(lang_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {lang:15}: {count:8,}")
    print("=" * 60)
    return total_lines

if __name__ == "__main__":
    count_lines()
