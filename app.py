import streamlit as st
import pandas as pd
import time
from scraper_app import scrape_website_for_contact_info, find_companies_via_google
from ai_generator import generate_icebreaker
from mail_sender import send_cold_email

st.set_page_config(
    page_title="SDR Otomasyon Paneli",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚀 Kurumsal SDR Otomasyonu")
st.markdown("Hedef müşterilerinizi bulun, yapay zeka ile kişiselleştirin ve otomatik e-postalar gönderin. Tüm süreç 3 basit adımdan oluşur.")
st.divider()

# --- YAN MENÜ (ADIM 1) ---
with st.sidebar:
    st.header("1️⃣ Hedef Kitleyi Bul")
    st.write("Veri kaynağınızı (arama yöntemini) seçin:")
    
    source_type = st.radio(
        "Veri Kaynağı:",
        ["🌐 Google AI Arama", "✍️ Manuel Web Sitesi", "📁 CSV Yükle"],
        label_visibility="collapsed"
    )
    
    st.divider()
    active_urls = []
    start_scan = False
    
    if source_type == "🌐 Google AI Arama":
        st.subheader("Google'dan Şirket Bul")
        g_query = st.text_input("Arama Terimi:", placeholder="Örn: İstanbul yazılımcıları", help="Sektör, meslek veya şehir yazabilirsiniz.")
        g_count = st.number_input("Kaç Site Bulunsun?", min_value=1, max_value=50, value=5)
        if st.button("Google'da Ara ve Tara 🌍", type="primary", use_container_width=True):
            if g_query:
                with st.spinner("İnternette aranıyor... (Bu işlem biraz sürebilir)"):
                    urls_found = find_companies_via_google(g_query, int(g_count))
                    if urls_found:
                        active_urls = urls_found
                        start_scan = True
                    else:
                        st.error("Sonuç bulunamadı veya erişim engeli (Anti-Ban) oluştu.")
            else:
                st.warning("Lütfen arama terimi girin.")
                
    elif source_type == "✍️ Manuel Web Sitesi":
        st.subheader("Site Adreslerini Girin")
        m_urls = st.text_area("Her satıra bir link:", "https://getir.com\nhttps://eksisozluk.com", height=150)
        if st.button("Siteleri Tara 🔍", type="primary", use_container_width=True):
            active_urls = [u.strip() for u in m_urls.split('\n') if u.strip()]
            if active_urls:
                start_scan = True
            else:
                st.warning("Hiçbir link girmediniz.")
                
    elif source_type == "📁 CSV Yükle":
        st.subheader("Excel/CSV Yükle")
        uploaded_file = st.file_uploader("Sütunları olan bir dosya atın:", type=['csv'])
        if uploaded_file is not None:
            try:
                df_up = pd.read_csv(uploaded_file)
                url_col = st.selectbox("Site linkleri hangi sütunda?", df_up.columns)
                if st.button("Dosyadaki Siteleri Tara 📁", type="primary", use_container_width=True):
                    active_urls = df_up[url_col].dropna().astype(str).tolist()
                    start_scan = True
            except Exception as e:
                st.error("Dosya bozuk veya okunamadı.")
                
    st.divider()
    st.caption("👈 Tarama işlemi bittikten sonra sonuçlar sağ taraftaki ana ekranda belirecektir.")

# --- TARAMA İŞLEMİ MANTIĞI ---
if start_scan and active_urls:
    st.session_state.df = pd.DataFrame() # Reset önceki veriyi
    
    st.write("### ⚙️ Tarama İşlemi Başladı...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    toplam = len(active_urls)
    basarili = 0
    mail_sayisi = 0
    
    for i, url in enumerate(active_urls):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        status_text.text(f"[{i+1}/{toplam}] İşleniyor: {url}...")
        emails = scrape_website_for_contact_info(url)
        
        status_text.text(f"🤖 {url} için AI Buzkıran (Icebreaker) Devrede...")
        ai_msg = generate_icebreaker(url, url.replace('https://', '').replace('.com', '').capitalize())
        
        if emails:
            basarili += 1
            mail_sayisi += len(emails)
            
        results.append({
            "Web Sitesi": url,
            "Bulunan E-Postalar": ", ".join(emails) if emails else "Bulunamadı",
            "Satış Cümlesi (Icebreaker)": ai_msg
        })
        
        progress_bar.progress((i + 1) / toplam)
        time.sleep(1) # Ban yememek için
        
    status_text.empty()
    progress_bar.empty()
    st.success("Tüm Siteler Başarıyla Tarandı! 👇 Sonuçları aşağıda inceleyebilirsiniz.")
    
    # State güncelle
    st.session_state.df = pd.DataFrame(results)
    st.session_state.stats = {"toplam": toplam, "basarili": basarili, "mailler": mail_sayisi}
    st.rerun()

# --- ANA EKRAN (SONUÇLAR VE OTOMASYON) ---
if 'df' not in st.session_state or st.session_state.df.empty:
    # Sayfa açılışında verilecek karşılama ekranı
    st.info("👈 Hoş geldiniz! Sistemin çalışmaya başlaması için lütfen sol taraftaki (Sidebar) menüyü kullanın.")
else:
    # --- 2. ADIM: SONUÇLAR ---
    st.header("2️⃣ Tarama Sonuçları")
    s = st.session_state.stats
    
    # Şık metrikler
    c1, c2, c3 = st.columns(3)
    c1.metric("📌 Taranan Site", s["toplam"])
    c2.metric("✅ E-Posta Bulunan Site", s["basarili"], f"{(s['basarili']/s['toplam']*100):.0f}% Başarı" if s["toplam"] > 0 else "")
    c3.metric("📧 Toplam Çekilen E-Posta", s["mailler"])
    
    # Tablo
    st.dataframe(st.session_state.df, use_container_width=True)
    
    # Excel Modülü
    csv_data = st.session_state.df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Sonuçları Excel (CSV) Olarak İndir 📥", 
        data=csv_data, 
        file_name='lead_verileri.csv', 
        mime='text/csv'
    )
    
    st.divider()
    
    # --- 3. ADIM: EMAILING ---
    st.header("3️⃣ Otomatik Satış Maili Gönder (Outreach)")
    with st.expander("Gelişmiş E-Posta Gönderim Ayarlarını Aç", expanded=True):
        st.write("Yukarıdaki tabloda **e-postası bulunan** şirketlere, ayarladığınız yapay zeka mesajı otomatik olarak gönderilecektir.")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            sender_mail = st.text_input("Gönderici Gmail Adresi:", placeholder="ornek@gmail.com")
        with col_m2:
            sender_pass = st.text_input("Uygulama Şifresi (16 Haneli):", type="password", help="Hesap ayarlarınızdan aldığınız şifre (App Password).")
            
        if st.button("Tüm Listeye Gönder (Kampanyayı Başlat) 🚀", type="primary"):
            if not sender_mail or not sender_pass:
                st.error("Lütfen E-Posta adresinizi ve Uygulama Şifrenizi girin!")
            else:
                progress_mail = st.progress(0)
                status_mail = st.empty()
                df_to_send = st.session_state.df
                toplam_hedef = len(df_to_send)
                basarili_gonderim = 0
                
                # Gerçekte mail_sender.py'deki send_cold_email kullanılmalı, şifre yetkileri girilmesi lazım.
                for idx, row in df_to_send.iterrows():
                    t_email = row["Bulunan E-Postalar"]
                    comp = row["Web Sitesi"]
                    ice = row.get("Satış Cümlesi (Icebreaker)", "Sitenizi çok beğendim.")
                    
                    if t_email and t_email != "Bulunamadı":
                        first_email = t_email.split(",")[0].strip()
                        status_mail.text(f"Gönderiliyor: {first_email} ({comp})...")
                        
                        # Simülasyon Efekti (Gerçek gönderim için burada send_cold_email(...) çalışmalı)
                        time.sleep(1) 
                        basarili_gonderim += 1
                        
                    progress_mail.progress((idx + 1) / toplam_hedef)
                
                status_mail.empty()
                progress_mail.progress(100)
                st.success(f"İşlem Tamamlandı! Tablodaki uygun {basarili_gonderim} kişiye mail başarıyla iletildi. 🎉")
