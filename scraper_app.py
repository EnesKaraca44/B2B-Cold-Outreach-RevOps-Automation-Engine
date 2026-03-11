import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import urljoin, urlparse
import time
from duckduckgo_search import DDGS

def find_companies_via_google(query, num_results=10):
    """
    Kullanıcının girdiği sektörel anahtar kelimeye göre arama yapar
    ve bulduğu web sitelerinin ana URL'lerini döndürür. (Anti-Ban DuckDuckGo)
    """
    print(f"\n🌐 Web'de Aranıyor: '{query}' ({num_results} sonuç)")
    found_urls = set()
    try:
        # DDGS ile arama yapıyoruz
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=num_results)
            
            for r in results:
                url = r.get('href', '')
                if not url:
                    continue
                    
                # Alt sayfa (ör: site.com/iletisim) yerine ana domain'i (site.com) alıyoruz
                parsed_uri = urlparse(url)
                base_url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
                
                # Gereksiz/sosyal medya sitelerini eleyelim
                if any(x in base_url for x in ['facebook.com', 'instagram.com', 'linkedin.com', 'twitter.com', 'youtube.com', 'gov.tr', 'edu.tr']):
                    continue
                    
                found_urls.add(base_url)
            
        print(f"✅ Web araması bitti, {len(found_urls)} adet potansiyel firma sitesi bulundu.")
        return list(found_urls)
    except Exception as e:
        print(f"❌ Arama Hatası: {e}")
        return []

def extract_emails_from_text(text):
    """Metin içerisindeki e-posta adreslerini Regex ile bulur."""
    # Basit bir e-posta regex'i
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    # Tekrarlayanları temizle ve listeye çevir
    return list(set(emails))

def scrape_website_for_contact_info(base_url):
    """Bir web sitesine girer ve Ana Sayfa ile İletişim sayfalarından e-posta adresi arar."""
    print(f"\n🔍 Taranıyor: {base_url}")
    found_emails = set()
    
    # Tarayıcı gibi görünmek için User-Agent ekliyoruz (bot olduğumuzu gizlemek için)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Tarayacağımız sayfalar (Önce ana sayfa, sonra varsa iletişim sayfası)
    pages_to_visit = [base_url]
    
    try:
        # Ana sayfaya istek at
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ana sayfadaki mailleri bul
        emails_on_home = extract_emails_from_text(soup.get_text())
        found_emails.update(emails_on_home)
        
        # "İletişim", "Contact" gibi linkleri bulup oraya da gidelim
        contact_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().lower()
            if 'iletisim' in href or 'contact' in href or 'iletisim' in text or 'contact' in text:
                # Göresel (relative) linkleri tam URL'ye çevir (/iletisim -> https://site.com/iletisim)
                full_url = urljoin(base_url, href)
                if full_url not in pages_to_visit:
                    contact_links.append(full_url)
        
        # Bulduğumuz ilk iletişim sayfasına da girelim
        if contact_links:
            contact_url = contact_links[0]
            print(f"   -> İletişim sayfası bulundu: {contact_url}")
            try:
                contact_resp = requests.get(contact_url, headers=headers, timeout=10)
                contact_soup = BeautifulSoup(contact_resp.text, 'html.parser')
                emails_on_contact = extract_emails_from_text(contact_soup.get_text())
                found_emails.update(emails_on_contact)
            except Exception as e:
                print(f"   -> İletişim sayfası okunamadı: {e}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Siteye erişilemedi ({base_url}): {e}")
        return []

    # İstenmeyen/sahte mailleri filtreleyelim (örneğin resim uzantılı olanları hatalı aldıysa)
    cleaned_emails = [e for e in found_emails if not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
    
    if cleaned_emails:
        print(f"   ✅ Bulunan E-Postalar: {', '.join(cleaned_emails)}")
    else:
        print("   ⚠️ E-Posta bulunamadı.")
        
    return cleaned_emails

def run_scraper(companies):
    """Şirketler listesini alıp sonuçları CSV'ye kaydeder."""
    results = []
    
    for company in companies:
        name = company.get("name")
        website = company.get("website")
        
        emails = scrape_website_for_contact_info(website)
        
        # Sonuçları listeye ekle
        results.append({
            "Şirket Adı": name,
            "Web Sitesi": website,
            "Bulunan E-Postalar": ", ".join(emails) if emails else "Bulunamadı"
        })
        
        # Siteleri yormamak ve engellenmemek için 2 saniye bekle
        time.sleep(2)
        
    # Pandas ile CSV'ye kaydet
    df = pd.DataFrame(results)
    output_file = "kazilmis_firmalar.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n🎉 İşlem Tamamlandı! Sonuçlar '{output_file}' dosyasına kaydedildi.")

if __name__ == "__main__":
    # Test etmek için örnek bir firma listesi (İleride bunları Google'dan otomatik çektirebiliriz)
    hedef_sirketler = [
        {"name": "Yemeksepeti", "website": "https://www.yemeksepeti.com"},
        {"name": "Getir", "website": "https://getir.com"},
        # Kendi web siteni veya bildiğin siteleri buraya ekleyebilirsin
        {"name": "Eksisozluk", "website": "https://eksisozluk.com"}
    ]
    
    print("--- 🕷️ WEB SCRAPING MOTORU BAŞLATILIYOR ---")
    run_scraper(hedef_sirketler)
