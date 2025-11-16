import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df_eco = pd.read_csv("data/ekonomi_bps.csv")
    df_pol = pd.read_csv("data/political_survey.csv")
    df_merged = pd.read_csv("data/gabungan.csv")
    return df_eco, df_pol, df_merged

df_eco, df_pol, df_merged = load_data()

st.set_page_config(page_title="Dashboard Ekonomi & Politik", layout="wide")

# ======================
# TITLE
# ======================
st.title("📈 Dashboard Ekonomi & Politik Provinsi (Demo)")

st.markdown(
    """
    Dashboard ini menampilkan:
    - **Trust Government** dan **Political Participation Index**  
    - Analisis Data Ekonomi.
    - Analisis Data Politik.
    - Dibedakan berdasarkan **tahun** (2023 dan 2024)  
    """
)

# ========== SIDEBAR: PILIH DATASET ==========
st.sidebar.title("Pengaturan Dashboard:")
dataset_choice = st.sidebar.selectbox(
    "Pilih dataset",
    ["Data Gabungan", "Data Ekonomi", "Data Politik"]
)

if dataset_choice == "Data Gabungan":
    df = df_merged
elif dataset_choice == "Data Ekonomi":
    df = df_eco
elif dataset_choice == "Data Politik":
    df = df_pol

st.write(f"Dataset yang dipakai: **{dataset_choice}**")
st.dataframe(df.head())

# ======================
# SIDEBAR
# ======================
tahun_list = sorted(df["tahun"].unique()) if "tahun" in df.columns else []
prov_list = sorted(df["provinsi"].unique()) if "provinsi" in df.columns else []

if tahun_list:
    tahun_filter = st.sidebar.selectbox(
        "Pilih tahun (untuk beberapa grafik):",
        options = ['Semua'] + list(map(int, tahun_list))
    )
else:
    tahun_filter = "Semua"

#if prov_list: (karena time series tidak diperlukan)
 #   prov_selected = st.sidebar.selectbox(
  #      "Pilih provinsi untuk analisis:",
   #     prov_list
    #)
#else:
#    prov_selected = None
# (karena time series tidak diperlukan)

st.sidebar.markdown("---")
st.sidebar.write("Shape Dataset:")
st.sidebar.write("Dataset ekonomi:", df_eco.shape)
st.sidebar.write("Dataset politik:", df_pol.shape)
st.sidebar.write("Dataset gabungan:", df_merged.shape)


#st.write(f"Dataset Aktif: **{dataset_choice}**")
#st.write("Preview Data")
#st.dataframe(df.head())

# ======================
# VISUALISASI
# ======================

def filter_by_year(dataframe):
    if "tahun" not in dataframe.columns:
        return dataframe
    if tahun_filter == "Semua":
        return dataframe
    return dataframe[dataframe["tahun"] == tahun_filter]

def show_data_gabungan(df):
    st.markdown("## Analisis Data Gabungan (Ekonomi + Politik)")
    df_use = df.copy()

    #---------------------- Bar: Trust & Pariticipation per provinsi -----------------------
    st.markdown("### Trust Government & Political Paticipation per Provinsi")
    pol_long = df_pol.melt(
        id_vars=["tahun", "provinsi"],
        value_vars=["trust_government", "political_participation_index"],
        var_name="indikator",
        value_name="nilai",
    )
    if tahun_filter == "Semua":
    # facet: panel terpisah untuk 2023 & 2024
        fig_pol = px.bar(
            pol_long,
            x="provinsi",
            y="nilai",
            color="indikator",
            barmode="group",
            facet_col="tahun",
            title="Trust Government & Political Participation per Provinsi",
        )
    else:
    # filter 1 tahun saja
        pol_year = pol_long[pol_long["tahun"] == tahun_filter]

        fig_pol = px.bar(
            pol_year,
            x="provinsi",
            y="nilai",
            color="indikator",
            barmode="group",
            text="nilai",
            title=(f"Trust Government & Political Participation per Provinsi - Tahun ({tahun_filter})"),
        )
        fig_pol.update_traces(textposition="outside")

    fig_pol.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_pol, use_container_width=True)

