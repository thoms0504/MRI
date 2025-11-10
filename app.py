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
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Mode Selection Cards */
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
    
    /* Button styling */
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
    
    /* Question box styling */
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
    
    /* Progress bar styling */
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
    
    /* Metric card styling */
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
    
    /* User info box */
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
    
    /* Aspect card */
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
    
    /* Checkbox styling */
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
    
    /* Title styling */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Info box styling */
    .stAlert {
        border-radius: 12px;
        border-left-width: 6px;
    }
    
    /* Legend button */
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
    
    /* Sidebar info box */
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
    
    /* Animation keyframes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated-content {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px;
        padding: 15px 25px;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Welcome banner */
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
    
    /* Data table styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Hide radio button */
    [data-testid="stSidebar"] .stRadio {
        display: none;
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

# ==================== FUNGSI UTILITY ====================

@st.cache_data
def load_data():
    """Load data dari CSV atau gunakan data hardcoded sebagai fallback"""
    try:
        df = pd.read_csv('assets/data/data_mri.csv')
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        data = """Dimensi,Aspek,Arti,Perilaku
Motivation,Aversive,Memiliki pemikiran terdorong untuk berhati-hati dan mampu memitigasi risiko.,Mereka waspada terutama terhadap niat buruk seseorang.
Motivation,Aversive,Memiliki pemikiran terdorong untuk berhati-hati dan mampu memitigasi risiko.,Mampu mengidentifikasi masalah atau resiko sebelum terjadi.
Motivation,Aversive,Memiliki pemikiran terdorong untuk berhati-hati dan mampu memitigasi risiko.,Berpegang pada aturan dan prosedur.
Motivation,Aversive,Memiliki pemikiran terdorong untuk berhati-hati dan mampu memitigasi risiko.,Memperhitungkan setiap risiko dan dampak yang mungkin ditimbulkannya.
Motivation,Collector,Ingin mengetahui lebih banyak baik tentang hal-hal yang menarik atau sebuah informasi,Mencari tahu lebih banyak dan memperbarui informasi.
Motivation,Collector,Ingin mengetahui lebih banyak baik tentang hal-hal yang menarik atau sebuah informasi,Mengumpulkan hal-hal yang menurut mereka menarik karena mereka yakin dapat menggunakannya di kemudian hari.
Motivation,Competitive,Memiliki keinginan kuat untuk bersaing dan menang.,Selalu berusaha menjadi yang terbaik
Motivation,Competitive,Memiliki keinginan kuat untuk bersaing dan menang.,Menikmati pertandingan
Motivation,Directive,Memiliki kecenderungan untuk memimpin mengarahkan dan mengambil kendali.,Secara alami mengambil peran pemimpin dalam kelompok
Motivation,Directive,Memiliki kecenderungan untuk memimpin mengarahkan dan mengambil kendali.,Memberikan instruksi jelas
Relation,Advisor,Berantusias besar untuk berbagi masukan atau nasihat yang bisa membantu orang tersebut mengatasi masalahnya,Secara spontan memberi nasihat dalam berbagai situasi.
Relation,Advisor,Berantusias besar untuk berbagi masukan atau nasihat yang bisa membantu orang tersebut mengatasi masalahnya,Mengesampingkan diri untuk membantu orang lain menghadapi rintangannya.
Relation,Affectionate,Menunjukkan kasih sayang kehangatan dan kepedulian secara terbuka.,Sering memberikan pujian
Relation,Affectionate,Menunjukkan kasih sayang kehangatan dan kepedulian secara terbuka.,Sentuhan fisik seperti pelukan
Relation,Caring,Sangat peka terhadap keinginan dan kebutuhan orang lain yang mungkin tidak terekspresikan,Terhubung secara mendalam dengan kondisi emosi diri dan orang lain.
Relation,Caring,Sangat peka terhadap keinginan dan kebutuhan orang lain yang mungkin tidak terekspresikan,Selalu menunjukkan kepekaan dan empati yang tinggi terhadap perasaan orang lain.
Impact,Accountable,Dapat diandalkan dan selalu mengemban amanah untuk mencapai tujuan,Mengemban tanggung jawab dan memastikan semua komitmen terpenuhi.
Impact,Accountable,Dapat diandalkan dan selalu mengemban amanah untuk mencapai tujuan,Dapat diandalkan untuk memastikan tugas-tugas diselesaikan.
Impact,Decisive,Mampu mengambil keputusan dengan cepat tepat dan tanpa ragu.,Tidak menunda-nunda keputusan penting
Impact,Decisive,Mampu mengambil keputusan dengan cepat tepat dan tanpa ragu.,Bertindak cepat saat dibutuhkan
Impact,Flexible,Bersedia memodifikasi pendekatan mereka sesuai situasi atau kondisi yang ada,Siap menyesuaikan diri dan menerima perubahan ketika terjadi.
Impact,Flexible,Bersedia memodifikasi pendekatan mereka sesuai situasi atau kondisi yang ada,Tetap tenang ketika ada perubahan yang bersifat tiba-tiba karena mereka percaya bahwa perubahan adalah sesuatu yang akan selalu terjadi."""
        
        from io import StringIO
        df = pd.read_csv(StringIO(data))
        return df

def create_questions(df, num_questions=60):
    """Buat soal dari data dengan randomisasi"""
    questions = []
    grouped = df.groupby(['Dimensi', 'Aspek', 'Arti'])['Perilaku'].apply(list).reset_index()
    
    question_count = 0
    while question_count < num_questions and len(grouped) > 0:
        idx = random.randint(0, len(grouped) - 1)
        row = grouped.iloc[idx]
        
        all_behaviors = row['Perilaku']
        if len(all_behaviors) >= 6:
            selected_behaviors = random.sample(all_behaviors, 6)
        else:
            selected_behaviors = all_behaviors.copy()
            other_behaviors = df[df['Aspek'] != row['Aspek']]['Perilaku'].tolist()
            additional = random.sample(other_behaviors, min(6 - len(selected_behaviors), len(other_behaviors)))
            selected_behaviors.extend(additional)
            selected_behaviors = selected_behaviors[:6]
        
        questions.append({
            'dimensi': row['Dimensi'],
            'aspek': row['Aspek'],
            'arti': row['Arti'],
            'behaviors': selected_behaviors,
            'original_order': list(range(6))
        })
        
        question_count += 1
    
    random.shuffle(questions)
    
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

def save_results(username_bps, nama, nip, top_10, bottom_5):
    """Simpan hasil survey ke CSV"""
    result_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'username_bps': username_bps,
        'nama': nama,
        'nip': nip,
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
    return pd.DataFrame(columns=['timestamp', 'username_bps', 'nama', 'nip', 'top_10', 'bottom_5'])

# ==================== TAMPILAN HASIL USER ====================

def display_results(aspect_scores, aspect_dimensions, user_data=None):
    """Tampilkan hasil top 10 dan bottom 5"""
    
    # Animated welcome banner
    st.markdown("""
    <div class="welcome-banner animated-content">
        <h1>🎉 Selamat! Survey Anda Telah Selesai</h1>
        <p style="font-size: 18px; opacity: 0.95;">Berikut adalah hasil analisis kepribadian MRI Anda</p>
    </div>
    """, unsafe_allow_html=True)
    
    if user_data:
        st.markdown(f"""
        <div class="user-info-box animated-content">
            <h3>👤 Informasi Peserta</h3>
            <p style="margin: 5px 0;"><b>Username BPS:</b> {user_data['username_bps']}</p>
            <p style="margin: 5px 0;"><b>Nama:</b> {user_data['nama']}</p>
            <p style="margin: 5px 0;"><b>NIP:</b> {user_data['nip']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    sorted_aspects = sorted(aspect_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Top 10
    st.markdown("<div class='animated-content'>", unsafe_allow_html=True)
    st.header("🏆 Top 10 Aspek Dominan Anda")
    st.markdown("</div>", unsafe_allow_html=True)
    
    top_10 = sorted_aspects[:10]
    
    # Chart dengan animasi
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
    
    # Cards untuk top 10
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
    
    # Bottom 5
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
    
    # Cards untuk bottom 5
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
    
    # Legend dengan styling lebih menarik
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎨 Legenda Dimensi")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='legend-button' style='background: linear-gradient(135deg, {DIMENSION_COLORS['Motivation']} 0%, {DIMENSION_COLORS['Motivation']}dd 100%);'>🎯 Motivation</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='legend-button' style='background: linear-gradient(135deg, {DIMENSION_COLORS['Relation']} 0%, {DIMENSION_COLORS['Relation']}dd 100%);'>🤝 Relation</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='legend-button' style='background: linear-gradient(135deg, {DIMENSION_COLORS['Impact']} 0%, {DIMENSION_COLORS['Impact']}dd 100%);'>⚡ Impact</div>", unsafe_allow_html=True)
    
    # Return data untuk disimpan
    top_10_data = [{'aspek': aspect, 'skor': score, 'dimensi': aspect_dimensions.get(aspect, 'Unknown')} for aspect, score in top_10]
    bottom_5_data = [{'aspek': aspect, 'skor': score, 'dimensi': aspect_dimensions.get(aspect, 'Unknown')} for aspect, score in bottom_5]
    
    return top_10_data, bottom_5_data

# ==================== DASHBOARD ADMIN ====================

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
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Ranking Aspek",
        "🏆 Top 10 Populer",
        "📉 Bottom 5 Populer",
        "👥 Data Peserta",
        "📈 Analisis Dimensi"
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

# ==================== FORM INPUT DATA DIRI ====================

def user_data_form():
    """Form untuk input data diri user sebelum mengerjakan survey"""
    st.markdown("""
    <div class="welcome-banner">
        <h1>📝 Selamat Datang di MRI Survey</h1>
        <p style="font-size: 18px; opacity: 0.95;">Silakan isi data diri Anda untuk memulai</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
    """, unsafe_allow_html=True)
    
    with st.form("user_data_form"):
        st.markdown("### 👤 Informasi Peserta")
        username_bps = st.text_input("Username BPS *", placeholder="Contoh: thomson")
        nama = st.text_input("Nama Lengkap *", placeholder="Contoh: Thomson")
        nip = st.text_input("NIP *", placeholder="Contoh: 200104052024121001")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✅ Mulai Survey", use_container_width=True)
        
        if submitted:
            if not username_bps or not nama or not nip:
                st.error("❌ Semua field harus diisi!")
                return None
            
            if not nip.isdigit():
                st.error("❌ NIP harus berupa angka!")
                return None
            
            return {
                'username_bps': username_bps.strip(),
                'nama': nama.strip(),
                'nip': nip.strip()
            }
    
    st.markdown("</div>", unsafe_allow_html=True)
    return None

# ==================== SURVEY USER ====================

def user_survey(df):
    """Survey untuk user"""
    
    if 'survey_initialized' not in st.session_state:
        st.session_state.survey_initialized = True
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.questions = None
        st.session_state.completed = False
        st.session_state.user_data = None
    
    if st.session_state.user_data is None:
        user_data = user_data_form()
        if user_data:
            st.session_state.user_data = user_data
            st.rerun()
        return
    
    if st.session_state.questions is None:
        st.session_state.questions = create_questions(df, num_questions=60)
    
    questions = st.session_state.questions
    
    if st.session_state.completed:
        aspect_scores, aspect_dimensions = calculate_results(st.session_state.answers, questions)
        top_10_data, bottom_5_data = display_results(aspect_scores, aspect_dimensions, st.session_state.user_data)
        
        if 'result_saved' not in st.session_state:
            save_results(
                st.session_state.user_data['username_bps'],
                st.session_state.user_data['nama'],
                st.session_state.user_data['nip'],
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
    
    # Header dengan styling menarik
    st.markdown("""
    <div class="welcome-banner">
        <h1>🧠 Survey MRI Pegawai BPS Provinsi Lampung</h1>
        <p style="font-size: 18px; opacity: 0.95;">Temukan Profil Kepribadian Anda</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); margin-bottom: 20px;">
        <h3 style="margin: 0; color: #667eea;">Selamat datang, <span style="color: #764ba2;">{st.session_state.user_data['nama']}</span>! 👋</h3>
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
    
    dimension_color = DIMENSION_COLORS.get(question['dimensi'], '#gray')
    
    st.markdown(f"""
    <div class="question-box" style="border-top: 5px solid {dimension_color};">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background: {dimension_color}; color: white; padding: 8px 15px; border-radius: 8px; font-weight: 600; margin-right: 15px;">
                {question['dimensi']}
            </div>
            <h3 style="margin: 0; color: {dimension_color};">{question['aspek']}</h3>
        </div>
        <h4 style="color: #333; margin: 15px 0;">{question['arti']}</h4>
        <p style="color: #666; font-style: italic; background: #f8f9ff; padding: 10px; border-radius: 8px; border-left: 3px solid {dimension_color};">
            💡 <b>Instruksi:</b> Pilih <b>3 pernyataan</b> yang paling menggambarkan Anda
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Opsi jawaban
    selected_options = []
    
    for idx, behavior in enumerate(question['behaviors']):
        is_selected = st.checkbox(
            behavior,
            key=f"q_{current_q_idx}_opt_{idx}",
            value=idx in st.session_state.answers.get(current_q_idx, [])
        )
        if is_selected:
            selected_options.append(idx)
    
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

# ==================== MAIN APP ====================

def main():
    df = load_data()
    
    # Initialize mode state
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
        
        # Mode User Card
        user_active = "active" if st.session_state.selected_mode == "user" else ""
        st.markdown(f"""
        <div class="mode-card {user_active}" id="user-card">
            <div class="mode-icon">👤</div>
            <h3>User Mode</h3>
            <p>Kerjakan survey kepribadian MRI</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Pilih User Mode", key="btn_user", use_container_width=True):
            st.session_state.selected_mode = "user"
            st.rerun()
        
        st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)
        
        # Mode Admin Card
        admin_active = "active" if st.session_state.selected_mode == "admin" else ""
        st.markdown(f"""
        <div class="mode-card {admin_active}" id="admin-card">
            <div class="mode-icon">🔐</div>
            <h3>Admin Mode</h3>
            <p>Akses dashboard dan analytics</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Pilih Admin Mode", key="btn_admin", use_container_width=True):
            st.session_state.selected_mode = "admin"
            st.rerun()
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.3); margin: 20px 0;'>", unsafe_allow_html=True)
        
        # Informasi Section
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
                <li>60 pertanyaan interaktif</li>
                <li>Pilih 3 dari 6 opsi</li>
                <li>Hasil analisis real-time</li>
                <li>Dashboard admin lengkap</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 12px; border-radius: 8px; text-align: center; margin-top: 20px;">
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">© 2024 MRI Survey System</p>
            <p style="margin: 5px 0 0 0; font-size: 11px; opacity: 0.7;">Version 2.0</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content based on selected mode
    if st.session_state.selected_mode == "user":
        user_survey(df)
    
    else:  # admin mode
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
            # Admin Dashboard Header
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