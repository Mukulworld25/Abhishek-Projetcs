import os
import re
import requests
from bs4 import BeautifulSoup

dest_dir = r'd:\SAGE DO ASSETS\Imges\Alisha\Abhishek flat'
original_html_path = r'C:\Users\admin\Downloads\proactive_dental_homepage.html'
base_url = 'https://proactivedental.com.au/'

# Load the original premium homepage HTML template
with open(original_html_path, 'r', encoding='utf-8') as f:
    orig_html = f.read()

# Define the white outline tooth SVG logo path
logo_svg_html = """<svg viewBox="0 0 512 512" fill="none" stroke="currentColor" stroke-width="32" stroke-linecap="round" stroke-linejoin="round">
        <path d="M376 144c-12-40-52-72-104-72-12 0-24 2-36 6-12-4-24-6-36-6-52 0-92 32-104 72-18 62 4 128 16 160 16 43 48 80 48 112 0 16-16 48-16 64 0 24 24 48 48 48 16 0 32-16 48-32 16-16 32-32 48-32s32 16 48 32c16 16 32 32 48 32 24 0 48-24 48-48 0-16-16-48-16-64 0-32 32-69 48-112 12-32 34-98 16-160z"/>
      </svg>"""

nav_links_html = """
    <div class="nav-links">
      <a href="index.html">Home</a>
      <a href="about-us.html">About</a>
      <a href="our-dentists.html">Meet Winston</a>
      <a href="our-services.html">Services</a>
      <a href="free-kids-dental.html">Free Kids Dental</a>
      <a href="smile-gallery.html">Smile Gallery</a>
      <a href="contact-us.html">Contact</a>
    </div>
"""

mobile_links_html = """
<div class="mobile-menu" id="mobileMenu">
  <a href="index.html" onclick="toggleMenu()">Home</a>
  <a href="about-us.html" onclick="toggleMenu()">About</a>
  <a href="our-dentists.html" onclick="toggleMenu()">Meet Winston</a>
  <a href="our-services.html" onclick="toggleMenu()">Services</a>
  <a href="free-kids-dental.html" onclick="toggleMenu()">Free Kids Dental</a>
  <a href="smile-gallery.html" onclick="toggleMenu()">Smile Gallery</a>
  <a href="contact-us.html" onclick="toggleMenu()">Contact</a>
  <div class="mobile-cta">
    <a href="contact-us.html" class="btn btn-primary" onclick="toggleMenu()" style="justify-content:center;width:100%">Book Appointment</a>
  </div>
</div>
"""

# Header template for subpages (updated logo and dark links color fallback)
site_header = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Proactive Dental Burpengary — Gentle, premium dental care for your whole family. Serving Burpengary, Morayfield & Narangba since 2010. Book today: (07) 5433 1569.">
<meta name="keywords" content="dentist Burpengary, dental clinic Morayfield, family dentist Narangba, cosmetic dentistry Queensland, dental implants Burpengary, children's dentist CDBS">
<title>Proactive Dental Burpengary | Gentle Family Dentistry Since 2010</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script src="script.js" defer></script>
</head>
<body>

<!-- ═══════════ NAV ═══════════ -->
<nav class="nav" id="mainNav">
  <div class="container nav-inner">
    <a href="index.html" class="nav-logo">
      """ + logo_svg_html + """
      <div class="nav-logo-text">
        <span class="name">proactive</span>
        <span class="sub">DENTAL</span>
      </div>
    </a>
""" + nav_links_html + """
    <div class="nav-right">
      <a href="tel:0754331569" class="nav-phone">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.67A2 2 0 012 0h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 14v2.92z"/></svg>
        (07) 5433 1569
      </a>
      <a href="contact-us.html" class="btn-book">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        Book Appointment
      </a>
    </div>
    <div class="hamburger" id="hamburger" onclick="toggleMenu()">
      <span></span><span></span><span></span>
    </div>
  </div>
