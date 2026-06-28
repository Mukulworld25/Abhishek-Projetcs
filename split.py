import os
import re

src = r'C:\Users\admin\Downloads\proactive_dental_homepage.html'
dest_dir = r'd:\SAGE DO ASSETS\Imges\Alisha\Abhishek flat'
html_dest = os.path.join(dest_dir, 'index.html')
css_dest = os.path.join(dest_dir, 'style.css')
js_dest = os.path.join(dest_dir, 'script.js')

with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract styles
style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
styles = style_match.group(1) if style_match else ''

# Replace style block with link
new_html = re.sub(
    r'<style>.*?</style>', 
    '<link rel="stylesheet" href="style.css">\n    <script src="script.js" defer></script>', 
    content, 
    flags=re.DOTALL
)

# Save files
with open(css_dest, 'w', encoding='utf-8') as f:
    f.write(styles)

with open(html_dest, 'w', encoding='utf-8') as f:
    f.write(new_html)

# Extract and save JS (which might be inline in onclick, etc, but we will make a clean script.js)
js_content = """
function toggleMenu() {
    const menu = document.getElementById("mobileMenu");
    const hamburger = document.getElementById("hamburger");
    if(menu) menu.classList.toggle("open");
}

window.addEventListener("scroll", () => {
    const nav = document.getElementById("mainNav");
    if (nav) {
        if (window.scrollY > 10) {
            nav.classList.add("scrolled");
        } else {
            nav.classList.remove("scrolled");
        }
    }
});
"""
with open(js_dest, 'w', encoding='utf-8') as f:
    f.write(js_content)

print('Separated HTML, CSS, and JS successfully.')
