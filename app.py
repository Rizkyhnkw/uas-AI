import streamlit as st
import pandas as pd
from io import BytesIO
import plotly.graph_objects as go

# ==============================
# Judul Aplikasi
# ==============================
st.title("📦 Penjadwalan Relawan & Truk ke Posko Bencana")
st.write("Solusi alokasi sumber daya dengan **Greedy** atau **Proporsional Allocation**")

# ==============================
# Upload CSV
# ==============================
st.subheader("📂 Upload Data Posko (CSV)")

uploaded_file = st.file_uploader("Unggah file CSV (kolom: nama, relawan, truk)", type="csv")

if uploaded_file:
    df_posko = pd.read_csv(uploaded_file)
else:
    st.info("Contoh data digunakan karena belum ada file diunggah.")
    data_posko = [
        {"nama": "Posko A", "relawan": 10, "truk": 3},
        {"nama": "Posko B", "relawan": 7, "truk": 2},
        {"nama": "Posko C", "relawan": 15, "truk": 4},
        {"nama": "Posko D", "relawan": 8, "truk": 1},
    ]
    df_posko = pd.DataFrame(data_posko)

st.dataframe(df_posko)

# ==============================
# Input sumber daya
# ==============================
st.subheader("🔧 Sumber Daya Tersedia")

total_relawan = st.number_input("Jumlah Total Relawan", min_value=0, value=30)
total_truk = st.number_input("Jumlah Total Truk", min_value=0, value=7)

# ==============================
# Mode Alokasi
# ==============================
st.subheader("⚙️ Pilih Mode Alokasi")
mode = st.radio("Metode Alokasi", ["Greedy", "Proporsional"])

# ==============================
# Proses Alokasi
# ==============================
if st.button("🚀 Proses Alokasi"):
    sisa_relawan = total_relawan
    sisa_truk = total_truk
    hasil = []

    if mode == "Greedy":
        sorted_posko = df_posko.sort_values(by=["relawan", "truk"], ascending=False)
        for _, posko in sorted_posko.iterrows():
            alok_relawan = min(posko["relawan"], sisa_relawan)
            alok_truk = min(posko["truk"], sisa_truk)

            hasil.append({
                "Posko": posko["nama"],
                "Relawan Dibutuhkan": posko["relawan"],
                "Relawan Dialokasikan": alok_relawan,
                "Truk Dibutuhkan": posko["truk"],
                "Truk Dialokasikan": alok_truk,
            })

            sisa_relawan -= alok_relawan
            sisa_truk -= alok_truk

    elif mode == "Proporsional":
        total_kebutuhan_relawan = df_posko["relawan"].sum()
        total_kebutuhan_truk = df_posko["truk"].sum()

        for _, posko in df_posko.iterrows():
            if total_kebutuhan_relawan > 0:
                alok_relawan = round((posko["relawan"] / total_kebutuhan_relawan) * total_relawan)
            else:
                alok_relawan = 0

            if total_kebutuhan_truk > 0:
                alok_truk = round((posko["truk"] / total_kebutuhan_truk) * total_truk)
            else:
                alok_truk = 0

            hasil.append({
                "Posko": posko["nama"],
                "Relawan Dibutuhkan": posko["relawan"],
                "Relawan Dialokasikan": alok_relawan,
                "Truk Dibutuhkan": posko["truk"],
                "Truk Dialokasikan": alok_truk,
            })

    df_hasil = pd.DataFrame(hasil)
    st.success("✅ Alokasi Selesai!")
    st.dataframe(df_hasil)

    # ==============================
    # 📊 Grafik Plotly
    # ==============================
    st.subheader("📊 Grafik Perbandingan Alokasi")

    # Grafik Relawan
    fig_relawan = go.Figure(data=[
        go.Bar(name='Dibutuhkan', x=df_hasil["Posko"], y=df_hasil["Relawan Dibutuhkan"], marker_color='indianred'),
        go.Bar(name='Dialokasikan', x=df_hasil["Posko"], y=df_hasil["Relawan Dialokasikan"], marker_color='lightsalmon')
    ])
    fig_relawan.update_layout(
        barmode='group',
        title='Perbandingan Relawan per Posko',
        xaxis_title='Posko',
        yaxis_title='Jumlah Relawan'
    )
    st.plotly_chart(fig_relawan)

    # Grafik Truk
    fig_truk = go.Figure(data=[
        go.Bar(name='Dibutuhkan', x=df_hasil["Posko"], y=df_hasil["Truk Dibutuhkan"], marker_color='steelblue'),
        go.Bar(name='Dialokasikan', x=df_hasil["Posko"], y=df_hasil["Truk Dialokasikan"], marker_color='lightskyblue')
    ])
    fig_truk.update_layout(
        barmode='group',
        title='Perbandingan Truk per Posko',
        xaxis_title='Posko',
        yaxis_title='Jumlah Truk'
    )
    st.plotly_chart(fig_truk)

    # ==============================
    # Unduh Excel
    # ==============================
    st.subheader("📥 Unduh Hasil Alokasi")

    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Alokasi')
        return output.getvalue()

    excel_data = convert_df_to_excel(df_hasil)

    st.download_button(
        label="⬇️ Download sebagai Excel",
        data=excel_data,
        file_name="hasil_alokasi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
