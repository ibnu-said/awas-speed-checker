import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="AWAS Speed Checker", page_icon="🚗")

st.title("🚨 Sistem AWAS: Point-to-Point Speed Checker")
st.markdown("""
Sistem ini mengira kelajuan purata antara dua tol dan memberi amaran jika anda melebihi had laju.Ia juga mencadangkan masa rehat untuk elak daripada disaman.
""")

# Input pengguna
jarak_km = st.number_input("Jarak antara dua tol (km)", min_value=1.0, value=100.0, step=1.0)
masa_masuk = st.time_input("Masa masuk tol", value=datetime.strptime("13:00", "%H:%M").time())
masa_keluar = st.time_input("Masa keluar tol", value=datetime.strptime("13:30", "%H:%M").time())
had_laju = st.number_input("Had laju yang dibenarkan (km/j)", min_value=1, value=110, step=1)

# Butang kira
if st.button("Kira"):
    now = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    dt_masuk = now.replace(hour=masa_masuk.hour, minute=masa_masuk.minute)
    dt_keluar = now.replace(hour=masa_keluar.hour, minute=masa_keluar.minute)
    if dt_keluar < dt_masuk:
        dt_keluar += timedelta(days=1)

    tempoh_minit = (dt_keluar - dt_masuk).total_seconds() / 60
    tempoh_jam = tempoh_minit / 60
    kelajuan_purata = jarak_km / tempoh_jam

    masa_min_diperlukan_jam = jarak_km / had_laju
    masa_min_diperlukan = timedelta(hours=masa_min_diperlukan_jam)
    masa_ideal_keluar = dt_masuk + masa_min_diperlukan

    st.markdown("### 📊 Keputusan")
    st.write(f"⏱️ **Tempoh perjalanan:** {tempoh_minit:.1f} minit")
    st.write(f"🚗 **Kelajuan purata:** {kelajuan_purata:.1f} km/j")

    if kelajuan_purata > had_laju:
        beza_masa = masa_ideal_keluar - dt_keluar
        rehat_minit = abs(beza_masa).seconds // 60
        st.error("⚠️ Anda telah melebihi had laju.")
        st.info(f"💡 Berehat sekurang-kurangnya **{rehat_minit} minit** sebelum keluar tol.")
        st.write(f"🕓 Masa minimum keluar tol: **{masa_ideal_keluar.strftime('%H:%M')}**")
    else:
        st.success("✅ Anda mematuhi had laju yang ditetapkan.")
