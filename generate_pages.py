import os
import re

dest_dir = r'd:\SAGE DO ASSETS\Imges\Alisha\Abhishek flat'
index_path = os.path.join(dest_dir, 'index.html')

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Extract common parts
header_match = re.search(r'(<!DOCTYPE html>.*?<nav class="nav" id="mainNav">.*?</nav>\s*<div class="mobile-menu" id="mobileMenu">.*?</div>\s*</div>)', html, re.DOTALL)
footer_match = re.search(r'(<!-- ═══════════ CTA STRIP ═══════════ -->.*?</body>\s*</html>)', html, re.DOTALL)

header = header_match.group(1) if header_match else ''
footer = footer_match.group(1) if footer_match else ''

# Clean up header to make links relative or to absolute pages
header = header.replace('href="#home"', 'href="index.html"')
header = header.replace('href="#about"', 'href="about.html"')
header = header.replace('href="#services"', 'href="services.html"')
header = header.replace('href="#winston"', 'href="about.html#winston"')
header = header.replace('href="#kids"', 'href="services.html#kids"')
header = header.replace('href="#gallery"', 'href="testimonials.html"')
header = header.replace('href="#contact"', 'href="contact.html"')
header = header.replace('class="active"', '') # remove active class for now

# 1. about.html
about_content = """
<!-- ═══════════ PAGE HEADER ═══════════ -->
<section class="hero" style="min-height: 40vh; padding-top: 120px; align-items: flex-start;">
  <div class="hero-bg" style="background-image: url('https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=1600&q=80');"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner" style="grid-template-columns: 1fr;">
    <div class="hero-content" style="text-align: center; max-width: 800px; margin: 0 auto;">
      <h1 class="hero-h1">About <em>Proactive Dental</em></h1>
      <p class="hero-sub" style="margin: 0 auto;">Dedicated to providing gentle, premium dental care for the Burpengary community since 2010.</p>
    </div>
  </div>
</section>
"""
# Extract anxiety and winston sections
anxiety_match = re.search(r'(<!-- ═══════════ ANXIETY FREE ═══════════ -->.*?</section>)', html, re.DOTALL)
winston_match = re.search(r'(<!-- ═══════════ WINSTON ═══════════ -->.*?</section>)', html, re.DOTALL)
why_match = re.search(r'(<!-- ═══════════ WHY CHOOSE US ═══════════ -->.*?</section>)', html, re.DOTALL)

about_html = header + about_content + (anxiety_match.group(1) if anxiety_match else '') + (winston_match.group(1) if winston_match else '') + (why_match.group(1) if why_match else '') + footer
with open(os.path.join(dest_dir, 'about.html'), 'w', encoding='utf-8') as f:
    f.write(about_html)

# 2. services.html
services_content = """
<!-- ═══════════ PAGE HEADER ═══════════ -->
<section class="hero" style="min-height: 40vh; padding-top: 120px; align-items: flex-start;">
  <div class="hero-bg" style="background-image: url('https://images.unsplash.com/photo-1606811971618-4486d14f3f99?w=1600&q=80');"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner" style="grid-template-columns: 1fr;">
    <div class="hero-content" style="text-align: center; max-width: 800px; margin: 0 auto;">
      <h1 class="hero-h1">Our <em>Services</em></h1>
      <p class="hero-sub" style="margin: 0 auto;">Comprehensive dental treatments for every stage of life.</p>
    </div>
  </div>
</section>
"""
services_match = re.search(r'(<!-- ═══════════ SERVICES ═══════════ -->.*?</section>)', html, re.DOTALL)
kids_match = re.search(r'(<!-- ═══════════ FREE KIDS ═══════════ -->.*?</section>)', html, re.DOTALL)

services_html = header + services_content + (services_match.group(1) if services_match else '') + (kids_match.group(1) if kids_match else '') + footer
with open(os.path.join(dest_dir, 'services.html'), 'w', encoding='utf-8') as f:
    f.write(services_html)

# 3. testimonials.html
testi_content = """
<!-- ═══════════ PAGE HEADER ═══════════ -->
<section class="hero" style="min-height: 40vh; padding-top: 120px; align-items: flex-start;">
  <div class="hero-bg" style="background-image: url('https://images.unsplash.com/photo-1609840114035-3c981b782dfe?w=1600&q=80');"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner" style="grid-template-columns: 1fr;">
    <div class="hero-content" style="text-align: center; max-width: 800px; margin: 0 auto;">
      <h1 class="hero-h1">Patient <em>Stories</em></h1>
      <p class="hero-sub" style="margin: 0 auto;">See why over 5,000 patients trust us with their smiles.</p>
    </div>
  </div>
</section>
"""
testi_match = re.search(r'(<!-- ═══════════ TESTIMONIALS ═══════════ -->.*?</section>)', html, re.DOTALL)
gallery_match = re.search(r'(<!-- ═══════════ GALLERY ═══════════ -->.*?</section>)', html, re.DOTALL)

testi_html = header + testi_content + (testi_match.group(1) if testi_match else '') + (gallery_match.group(1) if gallery_match else '') + footer
with open(os.path.join(dest_dir, 'testimonials.html'), 'w', encoding='utf-8') as f:
    f.write(testi_html)

# 4. contact.html
contact_content = """
<!-- ═══════════ PAGE HEADER ═══════════ -->
<section class="hero" style="min-height: 40vh; padding-top: 120px; align-items: flex-start;">
  <div class="hero-bg" style="background-image: url('https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=1600&q=80');"></div>
  <div class="hero-overlay"></div>
  <div class="hero-inner" style="grid-template-columns: 1fr;">
    <div class="hero-content" style="text-align: center; max-width: 800px; margin: 0 auto;">
      <h1 class="hero-h1">Get In <em>Touch</em></h1>
      <p class="hero-sub" style="margin: 0 auto;">We are ready to welcome you. Book your appointment today.</p>
    </div>
  </div>
</section>
"""
contact_match = re.search(r'(<!-- ═══════════ CONTACT ═══════════ -->.*?</section>)', html, re.DOTALL)
payment_match = re.search(r'(<!-- ═══════════ PAYMENT PLANS ═══════════ -->.*?</section>)', html, re.DOTALL)

contact_html = header + contact_content + (contact_match.group(1) if contact_match else '') + (payment_match.group(1) if payment_match else '') + footer
with open(os.path.join(dest_dir, 'contact.html'), 'w', encoding='utf-8') as f:
    f.write(contact_html)

# Now rewrite index.html header as well to have proper links
index_html = html.replace('href="#home"', 'href="index.html"')
index_html = index_html.replace('href="#about"', 'href="about.html"')
index_html = index_html.replace('href="#services"', 'href="services.html"')
index_html = index_html.replace('href="#winston"', 'href="about.html#winston"')
index_html = index_html.replace('href="#kids"', 'href="services.html#kids"')
index_html = index_html.replace('href="#gallery"', 'href="testimonials.html"')
index_html = index_html.replace('href="#contact"', 'href="contact.html"')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_html)

print("Internal pages generated.")
