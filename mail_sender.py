import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time

# DİKKAT: Güvenlik için şifrelerinizi asla koda yazmayın, ortam değişkeni kullanın.
# Örn: EMAIL_PASSWORD = os.environ.get("SDR_EMAIL_PASSWORD")
SENDER_EMAIL = "sizin_mailiniz@gmail.com"
SENDER_PASSWORD = "mail_uygulama_sifreniz" # Gmail için App Password (Uygulama Şifresi) gerekir.

def send_cold_email(to_email, company_name, icebreaker_sentence):
    """
    Belirtilen e-posta adresine kişiselleştirilmiş bir soğuk satış (cold email) gönderir.
    """
    # 1. Aşama: E-Posta İçeriğini (Taslağını) Hazırlama
    subject = f"{company_name} için Dijital Büyüme Fırsatı"
    
    # E-posta gövdesi (HTML formatında daha profesyonel durur)
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <p>Merhaba,</p>
            <p>{icebreaker_sentence}</p>
            <p>Biz KDS Yazılım olarak, şirketlerin satış süreçlerini otomatize eden ve onlara nitelikli müşteri bulan sistemler kuruyoruz.</p>
            <p>Sizin operasyonunuza benzer firmalarda randevu sayılarını %40 oranında artırmayı başardık. Eğer sizin de yeni müşterilere ulaşma ve satış kanalınızı büyütme hedefiniz varsa, bu hafta 10 dakikalık kısa bir tanışma toplantısı ayarlayabilir miyiz?</p>
            <br>
            <p>İyi çalışmalar dilerim,</p>
            <p><b>Enes Karaca</b><br>
            Kurucu | KDS Yazılım<br>
            <i><a href="https://linkedin.com/in/enes" style="color: #2563EB;">LinkedIn Profilim</a></i></p>
        </body>
    </html>
    """
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    
    # 2. Aşama: SMTP Sunucusuna Bağlanma ve Gönderme
    print(f"📧 Mail hazırlanıyor: {to_email} ({company_name})")
    
    # Simülasyon Modu: Şifre girilmediyse gerçekten gönderme, sadece console'a yazdır.
    if SENDER_PASSWORD == "mail_uygulama_sifreniz":
        print(f"   ⚠️ SİMÜLASYON: Mail sunucusuna bağlanıldı (Şifre girilmediği için test modunda).")
        print(f"   ✅ Başarıyla GÖNDERİLDİ: {subject}")
        return True
        
    try:
        # Gmail SMTP Ayarları (Eğer Outlook vs. kullanılacaksa port ve host değişir)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Güvenli bağlantı (TLS) başlat
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, to_email, text)
        server.quit()
        
        print(f"   ✅ GERÇEK MAİL Başarıyla Gönderildi: {to_email}")
        return True
        
    except Exception as e:
        print(f"   ❌ Mail Gönderim Hatası: {e}")
        return False

def bulk_send_emails(leads_data):
    """
    Arayüzden (veya CSV'den) gelen adaylar listesindeki herkese sırayla mail atar.
    Spam'e düşmemek için aralarına bekleme süresi koyar.
    """
    print("\n--- 🚀 OTOMATİK MAİL MOTORU BAŞLATILIYOR ---")
    
    successful = 0
    for lead in leads_data:
        email = lead.get('E-Posta')
        company = lead.get('Şirket', 'Şirketiniz')
        icebreaker = lead.get('Icebreaker', 'Web sitenizi ve çalışmalarınızı inceledim, çok başarılı buldum.')
        
        if email and email != "Bulunamadı":
            success = send_cold_email(to_email=email, company_name=company, icebreaker_sentence=icebreaker)
            if success:
                successful += 1
                
            # SPAM KORUMASI: İki mail arası en az 5-10 saniye beklemek her zaman iyidir.
            print("   ⏳ Spam filtresine takılmamak için 5 saniye bekleniyor...")
            time.sleep(5) 
            
    print(f"\n🎉 İşlem Bitti: Toplam {successful} adet otomatik e-posta gönderildi.")

if __name__ == "__main__":
    # Test Verisi
    test_leads = [
        {"Şirket": "Örnek Yazılım A.Ş.", "E-Posta": "test_alici@example.com", "Icebreaker": "Örnek Yazılım olarak geliştirdiğiniz son mobil uygulamayı çok yenilikçi buldum."},
    ]
    bulk_send_emails(test_leads)
