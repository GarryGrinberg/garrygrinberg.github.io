import re

files = ["slot.html", "archive.html", "about.html", "privacy-policy.html", "terms.html"]

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    # We will simply find the <nav> block and replace it.
    match = re.search(r'<nav>.*?</nav>', content, re.DOTALL)
    if match:
        old_nav = match.group(0)
        
        # Build new nav based on active state
        new_nav = "<nav>\n"
        new_nav += f'  <a href="index.html"{" class=\\"active\\"" if f == "index.html" else ""}>Home</a>\n'
        new_nav += f'  <a href="archive.html"{" class=\\"active\\"" if f == "archive.html" else ""}>Archive</a>\n'
        new_nav += f'  <a href="slot.html"{" class=\\"active\\"" if f == "slot.html" else ""}>Game</a>\n'
        new_nav += f'  <a href="about.html"{" class=\\"active\\"" if f == "about.html" else ""}>About</a>\n'
        new_nav += f'  <a href="terms.html"{" class=\\"active\\"" if f == "terms.html" else ""}>Terms</a>\n'
        new_nav += "</nav>"
        
        content = content.replace(old_nav, new_nav)
        
        with open(f, 'w') as file:
            file.write(content)

print(f"Fixed root navs.")
