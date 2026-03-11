import requests
import json
import os

# DİKKAT: Gerçek kullanımda API anahtarı os.environ.get("GEMINI_API_KEY") şeklinde alınmalıdır.
# Ücretsiz bir Google Gemini API key alıp buraya yapıştırabilirsiniz. (https://aistudio.google.com/app/apikey)
GEMINI_API_KEY = "BURA_KENDI_GEMINI_API_ANAHTARINIZ_GELECEK"

def generate_icebreaker(company_url, company_name="Firma"):
    """
    Google Gemini AI kullanarak belirtilen web sitesi için 
    satış e-postalarında kullanılacak özel bir giriş cümlesi (Icebreaker) üretir.
    """
    if GEMINI_API_KEY == "BURA_KENDI_GEMINI_API_ANAHTARINIZ_GELECEK":
        # API anahtarı yoksa test amaçlı sabit bir "mock" cümle döndür.
        return f"Merhaba {company_name} ekibi, {company_url} adresindeki yenilikçi vizyonunuz dikkatimi çekti."
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }

    # SDR Mantığı: Prompt (İstem) mühendisliği çok önemlidir.
    prompt = f"""
    Sen, B2B SaaS pazarında uzman bir Satış Geliştirme Temsilcisisin (SDR). 
    Görevin: '{company_url}' adresine sahip şirketin (Adı: {company_name}) yöneticisine soğuk bir satış e-postası (Cold Email) göndereceğiz.
    Bunun için bana sadece 1 CÜMLELİK, son derece samimi ve o şirketin sektörüyle/işiyle alakalı bir giriş cümlesi (Icebreaker) yaz.
    Standart, kurumsal 'Merhaba nasılsınız' gibi cümleler kurma.
    Doğrudan şirkete iltifat eden VEYA dijital dünyalarındaki bir detaya dokunan akıllıca bir cümle olsun.
    
    Örnek: "Eksisozluk.com'un Türkiye'nin hafızası olma konusundaki istikrarını yıllardır hayranlıkla takip ediyorum."
    Örnek: "Getir.com'un anında teslimat modeliyle perakende sektörüne getirdiği hızı görünce size ulaşmak istedim."
    
    Lütfen sadece cümleyi yaz. Tırnak işaretleri, açıklama veya devam cümlesi ekleme.
    """

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        # Gemini'nin yanıt JSON yapısından metni çıkar
        if "candidates" in result and len(result["candidates"]) > 0:
            icebreaker = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            # Başta/sonda gereksiz tırnak varsa temizle
            icebreaker = icebreaker.strip('"\'')
            return icebreaker
        else:
            return f"Merhaba {company_name} ekibi, {company_url} sitenizi çok beğendim."
            
    except Exception as e:
        print(f"Yapay Zeka Hatası: {e}")
        return f"Merhaba {company_name} ekibi, iyi çalışmalar dilerim."

if __name__ == "__main__":
    # Tek başına dosyayı test etmek için
    print("--- 🤖 YAPAY ZEKA ICEBREAKER TESTİ ---")
    test_url = "https://eksisozluk.com"
    test_isim = "Ekşisözlük"
    print(f"Hedef: {test_url}")
    print(f"Üretilen Buzkıran:\n'{generate_icebreaker(test_url, test_isim)}'")
