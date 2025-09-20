import streamlit as st
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.corpus import cmudict
import nltk


st.set_page_config(layout="wide")  # Atau "centered"
# Download required NLTK data
try:
    nltk.download('stopwords')
except:
    pass
# Download required NLTK data
try:
    nltk.download('cmudict')
except:
    pass

# Daftar kata dengan tingkat suku kata sedang
DAFTAR_KATA_SUKU_KATA_SEDANG = [
    'matahari', 'membangunkanku', 'seragam', 'sekolah', 'gerbang',
    'guru', 'teman', 'kelas', 'bangku', 'jendela', 'bernayanyi',
    'istirahat', 'taman', 'berkenalan', 'masuk', 'belajar',
    'menulis', 'huruf', 'senang', 'pertama', 'esok'
]

# Daftar kata dasar bahasa Indonesia (contoh singkat)
DAFTAR_KATA_DASAR = [
    'pagi', 'ini', 'matahari', 'bersinar', 'cerah',
    'ibu', 'membangunkan', 'dengan', 'senyum',
    'segera', 'mandi', 'memakai', 'seragam', 'baru',
    'ayah', 'mengantar', 'ke', 'sekolah',
    'di', 'gerbang', 'bu', 'guru', 'menyambut',
    'aku', 'melihat', 'banyak', 'teman', 'baru',
    'di', 'kelas', 'duduk', 'di', 'bangku', 'dekat', 'jendela',
    'bu', 'guru', 'memperkenalkan', 'diri',
    'kami', 'bernyanyi', 'bersama',
    'saat', 'istirahat', 'bermain', 'di', 'taman', 'sekolah',
    'aku', 'berkenalan', 'dengan', 'rina',
    'bel', 'masuk', 'berbunyi',
    'kami', 'belajar', 'menulis', 'huruf', 'a', 'dan', 'b',
    'aku', 'senang', 'karena', 'bisa', 'menulis', 'rapi',
    'hari', 'pertama', 'di', 'sekolah', 'terasa', 'menyenangkan',
    'aku', 'tak', 'sabar', 'menunggu', 'hari', 'esok'
]
if "kondisi" not in st.session_state:
    st.session_state.kondisi={'kondisi1':True,'kondisi2':False,'kondisi3':False, 'kondisi4':False}

#========CSS=====
koding_css="""
    <style>
    .tulisan1, .tulisan2{
        color:black;
        background-color:yellow;
        font-family:'Times New Roman';
        font-size:20px;
        padding:5px;
        border-radius:10px;
        border:2px solid black;
        margin:10px;
        box-shadow: 2px 2px 2px 4px green;
    }
    .tulisan2{
        background-color:cyan;
    }
    .tulisan3{
        font-family:"comic sans ms";
        font-size:18px;
        padding:5px;
        margin:5px;
        border:2px solid black;
        color:black;
        background-color:pink;
        
    }
    ol{
        font-family:'Times New Roman';
        font-size:16px;
    }
    </style>
"""
st.markdown(koding_css,unsafe_allow_html=True)

#=========Kumpulan Fungsi=======

def count_sentences(text):
    """Menghitung jumlah kalimat dalam teks"""
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def analyze_story(story_text):
    """Menganalisis cerita berdasarkan jumlah kalimat"""
    sentence_count = count_sentences(story_text)
    
    if sentence_count >= 15:
        result = f"✅ **Evaluasi:**\n\nDengan {sentence_count} kalimat, cerita Anda memiliki detail yang cukup untuk memperjelas ide. Setiap kalimat memberikan informasi spesifik dan membangun narasi yang komprehensif."
        st.success(result)
    elif sentence_count >= 10:
        result = f"⚠️ **Evaluasi:**\n\nCerita Anda memiliki {sentence_count} kalimat. Meskipun cukup jelas, Anda bisa menambahkan beberapa detail untuk membuat cerita lebih kaya dan memperjelas ide."
        st.warning(result)
    else:
        result = f"❗ **Evaluasi:**\n\nDengan hanya {sentence_count} kalimat, cerita Anda masih kurang detail. Disarankan untuk menambahkan deskripsi, dialog, atau pengembangan karakter untuk memperjelas ide."
        st.error(result)
    
    return sentence_count


