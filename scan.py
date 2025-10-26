import os, json
from bs4 import BeautifulSoup

translations = {}

def extract_text(content):
    soup = BeautifulSoup(content, 'html.parser')
    texts = [t.strip() for t in soup.stripped_strings if t.strip()]
    return texts

def check_accessibility(content):
    soup = BeautifulSoup(content, 'html.parser')
    issues = []

    for img in soup.find_all('img'):
        if not img.get('alt'):
            issues.append(f"Missing alt attribute on image: {img}")

    for el in soup.find_all():
        if el.name == 'button' and not el.text.strip():
            issues.append(f"Button missing accessible label: {el}")
    return issues

def scan_directory(path):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.html') or file.endswith('.jsx'):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    texts = extract_text(content)
                    for t in texts:
                        translations.setdefault(t, None)

                    a11y_issues = check_accessibility(content)
                    if a11y_issues:
                        with open("accessibility_report.txt", "a") as a:
                            a.write(f"File: {file}\n" + "\n".join(a11y_issues) + "\n---\n")

if __name__ == "__main__":
    import sys
    scan_directory(sys.argv[1])
    with open("missing_translations.json", "w") as out:
        json.dump(translations, out, indent=2, ensure_ascii=False)
    print("Scan complete! Reports generated.")
