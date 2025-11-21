import streamlit as st
import pandas as pd
import random
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
import json

# Konfigurasi halaman
st.set_page_config(
    page_title="MRI Survey System",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🧠"
)

# CSS untuk styling yang lebih menarik
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .mode-card {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .mode-card:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.5);
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    .mode-card.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: white;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    .mode-card h3 {
        margin: 10px 0 5px 0;
        font-size: 20px;
        font-weight: 700;
    }
    
    .mode-card p {
        margin: 5px 0 0 0;
        font-size: 13px;
        opacity: 0.9;
    }
    
    .mode-icon {
        font-size: 48px;
        margin-bottom: 10px;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 12px;
        border: none;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    .question-box {
        background: white;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid #f0f2f6;
        transition: all 0.3s ease;
    }
    
    .question-box:hover {
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    .progress-text {
        font-size: 20px;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 10px 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card h2 {
        margin: 0;
        font-size: 48px;
        font-weight: 700;
    }
    
    .metric-card p {
        margin: 10px 0 0 0;
        font-size: 16px;
        opacity: 0.9;
    }
    
    .user-info-box {
        background: linear-gradient(135deg, #e8f4f8 0%, #d4e9f7 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #2196F3;
        margin-bottom: 30px;
        box-shadow: 0 5px 15px rgba(33, 150, 243, 0.2);
    }
    
    .user-info-box h3 {
        color: #2196F3;
        margin-top: 0;
        font-weight: 700;
    }
    
    .aspect-card {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .aspect-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
    }
    
    .stCheckbox {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 2px solid #f0f2f6;
        transition: all 0.3s ease;
    }
    
    .stCheckbox:hover {
        border-color: #667eea;
        background: #f8f9ff;
    }
    
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    .stAlert {
        border-radius: 12px;
        border-left-width: 6px;
    }
    
    .legend-button {
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .legend-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.3);
    }
    
    .sidebar-info {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid rgba(255, 255, 255, 0.5);
        margin: 15px 0;
        backdrop-filter: blur(10px);
    }
    
    .sidebar-info ul {
        margin: 10px 0;
        padding-left: 20px;
    }
    
    .sidebar-info li {
        margin: 8px 0;
        font-size: 13px;
    }
    
    .welcome-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .welcome-banner h1 {
        color: white !important;
        -webkit-text-fill-color: white;
        margin-bottom: 10px;
    }
    
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    [data-testid="stSidebar"] .stRadio {
        display: none;
    }
    
    .behavior-type-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        margin-left: 10px;
    }
    
    .badge-strong {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
    }
    
    .badge-weak {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Warna untuk setiap dimensi
DIMENSION_COLORS = {
    'Motivation': '#FF6B6B',
    'Relation': '#4CAF50',
    'Impact': '#45B7D1'
}

# Password admin
ADMIN_PASSWORD = "admin123"

# Path untuk file hasil
RESULTS_FILE = "survey_results.csv"
BIODATA_FILE = "assets/data/biodata.csv"

# Daftar Satker di Provinsi Lampung
SATKER_LAMPUNG = [
    "BPS Provinsi Lampung",
    "BPS Kabupaten Lampung Barat",
    "BPS Kabupaten Lampung Selatan",
    "BPS Kabupaten Lampung Tengah",
    "BPS Kabupaten Lampung Timur",
    "BPS Kabupaten Lampung Utara",
    "BPS Kabupaten Mesuji",
    "BPS Kabupaten Pesawaran",
    "BPS Kabupaten Pesisir Barat",
    "BPS Kabupaten Pringsewu",
    "BPS Kabupaten Tanggamus",
    "BPS Kabupaten Tulang Bawang",
    "BPS Kabupaten Tulang Bawang Barat",
    "BPS Kabupaten Way Kanan",
    "BPS Kota Bandar Lampung",
    "BPS Kota Metro"
]

# ==================== FUNGSI UTILITY ====================

@st.cache_data
def load_biodata():
    """Load data biodata pegawai dari CSV"""
    try:
        df = pd.read_csv(BIODATA_FILE)
        df.columns = df.columns.str.strip()
        # Pastikan kolom username ada dan lowercase untuk case-insensitive comparison
        if 'username' in df.columns:
            df['username'] = df['username'].str.strip().str.lower()
        # Pastikan NIP dalam format string
        if 'nip' in df.columns:
            df['nip'] = df['nip'].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading biodata: {e}")
        # Data sample untuk fallback (tanpa satker)
        data = """username,nama,nip
thomson,Thomson,200104052024121001
john,John Doe,199001012020121001
jane,Jane Smith,199502022021011002"""
        
        from io import StringIO
        df = pd.read_csv(StringIO(data))
        df['username'] = df['username'].str.strip().str.lower()
        df['nip'] = df['nip'].astype(str).str.strip()
        return df

def check_username_exists(username):
    """Cek apakah username terdaftar di biodata"""
    df_biodata = load_biodata()
    username_lower = username.strip().lower()
    return username_lower in df_biodata['username'].values

def check_username_taken(username):
    """Cek apakah username sudah pernah mengerjakan survey"""
    df_results = load_results()
    if df_results.empty:
        return False
    username_lower = username.strip().lower()
    # Case-insensitive comparison
    df_results['username_bps_lower'] = df_results['username_bps'].str.strip().str.lower()
    return username_lower in df_results['username_bps_lower'].values

def get_user_info(username):
    """Ambil informasi user dari biodata berdasarkan username"""
    df_biodata = load_biodata()
    username_lower = username.strip().lower()
    user_data = df_biodata[df_biodata['username'] == username_lower]
    if not user_data.empty:
        user_info = {
            'username': user_data.iloc[0]['username'],
            'nama': user_data.iloc[0]['nama'],
            'nip': str(user_data.iloc[0]['nip'])
        }
        return user_info
    return None

def validate_nip(username, nip_input):
    """Validasi apakah NIP sesuai dengan username di biodata"""
    user_info = get_user_info(username)
    if user_info:
        return user_info['nip'] == str(nip_input).strip()
    return False

@st.cache_data
def load_data():
    """Load data dari CSV atau gunakan data hardcoded sebagai fallback"""
    try:
        df = pd.read_csv('assets/data/data_mri.csv')
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Data sample dengan Perilaku Kuat dan Perilaku Lemah
        data = """Dimensi,Aspek,Arti,Perilaku Kuat,Perilaku Lemah
Motivation,Aversive,Memiliki pemikiran terdorong untuk berhati-hati dan mampu memitigasi risiko.,Mereka waspada terutama terhadap niat buruk seseorang.,Kurang waspada terhadap potensi risiko dari orang lain.
Motivation,Aversive,Memiliki pemikiran terdorong untuk berhati-hati dan mampu memitigasi risiko.,Mampu mengidentifikasi masalah atau resiko sebelum terjadi.,Sering terlambat menyadari masalah yang akan muncul.
Motivation,Aversive,Memiliki pemikiran terdorong untuk berhati-hati dan mampu memitigasi risiko.,Berpegang pada aturan dan prosedur.,Cenderung fleksibel mengabaikan aturan.
Motivation,Aversive,Memiliki pemikiran terdorong untuk berhati-hati dan mampu memitigasi risiko.,Memperhitungkan setiap risiko dan dampak yang mungkin ditimbulkannya.,Kurang mempertimbangkan risiko dalam keputusan.
Motivation,Collector,Ingin mengetahui lebih banyak baik tentang hal-hal yang menarik atau sebuah informasi,Mencari tahu lebih banyak dan memperbarui informasi.,Puas dengan informasi yang sudah dimiliki.
Motivation,Collector,Ingin mengetahui lebih banyak baik tentang hal-hal yang menarik atau sebuah informasi,Mengumpulkan hal-hal yang menurut mereka menarik karena mereka yakin dapat menggunakannya di kemudian hari.,Tidak tertarik mengumpulkan informasi tambahan.
Motivation,Competitive,Memiliki keinginan kuat untuk bersaing dan menang.,Selalu berusaha menjadi yang terbaik,Tidak terlalu peduli dengan kompetisi.
Motivation,Competitive,Memiliki keinginan kuat untuk bersaing dan menang.,Menikmati pertandingan,Menghindari situasi kompetitif.
Motivation,Directive,Memiliki kecenderungan untuk memimpin mengarahkan dan mengambil kendali.,Secara alami mengambil peran pemimpin dalam kelompok,Lebih nyaman mengikuti arahan orang lain.
Motivation,Directive,Memiliki kecenderungan untuk memimpin mengarahkan dan mengambil kendali.,Memberikan instruksi jelas,Jarang memberikan arahan kepada orang lain.
Relation,Advisor,Berantusias besar untuk berbagi masukan atau nasihat yang bisa membantu orang tersebut mengatasi masalahnya,Secara spontan memberi nasihat dalam berbagai situasi.,Menunggu diminta sebelum memberi nasihat.
Relation,Advisor,Berantusias besar untuk berbagi masukan atau nasihat yang bisa membantu orang tersebut mengatasi masalahnya,Mengesampingkan diri untuk membantu orang lain menghadapi rintangannya.,Fokus pada masalah sendiri terlebih dahulu.
Relation,Affectionate,Menunjukkan kasih sayang kehangatan dan kepedulian secara terbuka.,Sering memberikan pujian,Jarang mengekspresikan pujian.
Relation,Affectionate,Menunjukkan kasih sayang kehangatan dan kepedulian secara terbuka.,Sentuhan fisik seperti pelukan,Menjaga jarak fisik dengan orang lain.
Relation,Caring,Sangat peka terhadap keinginan dan kebutuhan orang lain yang mungkin tidak terekspresikan,Terhubung secara mendalam dengan kondisi emosi diri dan orang lain.,Sulit membaca emosi orang lain.
Relation,Caring,Sangat peka terhadap keinginan dan kebutuhan orang lain yang mungkin tidak terekspresikan,Selalu menunjukkan kepekaan dan empati yang tinggi terhadap perasaan orang lain.,Kurang sensitif terhadap perasaan orang lain.
Impact,Accountable,Dapat diandalkan dan selalu mengemban amanah untuk mencapai tujuan,Mengemban tanggung jawab dan memastikan semua komitmen terpenuhi.,Kadang mengabaikan komitmen yang telah dibuat.
Impact,Accountable,Dapat diandalkan dan selalu mengemban amanah untuk mencapai tujuan,Dapat diandalkan untuk memastikan tugas-tugas diselesaikan.,Kurang konsisten dalam menyelesaikan tugas.
Impact,Decisive,Mampu mengambil keputusan dengan cepat tepat dan tanpa ragu.,Tidak menunda-nunda keputusan penting,Cenderung menunda pengambilan keputusan.
Impact,Decisive,Mampu mengambil keputusan dengan cepat tepat dan tanpa ragu.,Bertindak cepat saat dibutuhkan,Perlu waktu lama untuk bertindak.
Impact,Flexible,Bersedia memodifikasi pendekatan mereka sesuai situasi atau kondisi yang ada,Siap menyesuaikan diri dan menerima perubahan ketika terjadi.,Sulit beradaptasi dengan perubahan.
Impact,Flexible,Bersedia memodifikasi pendekatan mereka sesuai situasi atau kondisi yang ada,Tetap tenang ketika ada perubahan yang bersifat tiba-tiba karena mereka percaya bahwa perubahan adalah sesuatu yang akan selalu terjadi.,Stres menghadapi perubahan mendadak."""
        
        from io import StringIO
        df = pd.read_csv(StringIO(data))
        return df

def create_questions(df, num_questions=60):
    """
    Buat soal dari data dengan randomisasi
    - Setiap soal hanya berisi SATU jenis perilaku (semua Kuat atau semua Lemah)
    - Opsi dalam soal diacak
    - Urutan soal juga diacak
    """
    questions = []
    grouped = df.groupby(['Dimensi', 'Aspek', 'Arti']).agg({
        'Perilaku Kuat': list,
        'Perilaku Lemah': list
    }).reset_index()
    
    question_count = 0
    max_attempts = num_questions * 10  # Prevent infinite loop
    attempts = 0
    
    while question_count < num_questions and attempts < max_attempts:
        attempts += 1
        idx = random.randint(0, len(grouped) - 1)
        row = grouped.iloc[idx]
        
        # Pilih secara random: gunakan Perilaku Kuat atau Perilaku Lemah
        behavior_type = random.choice(['Perilaku Kuat', 'Perilaku Lemah'])
        all_behaviors = row[behavior_type]
        
        # Ambil 6 perilaku dari tipe yang dipilih
        if len(all_behaviors) >= 6:
            selected_behaviors = random.sample(all_behaviors, 6)
        else:
            # Jika tidak cukup 6, ambil semua yang ada dan cari tambahan dari aspek lain dengan tipe yang sama
            selected_behaviors = all_behaviors.copy()
            other_behaviors = df[df['Aspek'] != row['Aspek']][behavior_type].tolist()
            other_behaviors = [b for b in other_behaviors if pd.notna(b)]  # Remove NaN
            
            if len(other_behaviors) > 0:
                additional_needed = min(6 - len(selected_behaviors), len(other_behaviors))
                additional = random.sample(other_behaviors, additional_needed)
                selected_behaviors.extend(additional)
        
        # Pastikan ada minimal 3 opsi untuk dipilih
        if len(selected_behaviors) < 3:
            continue
            
        selected_behaviors = selected_behaviors[:6]  # Maksimal 6 opsi
        
        questions.append({
            'dimensi': row['Dimensi'],
            'aspek': row['Aspek'],
            'arti': row['Arti'],
            'behaviors': selected_behaviors,
            'behavior_type': behavior_type,  # Track tipe perilaku
            'original_order': list(range(len(selected_behaviors)))
        })
        
        question_count += 1
    
    # Acak urutan soal
    random.shuffle(questions)
    
    # Acak opsi dalam setiap soal
    for q in questions:
        combined = list(zip(q['behaviors'], q['original_order']))
        random.shuffle(combined)
        q['behaviors'], q['original_order'] = zip(*combined)
        q['behaviors'] = list(q['behaviors'])
        q['original_order'] = list(q['original_order'])
    
    return questions

def calculate_results(answers, questions):
    """Hitung skor untuk setiap aspek"""
    aspect_scores = Counter()
    aspect_dimensions = {}
    
    for q_idx, answer in answers.items():
        if answer:
            question = questions[q_idx]
            for selected_idx in answer:
                aspect_scores[question['aspek']] += 1
                aspect_dimensions[question['aspek']] = question['dimensi']
    
    return aspect_scores, aspect_dimensions

def save_results(username_bps, nama, nip, satker, top_10, bottom_5):
    """Simpan hasil survey ke CSV"""
    result_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'username_bps': username_bps,
        'nama': nama,
        'nip': nip,
        'satker': satker,
        'top_10': json.dumps(top_10),
        'bottom_5': json.dumps(bottom_5)
    }
    
    df_result = pd.DataFrame([result_data])
    
    if os.path.exists(RESULTS_FILE):
        df_existing = pd.read_csv(RESULTS_FILE)
        df_result = pd.concat([df_existing, df_result], ignore_index=True)
    
    df_result.to_csv(RESULTS_FILE, index=False)
    return True

def load_results():
    """Load hasil survey dari CSV"""
    if os.path.exists(RESULTS_FILE):
        return pd.read_csv(RESULTS_FILE)
    return pd.DataFrame(columns=['timestamp', 'username_bps', 'nama', 'nip', 'satker', 'top_10', 'bottom_5'])

# ==================== TAMPILAN HASIL USER ====================

def display_results(aspect_scores, aspect_dimensions, user_data=None):
    """Tampilkan hasil top 10 dan bottom 5"""
    
    st.markdown("""
    <div class="welcome-banner animated-content">
        <h1>🎉 Selamat! Survey Anda Telah Selesai</h1>
        <p style="font-size: 18px; opacity: 0.95;">Berikut adalah hasil analisis kepribadian MRI Anda</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tampilkan info user dengan pengecekan satker
    satker_display = f"<p style='margin: 5px 0;'><b>Satker:</b> {user_data['satker']}</p>" if 'satker' in user_data else ""
    
    if user_data:
        st.markdown(f"""
        <div class="user-info-box animated-content">
            <h3>👤 Informasi Peserta</h3>
            <p style="margin: 5px 0;"><b>Username BPS:</b> {user_data['username_bps']}</p>
            <p style="margin: 5px 0;"><b>Nama:</b> {user_data['nama']}</p>
            <p style="margin: 5px 0;"><b>NIP:</b> {user_data['nip']}</p>
            {satker_display}
        </div>
        """, unsafe_allow_html=True)
    
    sorted_aspects = sorted(aspect_scores.items(), key=lambda x: x[1], reverse=True)
    
    st.markdown("<div class='animated-content'>", unsafe_allow_html=True)
    st.header("🏆 Top 10 Aspek Dominan Anda")
    st.markdown("</div>", unsafe_allow_html=True)
    
    top_10 = sorted_aspects[:10]
    
    fig_top = go.Figure()
    
    for aspect, score in top_10:
        dimension = aspect_dimensions.get(aspect, 'Unknown')
        color = DIMENSION_COLORS.get(dimension, '#gray')
        
        fig_top.add_trace(go.Bar(
            y=[aspect],
            x=[score],
            orientation='h',
            marker=dict(
                color=color,
                line=dict(color='white', width=2)
            ),
            name=dimension,
            text=score,
            textposition='outside',
            textfont=dict(size=14, color=color, family='Poppins'),
            hovertemplate=f'<b>{aspect}</b><br>Dimensi: {dimension}<br>Skor: {score}<extra></extra>'
        ))
    
    fig_top.update_layout(
        title={
            'text': "Top 10 Aspek Dominan",
            'font': {'size': 24, 'family': 'Poppins', 'weight': 'bold'}
        },
        xaxis_title="Skor",
        yaxis_title="",
        showlegend=False,
        height=550,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    st.plotly_chart(fig_top, use_container_width=True)
    
    col1, col2 = st.columns(2)
    for idx, (aspect, score) in enumerate(top_10):
        dimension = aspect_dimensions.get(aspect, 'Unknown')
        color = DIMENSION_COLORS.get(dimension, '#gray')
        
        with col1 if idx % 2 == 0 else col2:
            st.markdown(f"""
            <div class="aspect-card" style="background: linear-gradient(135deg, {color}15 0%, {color}30 100%); border-left: 5px solid {color}">
                <h4 style="margin: 0; color: {color}; font-size: 20px;">#{idx + 1} {aspect}</h4>
                <p style="margin: 8px 0 0 0; color: #666; font-size: 15px;">
                    <b>Dimensi:</b> {dimension} | <b>Skor:</b> <span style="color: {color}; font-weight: 700; font-size: 18px;">{score}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><hr style='border: 2px solid #f0f2f6; border-radius: 5px;'><br>", unsafe_allow_html=True)
    
    st.markdown("<div class='animated-content'>", unsafe_allow_html=True)
    st.header("📈 5 Aspek yang Perlu Dikembangkan")
    st.markdown("Ini adalah area potensial untuk pengembangan diri Anda")
    st.markdown("</div>", unsafe_allow_html=True)
    
    bottom_5 = sorted_aspects[-5:] if len(sorted_aspects) >= 5 else sorted_aspects
    
    fig_bottom = go.Figure()
    
    for aspect, score in bottom_5:
        dimension = aspect_dimensions.get(aspect, 'Unknown')
        color = DIMENSION_COLORS.get(dimension, '#gray')
        
        fig_bottom.add_trace(go.Bar(
            y=[aspect],
            x=[score],
            orientation='h',
            marker=dict(
                color=color,
                line=dict(color='white', width=2)
            ),
            name=dimension,
            text=score,
            textposition='outside',
            textfont=dict(size=14, color=color, family='Poppins'),
            hovertemplate=f'<b>{aspect}</b><br>Dimensi: {dimension}<br>Skor: {score}<extra></extra>'
        ))
    
    fig_bottom.update_layout(
        title={
            'text': "5 Aspek yang Perlu Dikembangkan",
            'font': {'size': 24, 'family': 'Poppins', 'weight': 'bold'}
        },
        xaxis_title="Skor",
        yaxis_title="",
        showlegend=False,
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    st.plotly_chart(fig_bottom, use_container_width=True)
    
    col1, col2 = st.columns(2)
    for idx, (aspect, score) in enumerate(bottom_5):
        dimension = aspect_dimensions.get(aspect, 'Unknown')
        color = DIMENSION_COLORS.get(dimension, '#gray')
        
        with col1 if idx % 2 == 0 else col2:
            st.markdown(f"""
            <div class="aspect-card" style="background: linear-gradient(135deg, {color}15 0%, {color}30 100%); border-left: 5px solid {color}">
                <h4 style="margin: 0; color: {color}; font-size: 18px;">{aspect}</h4>
                <p style="margin: 8px 0 0 0; color: #666; font-size: 14px;">
                    <b>Dimensi:</b> {dimension} | <b>Skor:</b> <span style="color: {color}; font-weight: 700; font-size: 16px;">{score}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎨 Legenda Dimensi")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='legend-button' style='background: linear-gradient(135deg, {DIMENSION_COLORS['Motivation']} 0%, {DIMENSION_COLORS['Motivation']}dd 100%);'>🎯 Motivation</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='legend-button' style='background: linear-gradient(135deg, {DIMENSION_COLORS['Relation']} 0%, {DIMENSION_COLORS['Relation']}dd 100%);'>🤝 Relation</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='legend-button' style='background: linear-gradient(135deg, {DIMENSION_COLORS['Impact']} 0%, {DIMENSION_COLORS['Impact']}dd 100%);'>⚡ Impact</div>", unsafe_allow_html=True)
    
    top_10_data = [{'aspek': aspect, 'skor': score, 'dimensi': aspect_dimensions.get(aspect, 'Unknown')} for aspect, score in top_10]
    bottom_5_data = [{'aspek': aspect, 'skor': score, 'dimensi': aspect_dimensions.get(aspect, 'Unknown')} for aspect, score in bottom_5]
    
    return top_10_data, bottom_5_data

def user_data_form():
    """Form untuk input data diri user sebelum mengerjakan survey"""
    st.markdown("""
    <div class="welcome-banner">
        <h1>📝 Selamat Datang di MRI Survey</h1>
        <p style="font-size: 18px; opacity: 0.95;">Silakan masukkan data Anda untuk memulai</p>
    </div>
    """, unsafe_allow_html=True)
    
    
    # Info box
    st.info("ℹ️ **Petunjuk:** Masukkan username BPS dan NIP Anda yang telah terdaftar di database, serta pilih asal satker Anda")
    
    with st.form("user_data_form"):
        st.markdown("### 👤 Informasi Peserta")
        
        col1, col2 = st.columns(2)
        with col1:
            username_bps = st.text_input("Username BPS *", placeholder="Contoh: thomson")
        with col2:
            nip = st.text_input("NIP *", placeholder="Contoh: 200104052024121001")
        
        satker = st.selectbox(
            "Asal Satuan Kerja *",
            options=["-- Pilih Satker --"] + SATKER_LAMPUNG,
            index=0,
            help="Pilih satuan kerja tempat Anda bertugas"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✅ Mulai Survey", use_container_width=True)
        
        if submitted:
            # Validasi input kosong
            if not username_bps or not nip or satker == "-- Pilih Satker --":
                st.error("❌ Semua field harus diisi!")
                return None
            
            username_clean = username_bps.strip()
            nip_clean = nip.strip()
            
            # Validasi NIP harus angka
            if not nip_clean.isdigit():
                st.error("❌ NIP harus berupa angka!")
                return None
            
            # Validasi 1: Cek apakah username terdaftar di biodata
            if not check_username_exists(username_clean):
                st.error(f"❌ Username '{username_clean}' tidak terdaftar dalam database!")
                st.warning("💡 Pastikan username BPS Anda sudah terdaftar. Hubungi admin jika ada masalah.")
                return None
            
            # Validasi 2: Cek apakah NIP sesuai dengan username
            if not validate_nip(username_clean, nip_clean):
                st.error(f"❌ NIP tidak sesuai dengan username '{username_clean}'!")
                st.warning("⚠️ Pastikan NIP yang Anda masukkan sesuai dengan data registrasi Anda.")
                return None
            
            # Validasi 3: Cek apakah username sudah pernah mengerjakan survey
            if check_username_taken(username_clean):
                st.error(f"❌ Username '{username_clean}' sudah pernah mengerjakan survey!")
                st.warning("⚠️ Setiap pegawai hanya dapat mengerjakan survey satu kali. Hasil Anda sudah tersimpan.")
                return None
            
            # Ambil data user dari biodata
            user_info = get_user_info(username_clean)
            
            if user_info:
                st.success(f"✅ Data valid! Selamat datang, {user_info['nama']} dari {satker}")
                # Tambahkan satker dari pilihan user
                user_info['satker'] = satker
                return user_info
            else:
                st.error("❌ Terjadi kesalahan dalam mengambil data user")
                return None
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Tampilkan informasi tambahan
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("❓ Bantuan & Informasi"):
        st.markdown("""
        **Jika Anda mengalami masalah:**
        
        1. **Username tidak terdaftar:**
           - Pastikan username BPS Anda sudah terdaftar di sistem
           - Hubungi admin untuk mendaftarkan username Anda
        
        2. **NIP tidak sesuai:**
           - Pastikan NIP yang diinput sesuai dengan NIP di data registrasi
           - Hubungi admin jika ada perbedaan data
        
        3. **Sudah pernah mengerjakan:**
           - Setiap pegawai hanya dapat mengerjakan survey satu kali
           - Hubungi admin jika perlu melihat hasil survey Anda
        
        4. **Lupa username atau NIP:**
           - Hubungi admin untuk mengecek data Anda
        
        5. **Satker:**
           - Pilih satuan kerja sesuai tempat Anda bertugas saat ini
           - Data satker akan tersimpan untuk analisis
        """)
    
    return None

# ==================== SURVEY USER ====================

def user_survey(df):
    """Survey untuk user"""
    
    # Inisialisasi session state
    if 'survey_initialized' not in st.session_state:
        st.session_state.survey_initialized = True
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.questions = None
        st.session_state.completed = False
        st.session_state.user_data = None
    
    # Form input data diri
    if st.session_state.user_data is None:
        user_data = user_data_form()
        if user_data:
            st.session_state.user_data = user_data
            st.rerun()
        return
    
    # Generate questions
    if st.session_state.questions is None:
        st.session_state.questions = create_questions(df, num_questions=60)
    
    questions = st.session_state.questions
    
    # Jika survey selesai
    if st.session_state.completed:
        aspect_scores, aspect_dimensions = calculate_results(st.session_state.answers, questions)
        top_10_data, bottom_5_data = display_results(aspect_scores, aspect_dimensions, st.session_state.user_data)
        
        if 'result_saved' not in st.session_state:
            # Ambil satker dari user_data, default ke "Tidak Diketahui" jika tidak ada
            satker_value = st.session_state.user_data.get('satker', 'Tidak Diketahui')
            
            save_results(
                st.session_state.user_data['username_bps'],
                st.session_state.user_data['nama'],
                st.session_state.user_data['nip'],
                satker_value,
                top_10_data,
                bottom_5_data
            )
            st.session_state.result_saved = True
            st.success("✅ Hasil survey Anda telah tersimpan!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Mulai Survey Baru", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        return
    
    # Header
    st.markdown("""
    <div class="welcome-banner">
        <h1>🧠 Survey MRI Pegawai BPS Provinsi Lampung</h1>
        <p style="font-size: 18px; opacity: 0.95;">Temukan Profil Kepribadian Anda</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tampilkan info user dengan pengecekan satker
    satker_info = f"<p style='margin: 5px 0; color: #666; font-size: 14px;'>📍 {st.session_state.user_data['satker']}</p>" if 'satker' in st.session_state.user_data else ""
    
    st.markdown(f"""
    <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); margin-bottom: 20px;">
        <h3 style="margin: 0; color: #667eea;">Selamat datang, <span style="color: #764ba2;">{st.session_state.user_data['nama']}</span>! 👋</h3>
        {satker_info}
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress = (st.session_state.current_question) / len(questions)
    st.progress(progress)
    st.markdown(f"<p class='progress-text'>Pertanyaan {st.session_state.current_question + 1} dari {len(questions)} ({progress*100:.0f}%)</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tampilkan pertanyaan
    current_q_idx = st.session_state.current_question
    question = questions[current_q_idx]
    
    st.markdown(f"""
    <div class="question-box">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #667eea; margin: 0;">Pertanyaan {current_q_idx + 1}</h2>
        </div>
        <p style="color: #666; font-size: 18px; text-align: center; background: #f8f9ff; padding: 15px; border-radius: 10px; border: 2px solid #667eea;">
            💡 <b>Instruksi:</b> Pilih <b>3 pernyataan</b> yang paling menggambarkan Anda
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Opsi jawaban
    selected_options = []
    
    st.markdown("<div style='background: white; padding: 25px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.08);'>", unsafe_allow_html=True)
    
    for idx, behavior in enumerate(question['behaviors']):
        is_selected = st.checkbox(
            behavior,
            key=f"q_{current_q_idx}_opt_{idx}",
            value=idx in st.session_state.answers.get(current_q_idx, [])
        )
        if is_selected:
            selected_options.append(idx)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if len(selected_options) > 3:
        st.error("❌ Anda hanya bisa memilih maksimal 3 pernyataan!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tombol navigasi
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_q_idx > 0:
            if st.button("⬅️ Sebelumnya", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        if len(selected_options) == 3:
            st.success(f"✅ {len(selected_options)}/3 dipilih")
        elif len(selected_options) > 0:
            st.warning(f"⚠️ {len(selected_options)}/3 dipilih")
        else:
            st.info("ℹ️ 0/3 dipilih")
    
    with col3:
        if len(selected_options) == 3:
            if current_q_idx < len(questions) - 1:
                if st.button("Selanjutnya ➡️", use_container_width=True):
                    st.session_state.answers[current_q_idx] = selected_options
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("🎉 Selesai", use_container_width=True):
                    st.session_state.answers[current_q_idx] = selected_options
                    st.session_state.completed = True
                    st.rerun()
        else:
            st.button("Selanjutnya ➡️", disabled=True, use_container_width=True)

# ==================== ADMIN DASHBOARD ====================

def analyze_satker_characteristics(df_results):
    """Analisis karakteristik per satker"""
    if df_results.empty or 'satker' not in df_results.columns:
        return None
    
    satker_analysis = {}
    
    for satker in df_results['satker'].unique():
        satker_data = df_results[df_results['satker'] == satker]
        
        # Kumpulkan semua aspek top 10 untuk satker ini
        all_aspects = []
        aspect_dimensions = {}
        
        for top_10_str in satker_data['top_10']:
            top_10 = json.loads(top_10_str)
            for item in top_10:
                all_aspects.append(item['aspek'])
                aspect_dimensions[item['aspek']] = item['dimensi']
        
        # Hitung frekuensi aspek
        aspect_counter = Counter(all_aspects)
        top_5_aspects = aspect_counter.most_common(5)
        
        # Hitung distribusi dimensi
        dimension_counter = Counter([aspect_dimensions.get(asp, 'Unknown') for asp in all_aspects])
        
        satker_analysis[satker] = {
            'total_peserta': len(satker_data),
            'top_5_aspects': top_5_aspects,
            'dimension_distribution': dimension_counter,
            'aspect_dimensions': aspect_dimensions
        }
    
    return satker_analysis

def admin_dashboard():
    """Dashboard admin untuk melihat hasil semua peserta"""
    st.markdown("""
    <div class="welcome-banner">
        <h1>🎯 Admin Dashboard</h1>
        <p style="font-size: 18px; opacity: 0.95;">MRI Survey Analytics & Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    df_results = load_results()
    
    if df_results.empty:
        st.warning("⚠️ Belum ada data hasil survey.")
        return
    
    # Metrics Overview dengan animasi
    st.header("📊 Overview Statistik")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{len(df_results)}</h2>
            <p>Total Peserta</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        latest = pd.to_datetime(df_results['timestamp']).max()
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h4 style="margin: 0; color: white; font-size: 22px;">{latest.strftime('%d/%m/%Y')}</h4>
            <p>Survey Terakhir</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        all_top_aspects = []
        for top_10_str in df_results['top_10']:
            top_10 = json.loads(top_10_str)
            all_top_aspects.extend([item['aspek'] for item in top_10])
        
        if all_top_aspects:
            most_common = Counter(all_top_aspects).most_common(1)[0][0]
        else:
            most_common = "N/A"
        
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h4 style="margin: 0; color: white; font-size: 18px;">{most_common[:20]}</h4>
            <p>Aspek Terpopuler</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <h2>60</h2>
            <p>Total Pertanyaan</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs dengan styling yang lebih baik
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Ranking Aspek",
        "🏆 Top 10 Populer",
        "📉 Bottom 5 Populer",
        "👥 Data Peserta",
        "📈 Analisis Dimensi",
        "🏢 Karakteristik Satker"
    ])
    
    # TAB 1: Ranking Aspek
    with tab1:
        st.subheader("🎯 Ranking Rata-rata Skor Aspek")
        
        all_aspects_scores = {}
        all_aspects_dimensions = {}
        
        for idx, row in df_results.iterrows():
            top_10 = json.loads(row['top_10'])
            bottom_5 = json.loads(row['bottom_5'])
            
            for item in top_10 + bottom_5:
                aspek = item['aspek']
                skor = item['skor']
                dimensi = item['dimensi']
                
                if aspek not in all_aspects_scores:
                    all_aspects_scores[aspek] = []
                    all_aspects_dimensions[aspek] = dimensi
                
                all_aspects_scores[aspek].append(skor)
        
        avg_scores = {aspek: sum(scores) / len(scores) for aspek, scores in all_aspects_scores.items()}
        sorted_avg = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)
        
        st.markdown("#### 🥇 Top 10 Aspek dengan Skor Rata-rata Tertinggi")
        top_10_avg = sorted_avg[:10]
        
        fig_avg_top = go.Figure()
        for aspek, avg_score in top_10_avg:
            dimension = all_aspects_dimensions.get(aspek, 'Unknown')
            color = DIMENSION_COLORS.get(dimension, '#gray')
            
            fig_avg_top.add_trace(go.Bar(
                x=[aspek],
                y=[avg_score],
                marker=dict(
                    color=color,
                    line=dict(color='white', width=2)
                ),
                text=f'{avg_score:.2f}',
                textposition='outside',
                textfont=dict(size=12, family='Poppins'),
                hovertemplate=f'<b>{aspek}</b><br>Dimensi: {dimension}<br>Rata-rata: {avg_score:.2f}<extra></extra>',
                showlegend=False
            ))
        
        fig_avg_top.update_layout(
            xaxis_title="Aspek",
            yaxis_title="Skor Rata-rata",
            height=500,
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_avg_top, use_container_width=True)
        
        st.markdown("#### 📉 5 Aspek dengan Skor Rata-rata Terendah")
        bottom_5_avg = sorted_avg[-5:]
        
        fig_avg_bottom = go.Figure()
        for aspek, avg_score in bottom_5_avg:
            dimension = all_aspects_dimensions.get(aspek, 'Unknown')
            color = DIMENSION_COLORS.get(dimension, '#gray')
            
            fig_avg_bottom.add_trace(go.Bar(
                x=[aspek],
                y=[avg_score],
                marker=dict(
                    color=color,
                    line=dict(color='white', width=2)
                ),
                text=f'{avg_score:.2f}',
                textposition='outside',
                textfont=dict(size=12, family='Poppins'),
                hovertemplate=f'<b>{aspek}</b><br>Dimensi: {dimension}<br>Rata-rata: {avg_score:.2f}<extra></extra>',
                showlegend=False
            ))
        
        fig_avg_bottom.update_layout(
            xaxis_title="Aspek",
            yaxis_title="Skor Rata-rata",
            height=400,
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_avg_bottom, use_container_width=True)
    
    # TAB 2: Top 10 Populer
    with tab2:
        st.subheader("🏆 Aspek yang Paling Sering Muncul di Top 10")
        
        all_top_aspects_detail = []
        for top_10_str in df_results['top_10']:
            top_10 = json.loads(top_10_str)
            all_top_aspects_detail.extend(top_10)
        
        aspect_counter = Counter([item['aspek'] for item in all_top_aspects_detail])
        top_popular = aspect_counter.most_common(15)
        
        fig_popular = go.Figure()
        
        for aspek, count in top_popular:
            dimension = next((item['dimensi'] for item in all_top_aspects_detail if item['aspek'] == aspek), 'Unknown')
            color = DIMENSION_COLORS.get(dimension, '#gray')
            
            fig_popular.add_trace(go.Bar(
                x=[aspek],
                y=[count],
                marker=dict(
                    color=color,
                    line=dict(color='white', width=2)
                ),
                text=count,
                textposition='outside',
                textfont=dict(size=12, family='Poppins'),
                hovertemplate=f'<b>{aspek}</b><br>Dimensi: {dimension}<br>Muncul: {count}x<extra></extra>',
                showlegend=False
            ))
        
        fig_popular.update_layout(
            title="Frekuensi Kemunculan di Top 10",
            xaxis_title="Aspek",
            yaxis_title="Jumlah Kemunculan",
            height=500,
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_popular, use_container_width=True)
        
        st.markdown("#### 🎨 Distribusi Dimensi di Top 10")
        dimension_counter = Counter([item['dimensi'] for item in all_top_aspects_detail])
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=list(dimension_counter.keys()),
            values=list(dimension_counter.values()),
            marker=dict(colors=[DIMENSION_COLORS.get(d, '#gray') for d in dimension_counter.keys()]),
            hole=0.4,
            textfont=dict(size=16, family='Poppins')
        )])
        
        fig_pie.update_layout(
            title="Proporsi Dimensi dalam Top 10 Semua Peserta",
            height=400
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # TAB 3: Bottom 5 Populer
    with tab3:
        st.subheader("📉 Aspek yang Paling Sering Muncul di Bottom 5")
        
        all_bottom_aspects_detail = []
        for bottom_5_str in df_results['bottom_5']:
            bottom_5 = json.loads(bottom_5_str)
            all_bottom_aspects_detail.extend(bottom_5)
        
        bottom_aspect_counter = Counter([item['aspek'] for item in all_bottom_aspects_detail])
        bottom_popular = bottom_aspect_counter.most_common(15)
        
        fig_bottom_popular = go.Figure()
        
        for aspek, count in bottom_popular:
            dimension = next((item['dimensi'] for item in all_bottom_aspects_detail if item['aspek'] == aspek), 'Unknown')
            color = DIMENSION_COLORS.get(dimension, '#gray')
            
            fig_bottom_popular.add_trace(go.Bar(
                x=[aspek],
                y=[count],
                marker=dict(
                    color=color,
                    line=dict(color='white', width=2)
                ),
                text=count,
                textposition='outside',
                textfont=dict(size=12, family='Poppins'),
                hovertemplate=f'<b>{aspek}</b><br>Dimensi: {dimension}<br>Muncul: {count}x<extra></extra>',
                showlegend=False
            ))
        
        fig_bottom_popular.update_layout(
            title="Frekuensi Kemunculan di Bottom 5",
            xaxis_title="Aspek",
            yaxis_title="Jumlah Kemunculan",
            height=500,
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_bottom_popular, use_container_width=True)
    
    # TAB 4: Data Peserta
    with tab4:
        st.subheader("👥 Data Lengkap Peserta")
        
        display_df = df_results.copy()
        display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%d/%m/%Y %H:%M')
        
        st.dataframe(
            display_df[['timestamp', 'username_bps', 'nama', 'nip']],
            use_container_width=True,
            hide_index=True
        )
        
        csv = df_results.to_csv(index=False)
        st.download_button(
            label="📥 Download Data Lengkap (CSV)",
            data=csv,
            file_name=f"survey_results_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("#### 🔍 Detail Hasil Per Peserta")
        selected_user = st.selectbox(
            "Pilih Peserta:",
            options=df_results['nama'].tolist(),
            format_func=lambda x: f"{x} ({df_results[df_results['nama']==x]['username_bps'].values[0]})"
        )
        
        if selected_user:
            user_row = df_results[df_results['nama'] == selected_user].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 🏆 Top 10 Aspek")
                top_10 = json.loads(user_row['top_10'])
                for idx, item in enumerate(top_10, 1):
                    color = DIMENSION_COLORS.get(item['dimensi'], '#gray')
                    st.markdown(f"""
                    <div class="aspect-card" style="background: linear-gradient(135deg, {color}15 0%, {color}30 100%); border-left: 3px solid {color}; padding: 12px;">
                        <b>#{idx} {item['aspek']}</b> - Skor: <span style="color: {color}; font-weight: 700;">{item['skor']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("##### 📈 Bottom 5 Aspek")
                bottom_5 = json.loads(user_row['bottom_5'])
                for item in bottom_5:
                    color = DIMENSION_COLORS.get(item['dimensi'], '#gray')
                    st.markdown(f"""
                    <div class="aspect-card" style="background: linear-gradient(135deg, {color}15 0%, {color}30 100%); border-left: 3px solid {color}; padding: 12px;">
                        <b>{item['aspek']}</b> - Skor: <span style="color: {color}; font-weight: 700;">{item['skor']}</span>
                    </div>
                    """, unsafe_allow_html=True)
    
    # TAB 5: Analisis Dimensi
    with tab5:
        st.subheader("📊 Analisis Berdasarkan Dimensi")
        
        dimension_scores = {'Motivation': [], 'Relation': [], 'Impact': []}
        
        for idx, row in df_results.iterrows():
            top_10 = json.loads(row['top_10'])
            bottom_5 = json.loads(row['bottom_5'])
            
            for item in top_10 + bottom_5:
                dimensi = item['dimensi']
                skor = item['skor']
                if dimensi in dimension_scores:
                    dimension_scores[dimensi].append(skor)
        
        avg_dimension_scores = {dim: sum(scores)/len(scores) if scores else 0 
                               for dim, scores in dimension_scores.items()}
        
        fig_dim = go.Figure()
        
        for dim, avg_score in avg_dimension_scores.items():
            color = DIMENSION_COLORS.get(dim, '#gray')
            fig_dim.add_trace(go.Bar(
                x=[dim],
                y=[avg_score],
                marker=dict(
                    color=color,
                    line=dict(color='white', width=2)
                ),
                text=f'{avg_score:.2f}',
                textposition='outside',
                textfont=dict(size=14, family='Poppins'),
                showlegend=False
            ))
        
        fig_dim.update_layout(
            title="Rata-rata Skor per Dimensi",
            xaxis_title="Dimensi",
            yaxis_title="Skor Rata-rata",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_dim, use_container_width=True)
        
        st.markdown("#### 📦 Distribusi Skor per Dimensi")
        
        fig_box = go.Figure()
        
        for dim, scores in dimension_scores.items():
            if scores:
                color = DIMENSION_COLORS.get(dim, '#gray')
                fig_box.add_trace(go.Box(
                    y=scores,
                    name=dim,
                    marker_color=color,
                    boxmean='sd',
                    line=dict(width=2)
                ))
        
        fig_box.update_layout(
            title="Distribusi Skor Dimensi (dengan Mean & Standar Deviasi)",
            yaxis_title="Skor",
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_box, use_container_width=True)
        
        st.markdown("#### 🔥 Aspek yang Sering Muncul Bersamaan")
        
        from itertools import combinations
        cooccurrence = Counter()
        
        for idx, row in df_results.iterrows():
            top_10 = json.loads(row['top_10'])
            aspects = [item['aspek'] for item in top_10]
            
            for pair in combinations(aspects, 2):
                cooccurrence[tuple(sorted(pair))] += 1
        
        top_pairs = cooccurrence.most_common(10)
        
        if top_pairs:
            for i, ((asp1, asp2), count) in enumerate(top_pairs, 1):
                st.markdown(f"""
                <div class="aspect-card" style="background: linear-gradient(135deg, #667eea15 0%, #764ba230 100%); border-left: 3px solid #667eea;">
                    <b>{i}.</b> {asp1} ↔ {asp2}: <span style="color: #667eea; font-weight: 700;">{count}x</span>
                </div>
                """, unsafe_allow_html=True)
    # TAB 6: Karakteristik Satker
    with tab6:
        show_satker_analysis(df_results)


def show_overview_dashboard(df_results):
    """Tampilkan overview dashboard"""
def show_overview_dashboard(df_results):
    """Tampilkan overview dashboard"""
    # Metrics Overview
    st.header("📊 Overview Statistik")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{len(df_results)}</h2>
            <p>Total Peserta</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        latest = pd.to_datetime(df_results['timestamp']).max()
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h4 style="margin: 0; color: white; font-size: 22px;">{latest.strftime('%d/%m/%Y')}</h4>
            <p>Survey Terakhir</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        all_top_aspects = []
        for top_10_str in df_results['top_10']:
            top_10 = json.loads(top_10_str)
            all_top_aspects.extend([item['aspek'] for item in top_10])
        
        if all_top_aspects:
            most_common = Counter(all_top_aspects).most_common(1)[0][0]
        else:
            most_common = "N/A"
        
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h4 style="margin: 0; color: white; font-size: 18px;">{most_common[:20]}</h4>
            <p>Aspek Terpopuler</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if 'satker' in df_results.columns:
            total_satker = df_results['satker'].nunique()
        else:
            total_satker = 0
        
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <h2>{total_satker}</h2>
            <p>Satker Berpartisipasi</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Distribusi per Satker
    if 'satker' in df_results.columns:
        st.subheader("📍 Distribusi Peserta per Satker")
        satker_counts = df_results['satker'].value_counts().reset_index()
        satker_counts.columns = ['Satker', 'Jumlah Peserta']
        
        fig_satker = px.bar(
            satker_counts,
            x='Jumlah Peserta',
            y='Satker',
            orientation='h',
            color='Jumlah Peserta',
            color_continuous_scale='Viridis',
            title='Jumlah Peserta per Satker'
        )
        fig_satker.update_layout(
            height=500,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_satker, use_container_width=True)

def show_satker_analysis(df_results):
    """Tampilkan analisis karakteristik per satker"""
    st.header("🗺️ Analisis Karakteristik per Satker")
    
    if 'satker' not in df_results.columns:
        st.warning("⚠️ Data satker tidak tersedia")
        return
    
    # Analisis karakteristik
    satker_analysis = analyze_satker_characteristics(df_results)
    
    if not satker_analysis:
        st.warning("⚠️ Tidak dapat menganalisis data satker")
        return
    
    # Pilih satker untuk analisis detail
    selected_satker = st.selectbox(
        "Pilih Satker untuk Analisis Detail:",
        options=sorted(satker_analysis.keys())
    )
    
    if selected_satker:
        analysis = satker_analysis[selected_satker]
        
        # Header info satker
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 15px; color: white; margin-bottom: 20px;">
            <h2 style="margin: 0; color: white;">{selected_satker}</h2>
            <p style="margin: 10px 0 0 0; font-size: 18px;">Total Peserta: <b>{analysis['total_peserta']}</b> orang</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Top 5 Aspek Dominan
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🏆 Top 5 Aspek Dominan")
            
            top_5_data = []
            for aspect, count in analysis['top_5_aspects']:
                dimension = analysis['aspect_dimensions'].get(aspect, 'Unknown')
                top_5_data.append({
                    'Aspek': aspect,
                    'Frekuensi': count,
                    'Dimensi': dimension
                })
            
            df_top5 = pd.DataFrame(top_5_data)
            
            fig_aspects = px.bar(
                df_top5,
                x='Frekuensi',
                y='Aspek',
                orientation='h',
                color='Dimensi',
                color_discrete_map=DIMENSION_COLORS,
                title=f'Aspek Paling Dominan di {selected_satker}'
            )
            fig_aspects.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_aspects, use_container_width=True)
        
        with col2:
            st.subheader("📊 Distribusi Dimensi")
            
            dimension_data = []
            for dim, count in analysis['dimension_distribution'].items():
                dimension_data.append({
                    'Dimensi': dim,
                    'Jumlah': count
                })
            
            df_dim = pd.DataFrame(dimension_data)
            
            fig_pie = px.pie(
                df_dim,
                values='Jumlah',
                names='Dimensi',
                color='Dimensi',
                color_discrete_map=DIMENSION_COLORS,
                title='Proporsi Dimensi'
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Detail aspek dalam cards
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📋 Detail Aspek Dominan")
        
        cols = st.columns(2)
        for idx, (aspect, count) in enumerate(analysis['top_5_aspects']):
            dimension = analysis['aspect_dimensions'].get(aspect, 'Unknown')
            color = DIMENSION_COLORS.get(dimension, '#gray')
            
            with cols[idx % 2]:
                st.markdown(f"""
                <div class="aspect-card" style="background: linear-gradient(135deg, {color}15 0%, {color}30 100%); 
                                                border-left: 5px solid {color}">
                    <h4 style="margin: 0; color: {color}; font-size: 18px;">#{idx + 1} {aspect}</h4>
                    <p style="margin: 8px 0 0 0; color: #666; font-size: 14px;">
                        <b>Dimensi:</b> {dimension} | <b>Frekuensi:</b> <span style="color: {color}; 
                        font-weight: 700; font-size: 16px;">{count}x</span>
                    </p>
                    <p style="margin: 5px 0 0 0; color: #999; font-size: 12px;">
                        Muncul pada {count} dari {analysis['total_peserta']} peserta 
                        ({count/analysis['total_peserta']*100:.1f}%)
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br><hr style='border: 2px solid #f0f2f6;'><br>", unsafe_allow_html=True)
        
        # Perbandingan dengan satker lain
        st.subheader("📊 Perbandingan dengan Satker Lain")
        
        # Buat data untuk perbandingan dimensi
        comparison_data = []
        for satker, data in satker_analysis.items():
            for dim, count in data['dimension_distribution'].items():
                comparison_data.append({
                    'Satker': satker,
                    'Dimensi': dim,
                    'Jumlah': count,
                    'Persentase': (count / sum(data['dimension_distribution'].values())) * 100
                })
        
        df_comparison = pd.DataFrame(comparison_data)
        
        fig_comparison = px.bar(
            df_comparison,
            x='Satker',
            y='Persentase',
            color='Dimensi',
            color_discrete_map=DIMENSION_COLORS,
            title='Distribusi Dimensi per Satker (%)',
            barmode='group'
        )
        fig_comparison.update_layout(
            height=500,
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Tabel ringkasan semua satker
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📈 Ringkasan Semua Satker")
        
        summary_data = []
        for satker, data in satker_analysis.items():
            dim_dist = data['dimension_distribution']
            total = sum(dim_dist.values())
            
            summary_data.append({
                'Satker': satker,
                'Peserta': data['total_peserta'],
                'Aspek #1': data['top_5_aspects'][0][0] if data['top_5_aspects'] else '-',
                'Motivation %': f"{(dim_dist.get('Motivation', 0) / total * 100):.1f}%" if total > 0 else "0%",
                'Relation %': f"{(dim_dist.get('Relation', 0) / total * 100):.1f}%" if total > 0 else "0%",
                'Impact %': f"{(dim_dist.get('Impact', 0) / total * 100):.1f}%" if total > 0 else "0%"
            })
        
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True, hide_index=True)

def show_participant_data(df_results):
    """Tampilkan data peserta"""
def show_participant_data(df_results):
    """Tampilkan data peserta"""
    st.header("👥 Data Lengkap Peserta")
    
    # Tambahkan info jumlah username unik
    unique_users = df_results['username_bps'].nunique()
    st.info(f"📊 Total username unik yang sudah mengerjakan survey: **{unique_users}** dari **{len(df_results)}** records")
    
    # Filter berdasarkan satker
    if 'satker' in df_results.columns:
        satker_filter = st.multiselect(
            "Filter berdasarkan Satker:",
            options=sorted(df_results['satker'].unique()),
            default=None
        )
        
        if satker_filter:
            df_filtered = df_results[df_results['satker'].isin(satker_filter)]
        else:
            df_filtered = df_results
    else:
        df_filtered = df_results
    
    display_df = df_filtered.copy()
    display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%d/%m/%Y %H:%M')
    
    # Cek apakah kolom satker ada
    columns_to_show = ['timestamp', 'username_bps', 'nama', 'nip']
    if 'satker' in display_df.columns:
        columns_to_show.append('satker')
    
    st.dataframe(
        display_df[columns_to_show],
        use_container_width=True,
        hide_index=True
    )
    
    # Tambahkan fitur search username
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔍 Cek Username")
    search_username = st.text_input("Masukkan username untuk mengecek status:", placeholder="Contoh: thomson")
    
    if search_username:
        if check_username_taken(search_username):
            st.success(f"✅ Username '{search_username}' sudah pernah mengerjakan survey")
            # Tampilkan data user tersebut
            user_result = df_results[df_results['username_bps'].str.lower() == search_username.lower()]
            if not user_result.empty:
                st.markdown("**Detail:**")
                st.write(f"- Nama: {user_result.iloc[0]['nama']}")
                st.write(f"- NIP: {user_result.iloc[0]['nip']}")
                if 'satker' in user_result.columns:
                    st.write(f"- Satker: {user_result.iloc[0]['satker']}")
                st.write(f"- Waktu: {pd.to_datetime(user_result.iloc[0]['timestamp']).strftime('%d/%m/%Y %H:%M')}")
        else:
            st.warning(f"⚠️ Username '{search_username}' belum mengerjakan survey")
    
    st.markdown("<br>", unsafe_allow_html=True)
    csv = df_results.to_csv(index=False)
    st.download_button(
        label="📥 Download Data Lengkap (CSV)",
        data=csv,
        file_name=f"survey_results_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==================== MAIN APP ====================

def main():
    df = load_data()
    
    if 'selected_mode' not in st.session_state:
        st.session_state.selected_mode = "user"
    
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="color: white; margin: 0; font-size: 60px;">🧠</h1>
            <h2 style="color: white; margin: 10px 0;">MRI Survey</h2>
            <p style="color: rgba(255,255,255,0.8); font-size: 14px;">Survey MRI Pegawai BPS Provinsi Lampung</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.3); margin: 20px 0;'>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='color: white; text-align: center; margin-bottom: 20px;'>Pilih Mode</h3>", unsafe_allow_html=True)
        
        user_active = "active" if st.session_state.selected_mode == "user" else ""
        st.markdown(f"""
        <div class="mode-card {user_active}">
            <div class="mode-icon">👤</div>
            <h3>User Mode</h3>
            <p>Kerjakan survey kepribadian MRI</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Pilih User Mode", key="btn_user", use_container_width=True):
            st.session_state.selected_mode = "user"
            st.rerun()
        
        st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)
        
        admin_active = "active" if st.session_state.selected_mode == "admin" else ""
        st.markdown(f"""
        <div class="mode-card {admin_active}">
            <div class="mode-icon">🔐</div>
            <h3>Admin Mode</h3>
            <p>Akses dashboard dan analytics</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Pilih Admin Mode", key="btn_admin", use_container_width=True):
            st.session_state.selected_mode = "admin"
            st.rerun()
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.3); margin: 20px 0;'>", unsafe_allow_html=True)
        
        st.markdown("### 📚 Informasi")
        
        st.markdown("""
        <div class="sidebar-info">
            <p style="margin: 5px 0;"><b>Survey MRI mengukur:</b></p>
            <ul style="margin: 10px 0;">
                <li>🎯 <b>Motivation</b><br><span style="font-size: 12px; opacity: 0.8;">Dorongan & tujuan hidup</span></li>
                <li>🤝 <b>Relation</b><br><span style="font-size: 12px; opacity: 0.8;">Interaksi sosial</span></li>
                <li>⚡ <b>Impact</b><br><span style="font-size: 12px; opacity: 0.8;">Pengaruh & hasil kerja</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-info">
            <p style="margin: 5px 0;"><b>📋 Cara Kerja:</b></p>
            <ul style="margin: 10px 0;">
                <li>Validasi username otomatis</li>
                <li>60 pertanyaan interaktif</li>
                <li>Pilih 3 dari 6 opsi</li>
                <li>Perilaku Kuat atau Lemah</li>
                <li>Hasil analisis real-time</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-info">
            <p style="margin: 5px 0;"><b>💪 Perilaku Kuat:</b></p>
            <p style="font-size: 12px; opacity: 0.9; margin: 5px 0;">Perilaku yang sudah dominan dalam diri Anda</p>
            <p style="margin: 10px 0 5px 0;"><b>🌱 Perilaku Lemah:</b></p>
            <p style="font-size: 12px; opacity: 0.9; margin: 5px 0;">Perilaku yang perlu dikembangkan</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 12px; border-radius: 8px; text-align: center; margin-top: 20px;">
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">© 2024 MRI Survey System</p>
            <p style="margin: 5px 0 0 0; font-size: 11px; opacity: 0.7;">Version 2.5</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.selected_mode == "user":
        user_survey(df)
    
    else:
        if 'admin_logged_in' not in st.session_state:
            st.session_state.admin_logged_in = False
        
        if not st.session_state.admin_logged_in:
            st.markdown("""
            <div class="welcome-banner">
                <h1>🔐 Admin Login</h1>
                <p style="font-size: 18px; opacity: 0.95;">Akses Dashboard Analytics</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 500px; margin: 0 auto;'>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="font-size: 60px; margin-bottom: 10px;">🔒</div>
                <h3 style="color: #667eea; margin: 0;">Masukkan Kredensial Admin</h3>
            </div>
            """, unsafe_allow_html=True)
            
            password = st.text_input("Password Admin:", type="password", placeholder="••••••••")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🚀 Login", use_container_width=True):
                    if password == ADMIN_PASSWORD:
                        st.session_state.admin_logged_in = True
                        st.success("✅ Login berhasil!")
                        st.rerun()
                    else:
                        st.error("❌ Password salah!")
            
            with col2:
                if st.button("⬅️ Kembali", use_container_width=True):
                    st.session_state.selected_mode = "user"
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align: center; margin-top: 30px; padding: 20px; background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-radius: 15px;">
                <p style="color: #666; margin: 0;">💡 <b>Hint:</b> Default password adalah <code>admin123</code></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown("""
                <div style="padding: 10px 0;">
                    <h2 style="margin: 0; color: #667eea;">👨‍💼 Admin Dashboard</h2>
                    <p style="margin: 5px 0 0 0; color: #999;">Selamat datang, Administrator</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🚪 Logout", use_container_width=True):
                    st.session_state.admin_logged_in = False
                    st.session_state.selected_mode = "user"
                    st.rerun()
            
            admin_dashboard()

if __name__ == "__main__":
    main()