def hitung_kompleksitas_kalimat(teks):
    """Hitung kompleksitas kalimat berdasarkan panjang dan struktur"""
    kalimat = re.split(r'[.!?]+', teks)
    hasil = []
    
    for i, k in enumerate(kalimat):
        if not k.strip():
            continue
            
        # Hitung jumlah kata
        kata = k.split()
        jumlah_kata = len(kata)
        
        # Analisis struktur kalimat
        kata_unik = len(set(kata))
        rasio_kata_unik = kata_unik / jumlah_kata if jumlah_kata > 0 else 0
        
        # Deteksi kata familiar
        kata_familiar = [kata.lower() for kata in kata if kata.lower() in DAFTAR_KATA_DASAR]
        persentase_familiar = len(kata_familiar) / jumlah_kata * 100 if jumlah_kata > 0 else 0
        
        hasil.append({
            'kalimat': k,
            'nomor': i+1,
            'jumlah_kata': jumlah_kata,
            'persentase_familiar': persentase_familiar,
            'kompleksitas': 'Sederhana' if jumlah_kata <= 8 and rasio_kata_unik <= 0.5 else 'Menengah' if jumlah_kata <= 12 else 'Kompleks'
        })
    
    return hasil

def analisis_teks(teks_asli, teks_user):
    """Analisis perbedaan antara teks asli dan teks user"""
    hasil_analisis = []
    
    # Pisahkan kedua teks menjadi kalimat
    kalimat_asli = re.split(r'[.!?]+', teks_asli)
    kalimat_user = re.split(r'[.!?]+', teks_user)
    
    # Bandingkan kalimat
    for i in range(min(len(kalimat_asli), len(kalimat_user))):
        kalimat_a = kalimat_asli[i].strip().lower()
        kalimat_u = kalimat_user[i].strip().lower()
        
        # Hitung kesamaan kata
        kata_asli = set(re.findall(r'\w+', kalimat_a))
        kata_user = set(re.findall(r'\w+', kalimat_u))
        
        kata_sama = kata_asli.intersection(kata_user)
        persentase_kecocokan = len(kata_sama) / len(kata_asli) * 100 if len(kata_asli) > 0 else 0
        
        hasil_analisis.append({
            'kalimat_asli': kalimat_asli,
            'kalimat_user': kalimat_u,
            'persentase_kecocokan': persentase_kecocokan,
            'status': 'Sesuai' if persentase_kecocokan >= 70 else ' Hampir Sesuai' if persentase_kecocokan >= 50 else 'Perlu Diperbaiki'
        })
    
    return hasil_analisis

def hitung_suku_kata(teks):
    """Hitung jumlah suku kata dalam teks"""
    # Daftar vokal dalam bahasa Indonesia
    vokal = 'aeiouAIUEO'
    
    def hitung_suku_kata_kata(kata):
        # Hitung suku kata berdasarkan jumlah vokal
        suku_kata = 0
        for char in kata:
            if char in vokal:
                suku_kata += 1
        return suku_kata
    
    kata = re.findall(r'\w+', teks)
    hasil = []
    
    for i, k in enumerate(kata):
        jumlah_suku_kata = hitung_suku_kata_kata(k)
        hasil.append({
            'kata': k,
            'nomor': i+1,
            'jumlah_suku_kata': jumlah_suku_kata,
            'kategori': 'Sedang' if jumlah_suku_kata <= 3 else 'Tinggi' if jumlah_suku_kata <= 5 else 'Sangat Tinggi'
        })
    
    return hasil

def analisis_suku_kata(teks):
    """Analisis distribusi suku kata dalam teks"""
    hasil_analisis = []
    kata_dengan_suku_kata = hitung_suku_kata(teks)
    
    # Hitung statistik
    total_kata = len(kata_dengan_suku_kata)
    kata_1_suku_kata = sum(1 for k in kata_dengan_suku_kata if k['jumlah_suku_kata'] == 1)
    kata_2_suku_kata = sum(1 for k in kata_dengan_suku_kata if k['jumlah_suku_kata'] == 2)
    kata_3_suku_kata = sum(1 for k in kata_dengan_suku_kata if k['jumlah_suku_kata'] == 3)
    kata_lebih_3_suku_kata = sum(1 for k in kata_dengan_suku_kata if k['jumlah_suku_kata'] > 3)
    
    # Hitung persentase
    persentase_1 = (kata_1_suku_kata / total_kata) * 100
    persentase_2 = (kata_2_suku_kata / total_kata) * 100
    persentase_3 = (kata_3_suku_kata / total_kata) * 100
    persentase_lebih_3 = (kata_lebih_3_suku_kata / total_kata) * 100
    
    hasil_analisis.append({
        'total_kata': total_kata,
        'persentase_1_suku_kata': persentase_1,
        'persentase_2_suku_kata': persentase_2,
        'persentase_3_suku_kata': persentase_3,
        'persentase_lebih_3_suku_kata': persentase_lebih_3,
        'kesimpulan': (
            "Teks ini memiliki distribusi suku kata yang ideal untuk anak yang sudah mulai lancar membaca. "
            "Mayoritas kata memiliki 1-3 suku kata, dengan sedikit variasi kata yang lebih kompleks."
        )
    })
    
    return hasil_analisis

