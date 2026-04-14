import re

files = ["slot.html", "archive.html", "about.html", "privacy-policy.html", "terms.html", "index.html"]

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    match = re.search(r'<nav>.*?</nav>', content, re.DOTALL)
    if match:
        old_nav = match.group(0)
        
        c_i = ' class="active"' if f == 'index.html' else ''
        c_a = ' class="active"' if f == 'archive.html' else ''
        c_s = ' class="active"' if f == 'slot.html' else ''
        c_o = ' class="active"' if f == 'about.html' else ''
        c_t = ' class="active"' if f == 'terms.html' else ''
        
        new_nav = "<nav>\n"
        new_nav += f'  <a href="index.html"{c_i}>Home</a>\n'
        new_nav += f'  <a href="archive.html"{c_a}>Archive</a>\n'
        new_nav += f'  <a href="slot.html"{c_s}>Game</a>\n'
        new_nav += f'  <a href="about.html"{c_o}>About</a>\n'
        new_nav += f'  <a href="terms.html"{c_t}>Terms</a>\n'
        new_nav += "</nav>"
        
        content = content.replace(old_nav, new_nav)
        
        with open(f, 'w') as file:
            file.write(content)

print(f"Fixed root navs.")
