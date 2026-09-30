import streamlit as st
st.image("TCTT.jpg")
# ==============================
# CẤU HÌNH ỨNG DỤNG
# ==============================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.caption("Tính toán tiền lãi theo phương pháp lãi đơn và lãi kép")

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def format_money(value):
    return f"{value:,.0f}".replace(",", ".") + " VNĐ"


# ==============================
# NHẬP THÔNG TIN
# ==============================
st.subheader("📋 Thông tin khoản gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=360,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1
)

phuong_phap = st.selectbox(
    "Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_nhan = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)


# ==============================
# NÚT TÍNH TOÁN
# ==============================
if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")

    elif lai_suat < 0:
        st.error("Lãi suất không hợp lệ.")

    else:

        # Chuyển lãi suất từ % sang số thập phân
        r = lai_suat / 100

        # Số năm gửi
        so_nam = ky_han / 12

        # ==============================
        # TRƯỜNG HỢP LÃI ĐƠN
        # ==============================
        if phuong_phap == "Lãi đơn":

            # Tổng tiền lãi
            tong_lai = so_tien * r * so_nam

            # Tổng gốc + lãi
            tong_tien = so_tien + tong_lai

            # Tiền lãi định kỳ
            lai_thang = so_tien * r / 12
            lai_quy = so_tien * r / 4

            if hinh_thuc_nhan == "Lãnh lãi theo tháng":
                lai_dinh_ky = lai_thang

            elif hinh_thuc_nhan == "Lãnh lãi theo quý":
                lai_dinh_ky = lai_quy

            else:
                lai_dinh_ky = tong_lai


        # ==============================
        # TRƯỜNG HỢP LÃI KÉP
        # ==============================
        else:

            # Lãi suất tháng
            r_thang = r / 12

            # Công thức lãi kép:
            # A = P * (1 + r)^n
            tong_tien = so_tien * (1 + r_thang) ** ky_han

            # Tổng tiền lãi
            tong_lai = tong_tien - so_tien

            # Lãi tháng đầu tiên
            lai_thang = so_tien * r_thang

            # Lãi trong 1 quý đầu tiên
            tien_sau_3_thang = so_tien * (1 + r_thang) ** 3
            lai_quy = tien_sau_3_thang - so_tien

            if hinh_thuc_nhan == "Lãnh lãi theo tháng":
                lai_dinh_ky = lai_thang

            elif hinh_thuc_nhan == "Lãnh lãi theo quý":
                lai_dinh_ky = lai_quy

            else:
                lai_dinh_ky = tong_lai


        # ==============================
        # HIỂN THỊ KẾT QUẢ
        # ==============================
        st.divider()
        st.subheader("📊 KẾT QUẢ")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="💰 Tiền lãi định kỳ",
                value=format_money(lai_dinh_ky)
            )

        with col2:
            st.metric(
                label="📈 Tổng tiền lãi",
                value=format_money(tong_lai)
            )

        st.success(
            f"💵 **Tổng số tiền gốc và lãi: {format_money(tong_tien)}**"
        )


        # ==============================
        # CHI TIẾT KHOẢN GỬI
        # ==============================
        st.divider()
        st.subheader("📝 Chi tiết khoản gửi")

        st.write(
            f"**Số tiền gửi:** {format_money(so_tien)}"
        )

        st.write(
            f"**Kỳ hạn:** {ky_han} tháng ({so_nam:.2f} năm)"
        )

        st.write(
            f"**Lãi suất:** {lai_suat:.2f}%/năm"
        )

        st.write(
            f"**Phương pháp:** {phuong_phap}"
        )

        st.write(
            f"**Hình thức nhận lãi:** {hinh_thuc_nhan}"
    )