def uji_pemahaman_suku_kata(teks_asli, teks_user):
    """Uji pemahaman suku kata dengan teks alternatif"""
    hasil_test = []
    
    # Pisahkan teks menjadi kata
    kata_asli = re.findall(r'\w+', teks_asli)
    kata_user = re.findall(r'\w+', teks_user)
    
    # Bandingkan kata-kata
    for i in range(min(len(kata_asli), len(kata_user))):
        kata_a = kata_asli[i].lower()
        kata_u = kata_user[i].lower()
        
        # Hitung suku kata
        suku_kata_asli = sum(1 for char in kata_a if char in 'aeiouAIUEO')
        suku_kata_user = sum(1 for char in kata_u if char in 'aeiouAIUEO')
        
        # Tentukan tingkat kesulitan
        tingkat_kesulitan = abs(suku_kata_asli - suku_kata_user)
        
        hasil_test.append({
            'kata_asli': kata_a,
            'kata_user': kata_u,
            'suku_kata_asli': suku_kata_asli,
            'suku_kata_user': suku_kata_user,
            'tingkat_kesulitan': tingkat_kesulitan,
            'status': 'Sesuai' if tingkat_kesulitan <= 1 else 'Hampir Sesuai' if tingkat_kesulitan <= 2 else 'Perlu Diperbaiki'
        })
    
    return hasil_test


#=================Batasan===================
#=============Tampilan==================
def tampilan1():
    st.markdown("""
                <iframe src=https://martin123-oke.github.io/sekolahku/sekolahku.html style="width:100%; height:500px"></iframe>"""
                ,unsafe_allow_html=True)
def tampilan2():
    st.title("📝 Tes Frasa: Jumlah Kalimat Cukup Banyak")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='tulisan1'>Cara Penggunaan:</div>",unsafe_allow_html=True)
        st.markdown("""<div class='tulisan2'>
        Masukkan teks cerita Anda ke dalam kotak di bawah, 
        kemudian klik tombol "Analisis Cerita" untuk melihat 
        evaluasi berdasarkan jumlah kalimat.</div>
        """, unsafe_allow_html=True)
        
        story_text = st.text_area(
            "Masukkan cerita Anda:",
            value=""
            ,
            height=300
        )
        
        if st.button("Analisis Cerita", key="analyze_btn"):
            if story_text.strip():
                sentence_count = analyze_story(story_text)
                st.info(f"Total kalimat yang terdeteksi: {sentence_count}")
            else:
                st.error("Silakan masukkan teks cerita terlebih dahulu!")
    
    with col2:
        st.markdown("<div class='tulisan3'>Tips Penulisan:</div>", unsafe_allow_html=True)
        st.markdown("""<ol>
        <li> ≥ 15 kalimat: Ide jelas dan detail</li>
        <li> 10-14 kalimat: Cukup jelas, bisa ditambah detail </li>
        <li> < 10 kalimat: Kurang detail, perlu pengembangan </li>
        </ol>
        <div class='tulisan3'>Strategi Memperkaya Cerita:</div>
        <ol>
        <li>Tambahkan deskripsi sensoris (penglihatan, pendengaran)</li>
        <li>Sertakan dialog antar karakter</li>
        <li>Gunakan metafora atau perbandingan</li>
        <li>Perluas latar belakang karakter<li>
        </ol>
        """, unsafe_allow_html=True)