# ======================
# PLOT TAMBAHAN: GDP & PENGANGGURAN
# ======================
    st.subheader("Ringkasan Ekonomi per Provinsi")

    col1, col2 = st.columns(2)

    with col1:
        if {"gdp_per_capita", "provinsi"}.issubset(df_use.columns):
            df_eco_plot = filter_by_year(df_use)
            fig_gdp = px.bar(
                df_eco_plot,
                x="provinsi",
                y="gdp_per_capita",
                color="tahun",
                barmode="group",
                title="GDP per Capita per Provinsi",
            )
            fig_gdp.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_gdp, use_container_width=True)
        else:
            st.info("Kolom 'gdp_per_capita' tidak ditemukan di data gabungan.")

    with col2:
        if {"tingkat_pengangguran", "provinsi"}.issubset(df_use.columns):
            df_unem_plot = filter_by_year(df_use)
            fig_unemp = px.bar(
                df_unem_plot,
                x="provinsi",
                y="tingkat_pengangguran",
                color="tahun",
                barmode="group",
                title="Tingkat Pengangguran per Provinsi",
            )
            fig_unemp.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_unemp, use_container_width=True)

    # ---------------------- Time Series -----------------------------
    # Data hanya terdapat 2 tahun saja.
    #if prov_selected is not None:
        #st.markdown(f"### Time Series - {prov_selected}")
        #df_prov = df_use[df_use["provinsi"] == prov_selected].copy()

        # Politik
        #if {"trust_government", "political_participation_index"}.issubset(df_prov.columns):
            #pol_ts_long = df_pol.melt(
            #   id_vars=["tahun", "provinsi"],
            #   value_vars=["trust_government", "political_participation_index"],
            #   var_name="indikator",
            #   value_name="nilai",
            #)
            #fig_ts_pol = px.line(
            #   pol_ts_long,
            #   x="tahun",
            #   y="nilai",
            #   color="indikator",
            #   markers=True,
            #   title=f"Perkembangan Indikator Politik - {prov_selected}"
            #)
            #fig_ts_pol.update_layout(xaxis=dict(dtick=1))
            #st.plotly_chart(fig_ts_pol, use_container_width=True)

        # Ekonomi
        #eco_cols = [c for c in ["gdp_per_capita", "tingkat_pengangguran", "inflasi"] if c in df_prov.columns]
        #if eco_cols:
            #   eco_ts_long = df_prov.melt(
            #   id_vars=["tahun", "provinsi"],
            #   value_vars=["gdp_per_capita", "tingkat_pengangguran", "inflasi"],
            #   var_name="indikator",
            #   value_name="nilai",
            #)
            #fig_ts_eco = px.line(
            #   eco_ts_long,
            #   x="tahun",
            #   y="nilai",
            #   color="indikator",
            #   markers=True,
            #   title=f"Perkembangan Indikator Ekonomi - {prov_selected}"
            #)
            #fig_ts_eco.update_layout(xaxis=dict(dtick=1))
            #st.plotly_chart(fig_ts_eco, use_container_width=True)

def show_data_ekonomi(df):
    st.markdown("## Analisis Data Ekonomi")
    df_use = filter_by_year(df)

    if not {"provinsi", "gdp_per_capita"}.issubset(df_use.columns):
        st.warning("Kolom 'provinsi' atau 'gdp_per_capita' tidak ditemukan.")
        return

    col1, col2 = st.columns(2)

    with col1:
        fig_gdp = px.bar(
            df_use,
            x="provinsi",
            y="gdp_per_capita",
            color="tahun" if "tahun" in df_use.columns else None,
            barmode="group",
            title="GDP per Capita per Provinsi."
        )
        fig_gdp.update_layout(xaxis_tickangle=-20)
        st.plotly_chart(fig_gdp, use_container_width=True)

    with col2:
        if "tingkat_pengangguran" in df_use.columns:
            fig_unemp = px.bar(
                df_use,
                x="provinsi",
                y="tingkat_pengangguran",
                color="tahun" if "tahun" in df_use.columns else None,
                barmode="group",
                title="Tingkat Pengangguran per Provinsi"
            )
            fig_unemp.update_layout(xaxis_tickangle=-20)
            st.plotly_chart(fig_unemp, use_container_width=True)

def show_data_politik(df):
    st.markdown("## Analisis Data Politik")
    df_use = filter_by_year(df)
    if not {"provinsi", "trust_government"}.issubset(df_use.columns):
        st.warning("Kolom 'provinsi' atau 'trust_government' tidak ditemukan.")
        return

    fig_trust = px.bar(
        df_use,
        x="provinsi",
        y="trust_government",
        color="tahun" if "tahun" in df_use.columns else None,
        barmode="group",
        title="Trust Government per Provinsi"
    )
    fig_trust.update_layout(xaxis_tickangle=-20)
    st.plotly_chart(fig_trust, use_container_width=True)

# =========================
# ROUTING BERDASARKAN PILIHAN DATASET
# =========================
if dataset_choice == "Data Gabungan":
    show_data_gabungan(df)
elif dataset_choice == "Data Ekonomi":
    show_data_ekonomi(df)
else:
    show_data_politik(df)

# =========================
# FOOTNOTE
# =========================
st.markdown("---")
st.caption("Catatan: dashboard ini hanya untuk latihan dan project sederhana. "
           "\n [Dinar W. Rahman](https://www.linkedin.com/in/dinar-wahyu-rahman)")
