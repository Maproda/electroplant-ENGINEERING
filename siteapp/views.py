from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, JsonResponse, HttpResponseNotFound
import io, csv, os
from datetime import datetime

SITE = {
    'name': 'electroplant ENGINEERING',
    'tagline': 'Engineering real-world electrical solutions',
    'logo_text': 'electroplant',
    'email': 'hello@electroplant.example',
    'phone': '+1 (555) 123-4567',
    'address_lines': ['1234 Energy Way', 'Suite 100', 'San Francisco, CA 94107']
}

SERVICES = [
    {'id':'power','title':'Power Systems','summary':'Design of power distribution and substations','icon':'⚡'},
]

BLOG = [
    {'slug':'reliable-power','title':'Designing Reliable Power Systems','date':'2025-03-10','excerpt':'Key strategies for resilient power.'},
]

CONTACT_CSV = 'messages.csv'

def home(request):
    return render(request, 'home.html', {'site': SITE, 'services': SERVICES, 'projects': [], 'blog': BLOG})

def about(request):
    return render(request, 'about.html', {'site': SITE, 'team': []})

def services(request):
    return render(request, 'services.html', {'site': SITE, 'services': SERVICES})

def projects(request):
    return render(request, 'projects.html', {'site': SITE, 'projects': []})

def blog_index(request):
    return render(request, 'blog_index.html', {'site': SITE, 'blog': BLOG})

def blog_post(request, slug):
    post = next((b for b in BLOG if b['slug']==slug), None)
    if not post:
        return HttpResponseNotFound('Post not found')
    return render(request, 'blog_post.html', {'site': SITE, 'post': post})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        company = request.POST.get('company','')
        message = request.POST.get('message')
        if not name or not email or not message:
            return redirect('contact')
        save_message({'timestamp': datetime.utcnow().isoformat(), 'name': name, 'email': email, 'company': company, 'message': message})
        return redirect('contact')
    return render(request, 'contact.html', {'site': SITE})

def save_message(row):
    file_exists = os.path.exists(CONTACT_CSV)
    with open(CONTACT_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp','name','email','company','message'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def download_brochure(request):
    content = SITE['name'] + ' - Brochure\n' + SITE['tagline'] + '\n'
    buf = io.BytesIO(content.encode('utf-8'))
    return FileResponse(buf, as_attachment=True, filename='brochure.txt')

def sitemap(request):
    base = request.build_absolute_uri('/')[:-1]
    xml = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    for u in ['/', '/services', '/projects', '/about', '/blog', '/contact']:
        xml += f"<url><loc>{base}{u}</loc></url>"
    xml += '</urlset>'
    return HttpResponse(xml, content_type='application/xml')

def robots(request):
    txt = f"User-agent: *\nDisallow:\nSitemap: {request.build_absolute_uri('/sitemap.xml')}\n"
    return HttpResponse(txt, content_type='text/plain')

def health(request):
    return JsonResponse({'status':'ok','time':datetime.utcnow().isoformat()})