def tampilan3():
    st.title("📚 Tes Fry: Struktur Kalimat Sederhana dan Kata Familiar")

    # Konten cerita
    cerita_asli = """
Pagi ini, matahari bersinar cerah.
Ibu membangunkanku dengan senyum.
Aku segera mandi dan memakai seragam baru.
Ayah mengantarku ke sekolah.
Di gerbang, Bu Guru menyambutku.
Aku melihat banyak teman baru.
Di kelas, aku duduk di bangku dekat jendela.
Bu Guru memperkenalkan diri.
Kami bernyanyi bersama.
Saat istirahat, aku bermain di taman sekolah.
Aku berkenalan dengan Rina. 
Bel masuk berbunyi.
Kami belajar menulis huruf A dan B.
Aku senang karena bisa menulis rapi.
Hari pertamaku di sekolah terasa menyenangkan.
Aku tak sabar menunggu hari esok.
"""

        # Kolom utama
    col1, col2 = st.columns(2)

    with col1:
        st.header("Cerita Asli")
        st.write(cerita_asli)
    
        st.subheader("Analisis Struktur Kalimat")
        hasil_analisis = hitung_kompleksitas_kalimat(cerita_asli)
    
        for item in hasil_analisis:
            st.markdown(f"**Kalimat {item['nomor']}**")
            st.write(item['kalimat'])
            st.progress(int(item['persentase_familiar'] / 100 * 100))
            st.caption(f"Persentase kata familiar: {item['persentase_familiar']:.1f}% | Kompleksitas: {item['kompleksitas']}")

    with col2:
        st.header("Tes Kemampuan Membaca")
        st.write("Salin teks di bawah dan tulis ulang dengan benar:")
    
        teks_user = st.text_area("Tulis ulang cerita:", height=300, placeholder="Tulis cerita di sini...")
    
        if st.button("Analisis"):
            if teks_user.strip():
                st.subheader("Hasil Analisis")
                hasil_perbandingan = analisis_teks(cerita_asli, teks_user)
            
                for item in hasil_perbandingan:
                    #st.markdown(f"**Kalimat {item['kalimat_asli'].split()[0]}**")
                    st.write(f"Asli: {item['kalimat_asli']}")
                    st.write(f"Anda: {item['kalimat_user']}")
                    st.progress(int(item['persentase_kecocokan'] / 100 * 100))
                    st.caption(f"Status: {item['status']} ({item['persentase_kecocokan']:.1f}% kesamaan)")
            else:
                st.warning("Mohon tulis teks terlebih dahulu!")

    # Informasi tambahan
    st.sidebar.header("Petunjuk Penggunaan")
    st.sidebar.write("""
    1. Salin teks cerita asli di kolom kiri
    2. Tulis ulang teks tersebut di kolom kanan
    3. Klik tombol "Analisis" untuk mendapatkan hasil
    4. Hasil akan menunjukkan persentase kata familiar dan kesesuaian kalimat
    """)

    st.sidebar.header("Skor Keseluruhan")
    skor = sum([item['persentase_familiar'] for item in hasil_analisis]) / len(hasil_analisis)
    st.sidebar.metric("Skor Keseluruhan", f"{skor:.1f}/100")

    if skor >= 80:
        st.sidebar.success("Luar biasa! Struktur kalimat sangat sederhana dan familiar.")
    elif skor >= 60:
        st.sidebar.warning("Bagus! Struktur kalimat cukup sederhana dan familiar.")
    else:
        st.sidebar.error("Perlu latihan lebih! Cobalah menggunakan kata-kata yang lebih umum.")

    st.divider()
    st.caption("Tes ini mengukur kemampuan membaca berdasarkan struktur kalimat sederhana dan penggunaan kata-kata familiar.")