</nav>
""" + mobile_links_html

cta_and_footer_markup = """
<!-- ═══════════ CTA STRIP ═══════════ -->
<section class="cta-strip">
  <div class="container cta-strip-inner">
    <div class="cta-strip-text">Let's get you<br><em>smiling.</em></div>
    <div class="cta-strip-btns">
      <a href="tel:0754331569" class="btn-call">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.67A2 2 0 012 0h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 14v2.92z"/></svg>
        (07) 5433 1569
      </a>
      <a href="contact-us.html" class="btn btn-primary">Book Appointment</a>
    </div>
  </div>
</section>

<!-- ═══════════ FOOTER ═══════════ -->
<footer class="footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <div class="footer-brand-logo">
          """ + logo_svg_html + """
          <div class="nav-logo-text">
            <span class="name" style="color: #fff; font-family: var(--sans); font-size: 20px; font-weight: 700; letter-spacing: -0.5px; line-height: 1;">proactive</span>
            <span class="sub" style="color: rgba(255,255,255,0.7); font-family: var(--sans); font-size: 10px; font-weight: 600; letter-spacing: 4px; text-transform: uppercase; margin-top: 2px;">DENTAL</span>
          </div>
        </div>
        <p class="footer-desc">Gentle, affordable dentistry serving Burpengary, Morayfield, Narangba &amp; Deception Bay since 2010.</p>
        <div class="footer-social">
          <a href="#" class="social-btn">f</a>
          <a href="#" class="social-btn">in</a>
          <a href="#" class="social-btn">g</a>
        </div>
      </div>
      <div>
        <div class="footer-col-title">Explore</div>
        <div class="footer-links">
          <a href="about-us.html">About Us</a>
          <a href="our-dentists.html">Meet Winston</a>
          <a href="our-services.html">Our Services</a>
          <a href="free-kids-dental.html">Free Kids Dental</a>
          <a href="smile-gallery.html">Smile Gallery</a>
          <a href="contact-us.html">Book Appointment</a>
        </div>
      </div>
      <div>
        <div class="footer-col-title">Contact</div>
        <div class="footer-contact-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg><span>Unit 25/115 Buckley Rd, Burpengary East QLD 4505</span></div>
        <div class="footer-contact-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.67A2 2 0 012 0h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 14v2.92z"/></svg><span>(07) 5433 1569</span></div>
        <div class="footer-contact-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg><span>info@proactivedental.com.au</span></div>
      </div>
      <div>
        <div class="footer-col-title">Health Funds</div>
        <div class="footer-funds">
          <span class="footer-fund">Bupa</span>
          <span class="footer-fund">HCF</span>
          <span class="footer-fund">Medibank</span>
          <span class="footer-fund">HICAPS</span>
          <span class="footer-fund">nib</span>
          <span class="footer-fund">AGDVA</span>
        </div>
        <p class="footer-note">HICAPS on-the-spot claiming available.</p>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-copy">© 2026 Proactive Dental Burpengary. All rights reserved.</div>
      <div class="footer-bottom-links">
        <a href="#">Privacy Policy</a>
        <a href="#">Terms of Use</a>
        <a href="contact-us.html">Book Online</a>
      </div>
    </div>
  </div>
</footer>

<script>
// Sticky nav
window.addEventListener('scroll', () => {
  if (window.scrollY > 40) {
    document.getElementById('mainNav').classList.add('scrolled');
  } else {
    document.getElementById('mainNav').classList.remove('scrolled');
  }
});

// Mobile menu
function toggleMenu() {
  document.getElementById('mobileMenu').classList.toggle('open');
}