def tampilan4():
    st.title("📖 Tes Fry: Tingkat Suku Kata Sedang")

    # Konten cerita
    cerita_asli = """
Pagi ini, matahari bersinar cerah.
Ibu membangunkanku dengan senyum.
Aku segera mandi dan memakai seragam baru.
Ayah mengantarku ke sekolah.
Di gerbang, Bu Guru menyambutku.
Aku melihat banyak teman baru.
Di kelas, aku duduk di bangku dekat jendela.
Bu Guru memperkenalkan diri.
Kami bernyanyi bersama.
Saat istirahat, aku bermain di taman sekolah.
Aku berkenalan dengan Rina. 
Bel masuk berbunyi.
Kami belajar menulis huruf A dan B.
Aku senang karena bisa menulis rapi.
Hari pertamaku di sekolah terasa menyenangkan.
Aku tak sabar menunggu hari esok.
"""

    # Kolom utama
    col1, col2 = st.columns(2)

    with col1:
        st.header("Cerita Asli")
        st.write(cerita_asli)
    
        st.subheader("Analisis Distribusi Suku Kata")
        hasil_analisis = analisis_suku_kata(cerita_asli)
    
        for item in hasil_analisis:
            st.markdown(f"**Statistik Suku Kata**")
            st.progress(int(item['persentase_1_suku_kata']))
            st.caption(f"Suku kata 1: {item['persentase_1_suku_kata']:.1f}%")
        
            st.progress(int(item['persentase_2_suku_kata']))
            st.caption(f"Suku kata 2: {item['persentase_2_suku_kata']:.1f}%")
        
            st.progress(int(item['persentase_3_suku_kata']))
            st.caption(f"Suku kata 3: {item['persentase_3_suku_kata']:.1f}%")
        
            st.progress(int(item['persentase_lebih_3_suku_kata']))
            st.caption(f"Suku kata 3+: {item['persentase_lebih_3_suku_kata']:.1f}%")
        
            st.success(item['kesimpulan'])

    with col2:
        st.header("Uji Pemahaman Suku Kata")
        st.write("Salin teks di bawah dan tulis ulang dengan benar:")
    
        teks_user = st.text_area("Tulis ulang cerita:", height=300, placeholder="Tulis cerita di sini...")
    
        if st.button("Analisis"):
            if teks_user.strip():
                st.subheader("Hasil Uji Pemahaman")
                hasil_test = uji_pemahaman_suku_kata(cerita_asli, teks_user)
            
                for item in hasil_test:
                    st.markdown(f"**Kata {item['kata_asli']} vs {item['kata_user']}**")
                    st.write(f"Asli: {item['kata_asli']} ({item['suku_kata_asli']} suku kata)")
                    st.write(f"Anda: {item['kata_user']} ({item['suku_kata_user']} suku kata)")
                    st.progress(int((1 - item['tingkat_kesulitan']/5) * 100))
                    st.caption(f"Status: {item['status']} (Perbedaan: {item['tingkat_kesulitan']} suku kata)")
            else:
                st.warning("Mohon tulis teks terlebih dahulu!")

    # Informasi tambahan
    st.sidebar.header("Petunjuk Penggunaan")
    st.sidebar.write("""
1. Perhatikan distribusi suku kata dalam teks asli
2. Ketika menulis ulang, coba gunakan kata-kata dengan jumlah suku kata yang mirip
3. Perbedaan 1-2 suku kata masih normal untuk anak yang mulai lancar membaca
4. Hasil akan menunjukkan tingkat kesulitan setiap kata
""")

    st.sidebar.header("Rekomendasi Latihan")
    st.sidebar.write("""
- **Latihan 1**: Fokus pada kata-kata dengan 2-3 suku kata seperti 'matahari', 'seragam'
- **Latihan 2**: Coba ubah kata sederhana menjadi versi dengan lebih banyak suku kata
- **Contoh**: 'ibu' → 'ibu-bapa', 'hari' → 'harimau'
""")

    st.divider()
    st.caption("Tes ini membantu mengidentifikasi tingkat kesulitan suku kata dan memberikan panduan untuk meningkatkan keterampilan membaca.")


#=================================
if st.session_state.kondisi['kondisi1']:
    tampilan1()
if st.session_state.kondisi['kondisi2']:
    tampilan2()
if st.session_state.kondisi['kondisi3']:
    tampilan3()
if st.session_state.kondisi['kondisi4']:
    tampilan4()

#=====================================
if st.sidebar.button("Awal"):
    st.session_state.kondisi={'kondisi1':True,'kondisi2':False,'kondisi3':False, 'kondisi4':False}
    st.rerun()
with st.sidebar.expander("Baca dan dengarkan"):
    st.markdown("""
                <iframe src=https://martin123-oke.github.io/sekolahku/kegiatanku.html style="width:100%; height:500px"></iframe>"""
                ,unsafe_allow_html=True)
if st.sidebar.button("Jumlah kalimat "):
    st.session_state.kondisi={'kondisi1':False,'kondisi2':True,'kondisi3':False,'kondisi4':False}
    st.rerun()
if st.sidebar.button("Struktur Kalimat "):
    st.session_state.kondisi={'kondisi1':False,'kondisi2':False,'kondisi3':True,'kondisi4':False}
    st.rerun()
if st.sidebar.button("Tingkat Suku Kata "):
    st.session_state.kondisi={'kondisi1':False,'kondisi2':False,'kondisi3':False,'kondisi4':True}
    st.rerun()