// Active navigation handling
const currentPage = window.location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.nav-links a, .mobile-menu a').forEach(a => {
  const href = a.getAttribute('href');
  if (href === currentPage) {
    a.classList.add('active');
  } else {
    a.classList.remove('active');
  }
});
</script>
</body>
</html>
"""

def get_links():
    print("Crawling for links...")
    res = requests.get(base_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith(base_url):
            href = href.split('#')[0]
            if href.endswith('/'):
                links.add(href)
    links.add(base_url + 'our-services/general-dentistry/root-canal/')
    return sorted(list(links))

def clean_slug(url):
    slug = url.replace(base_url, '').strip('/')
    if not slug:
        return 'index'
    return slug.replace('/', '_')

links = get_links()
print(f"Found {len(links)} links to scrape.")

for link in links:
    slug = clean_slug(link)
    
    if slug == 'index':
        # Generate the Premium Homepage: index.html
        print(f"Generating Premium Homepage: index.html")
        homepage_html = orig_html
        
        # 1. Replace the style block with our stylesheet link and script
        style_pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
        homepage_html = style_pattern.sub('<link rel="stylesheet" href="style.css">\n<script src="script.js" defer></script>', homepage_html)
        
        # 2. Update the background image to the kids dentist photo
        kids_img_url = "https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=1600&q=80"
        # Find where hero background image or hero-bg is set, or replace any unsplash image in index.html
        homepage_html = re.sub(
            r'https://images\.unsplash\.com/[a-zA-Z0-9_-]+\?w=1600&q=80',
            kids_img_url,
            homepage_html
        )
        # Also replace inside the inline style of hero-bg if present
        homepage_html = re.sub(
            r'background-image:\s*url\([\'\"][^\'\"]*unsplash[^\'\"]*[\'\"]\)',
            f"background-image: url('{kids_img_url}')",
            homepage_html
        )
        
        # 3. Replace the logo SVG with the white contour tooth SVG
        svg_pattern = re.compile(r'<a href="/" class="nav-logo">.*?</a>', re.DOTALL)
        updated_logo = f"""<a href="index.html" class="nav-logo">
      {logo_svg_html}
      <div class="nav-logo-text">
        <span class="name">proactive</span>
        <span class="sub">DENTAL</span>
      </div>
    </a>"""
        homepage_html = svg_pattern.sub(updated_logo, homepage_html)
        
        # Also replace in other nav definitions in the page (like footer or mobile-menu)
        homepage_html = homepage_html.replace('href="#home"', 'href="index.html"')
        homepage_html = homepage_html.replace('href="#about"', 'href="about-us.html"')
        homepage_html = homepage_html.replace('href="#winston"', 'href="our-dentists.html"')
        homepage_html = homepage_html.replace('href="#services"', 'href="our-services.html"')
        homepage_html = homepage_html.replace('href="#kids"', 'href="free-kids-dental.html"')
        homepage_html = homepage_html.replace('href="#gallery"', 'href="smile-gallery.html"')
        homepage_html = homepage_html.replace('href="#contact"', 'href="contact-us.html"')
        
        # 4. Strictly look like screenshot 1: Remove the hero-card (stats card on the right)
        # In original: <div class="hero-card">...</div>
        homepage_html = re.sub(r'<div class="hero-card">.*?</div>\s*</div>\s*</section>', '</div>\n</section>', homepage_html, flags=re.DOTALL)
        # If there is another nested structure, let's clean it up:
        homepage_html = re.sub(r'<div class="hero-card">.*?</div>\s*</div>\s*</div>\s*</section>', '</div>\n</div>\n</section>', homepage_html, flags=re.DOTALL)
        
        # Let's write a targeted regex replacement for <div class="hero-card">...</div> inside the hero section
        card_pattern = re.compile(r'<div class="hero-card">.*?</div>\s*</div>\s*</section>', re.DOTALL)
        homepage_html = card_pattern.sub('</div>\n</section>', homepage_html)
        
        # Save index.html
        with open(os.path.join(dest_dir, 'index.html'), 'w', encoding='utf-8') as fw:
            fw.write(homepage_html)
        continue

    print(f"Scraping: {link} -> {slug}.html")
    try:
        res = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Meta
        title = soup.title.string if soup.title else 'Proactive Dental'
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
        meta_desc = meta_desc_tag['content'] if meta_desc_tag else ''
        
        h1_tag = soup.find('h1')
        h1_text = h1_tag.get_text(strip=True) if h1_tag else slug.replace('_', ' ').replace('-', ' ').title()
        
        main_content = soup.find(id='main-content')
        content_html = ""
        provider_logos = []
        
        if main_content:
            elements = main_content.find_all(['h2', 'h3', 'h4', 'p', 'ul', 'ol', 'img'])
            for el in elements:
                if el.name != 'img' and not el.get_text(strip=True):
                    continue
                if el.find_parent('header') or el.find_parent('footer') or el.find_parent(class_='et-tb-header'):
                    continue
                
                if el.name == 'img':
                    src = el.get('src', '')
                    alt = el.get('alt', '')
                    if src and not src.startswith('data:'):
                        src_lower = src.lower()
                        if any(fund in src_lower for fund in ['medibank', 'bupa', 'hcf', 'hicaps', 'agdva', 'nib']):
                            if src not in provider_logos:
                                provider_logos.append(src)
                        elif any(icon_keyword in src_lower for icon_keyword in ['icon', 'star', 'check', 'bullet']) or 'uploads/2021/08/tooth-new-img.png' in src:
                            content_html += f'<div style="margin:20px 0;"><img src="{src}" alt="{alt}" style="width:48px; height:auto;"></div>\n'
                        else:
                            content_html += f'<div style="margin:30px 0;"><img src="{src}" alt="{alt}" style="border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.06); max-width:100%; height:auto;"></div>\n'
                
                elif el.name in ['h2', 'h3', 'h4']:
                    el_text = el.get_text(strip=True)
                    if any(skip in el_text.lower() for skip in ['preferred providers', 'get in touch', 'opening hours']):
                        continue
                    content_html += f'<{el.name} style="color:var(--navy); margin:36px 0 16px; font-family:var(--serif); line-height:1.25;">{el_text}</{el.name}>\n'
                
                elif el.name == 'p':
                    p_text = el.get_text(strip=True)
                    if 'book an appointment' in p_text.lower() or '(07) 5433' in p_text:
                        continue
                    content_html += f'<p style="color:var(--mid); line-height:1.8; font-size:16px; margin-bottom:20px;">{p_text}</p>\n'
                
                elif el.name in ['ul', 'ol']:
                    content_html += f'<{el.name} style="color:var(--mid); line-height:1.8; font-size:16px; margin-bottom:20px; padding-left:20px;">'
                    for li in el.find_all('li'):
                        content_html += f'<li style="margin-bottom:8px;">{li.get_text(strip=True)}</li>'
                    content_html += f'</{el.name}>\n'
        
        if provider_logos:
            logo_markup = '<div class="fund-logos-row">\n'
            for logo in provider_logos:
                logo_markup += f'  <img src="{logo}" alt="Health Fund Logo" class="fund-logo-img">\n'
            logo_markup += '</div>\n'
            content_html += f'\n<h3 style="color:var(--navy); margin:40px 0 16px; font-family:var(--serif);">Our Preferred Providers</h3>\n' + logo_markup
            
        if not content_html:
            content_html = "<p style='color:var(--mid); padding:40px 0;'>Details for this service are coming soon. Please contact us for more information.</p>"
            
        # Build premium 2-column page layout with blurred kids bg for subpages
        kids_bg_url = "https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=1600&q=80"
        hero = f"""
        <!-- ═══════════ PAGE HEADER ═══════════ -->
        <section class="hero" style="min-height: 38vh; padding-top: 120px; align-items: flex-start; background: var(--navy);">
          <div class="hero-bg" style="background-image: url('{kids_bg_url}');"></div>
          <div class="hero-overlay" style="background: linear-gradient(105deg, rgba(11,61,78,0.95) 0%, rgba(11,61,78,0.8) 100%); backdrop-filter: blur(5px);"></div>
          <div class="hero-inner" style="grid-template-columns: 1fr; z-index: 10;">
            <div class="hero-content" style="text-align: center; max-width: 800px; margin: 0 auto; animation: fadeUp 0.8s ease;">
              <h1 class="hero-h1" style="font-size: clamp(32px, 4.5vw, 54px);">{h1_text}</h1>
              <p class="hero-sub" style="margin: 10px auto 0; font-size:16px; color: rgba(255,255,255,0.75);">{meta_desc}</p>
            </div>
          </div>
        </section>
        
        <main class="page-content" style="background: var(--light); padding: 80px 24px;">
            <div class="container">
                <div class="inner-page-grid">
                    <!-- Main content column -->
                    <article class="page-main-column">
                        {content_html}
                    </article>
                    
                    <!-- Sticky Sidebar column -->
                    <aside class="page-sidebar">
                        <!-- Quick Links widget -->
                        <div class="sidebar-widget">
                            <h3 class="widget-title">Dental Services</h3>
                            <ul class="widget-links">
                                <li><a href="our-services_general-dentistry_dental-implants.html">Dental Implants</a></li>
                                <li><a href="our-services_general-dentistry_wisdom-teeth.html">Wisdom Teeth</a></li>
                                <li><a href="our-services_general-dentistry_crowns.html">Dental Crowns</a></li>
                                <li><a href="our-services_cosmetic-dentistry_veneers.html">Dental Veneers</a></li>
                                <li><a href="our-services_orthodontics.html">Orthodontics</a></li>
                                <li><a href="our-services_cosmetic-dentistry_teeth-whitening-bleaching.html">Teeth Whitening</a></li>
                                <li><a href="our-services_dentures-burpengary_dentures.html">Dentures</a></li>
                                <li><a href="our-services_general-dentistry_root-canal.html">Root Canal Treatment</a></li>
                            </ul>
                        </div>
                        
                        <!-- Booking CTA Widget -->
                        <div class="sidebar-widget sidebar-cta" style="padding: 30px;">
                            <h3 class="widget-title">Need a Dentist?</h3>
                            <p style="color: rgba(255,255,255,0.8); font-size: 14px; margin-bottom: 20px; line-height: 1.6;">Book your appointment online or call our gentle team in Burpengary East.</p>
                            <a href="tel:0754331569" class="btn btn-primary" style="background: var(--teal); color: #fff; width: 100%; justify-content: center; font-size: 14px; font-weight:700;">Call (07) 5433 1569</a>
                            <a href="contact-us.html" class="btn btn-outline" style="width: 100%; justify-content: center; font-size: 14px; font-weight:700; border-color: rgba(255,255,255,0.45); margin-top:10px;">Book Online</a>
                        </div>
                        
                        <!-- Hours Widget -->
                        <div class="sidebar-widget">
                            <h3 class="widget-title">Opening Hours</h3>
                            <div class="hours-row" style="display:flex; justify-content:space-between; font-size:13.5px; color:var(--mid); padding:8px 0; border-bottom:1px solid var(--light2);"><span style="font-weight:600; color:var(--dark);">Mon - Fri:</span> <span>8:30 AM - 5:00 PM</span></div>
                            <div class="hours-row" style="display:flex; justify-content:space-between; font-size:13.5px; color:var(--mid); padding:8px 0; border-bottom:1px solid var(--light2);"><span style="font-weight:600; color:var(--dark);">Saturday:</span> <span>By Appointment</span></div>
                            <div class="hours-row" style="display:flex; justify-content:space-between; font-size:13.5px; color:var(--mid); padding:8px 0;"><span style="font-weight:600; color:var(--dark);">Sunday:</span> <span style="color:#E05C5C; font-weight: 600;">Closed</span></div>
                        </div>
                    </aside>
                </div>
            </div>
        </main>
        """
        
        new_header = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', site_header)
        new_header = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{meta_desc}">', new_header)
        
        full_html = new_header + hero + cta_and_footer_markup
        
        file_path = os.path.join(dest_dir, f"{slug}.html")
        with open(file_path, 'w', encoding='utf-8') as fw:
            fw.write(full_html)
            
    except Exception as e:
        print(f"Failed to scrape {link}: {e}")

# Create copies of main files for legacy links
legacy_mappings = {
    'about.html': 'about-us.html',
    'services.html': 'our-services.html',
    'testimonials.html': 'smile-gallery.html',
    'contact.html': 'contact-us.html',
    'kids.html': 'free-kids-dental.html'
}

for legacy, actual in legacy_mappings.items():
    actual_path = os.path.join(dest_dir, actual)
    legacy_path = os.path.join(dest_dir, legacy)
    if os.path.exists(actual_path):
        print(f"Creating Legacy Alias: {legacy} -> {actual}")
        with open(actual_path, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(legacy_path, 'w', encoding='utf-8') as fw:
            fw.write(content)

print("Scrape, Premium Generation, and Link Mapping completed successfully!")
