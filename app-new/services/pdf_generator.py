import os
from fpdf import FPDF

from babel.dates import format_date

class KoperasiPDF(FPDF):
    def header(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

        font_dir = os.path.join(project_root, "static", "font")
        self.add_font(
            "Rockwell",
            "",
            os.path.join(font_dir, "Rockwell.ttf")
        )
        # self.add_font(
        #     "Rockwell",
        #     "B",
        #     os.path.join(font_dir, "Rockwell-Bold.ttf")
        # )

        ub_logo_path = os.path.join(project_root, "static", "img", "logo_1.png")
        koperasi_logo_path = os.path.join(project_root, "static", "img", "logo-koperasi-indonesia.png")
        
        # --- RENDER LOGO (Kiri & Kanan) ---
        # Logo Kiri: Margin kiri 15mm, tinggi Y=10mm, lebar logo=18mm
        self.image(koperasi_logo_path, x=15, y=10, w=18)
        
        # Logo Kanan: Lebar kertas A4 (210mm) - margin kanan (15mm) - lebar logo (18mm) = 177mm
        self.image(ub_logo_path, x=170, y=12, w=25)
        
        # --- JUDUL KOP SURAT ---
        self.set_font("Rockwell", "", 14)
        self.cell(0, 6, "KOPERASI", ln=True, align="C")
        self.cell(0, 6, "UB MANDIRI SEJAHTERA", ln=True, align="C")
        self.set_font("Arial", "", 9)
        self.cell(0, 5, "Jl. Lodaya Ujung No 09 RT 03, RW 07, Kel. Babakan, Bogor", ln=True, align="C")

        # --- GARIS PEMBATAS DOUBLE ---
        self.ln(2)
        self.line(10, self.get_y(), 200, self.get_y())
        self.line(10, self.get_y() + 0.8, 200, self.get_y() + 0.8)
        self.ln(5)

def generate_member_pdf(user_data):
    pdf = KoperasiPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)
    
    pdf.set_font("Arial", "BU", 12)
    pdf.cell(0, 10, "SURAT PERMOHONAN MENJADI ANGGOTA", ln=True, align="C")
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, "Yang bertanda tangan dibawah ini:", ln=True)
    pdf.ln(2)
    
    # Data dinamis yang diambil dari database/user_data
    data_pemohon = [
        ("Nama Lengkap", user_data.full_name),
        ("Tempat Lahir", user_data.birth_place),
        ("Tanggal Lahir", format_date(user_data.birth_date, format='d MMMM yyyy', locale='id') if user_data.birth_date else "-"),
        ("Jenis Kelamin", user_data.gender),
        ("Alamat Rumah", user_data.address),
        ("Nomor Kartu Keluarga", user_data.family_card_number),
        ("Nomor KTP", user_data.identity_number),
        ("No Telp / HP", user_data.phone_number),
        ("Pekerjaan", user_data.job or "-"),
        ("Nama Suami / Istri", user_data.spouse_name or "-"),
        ("Kelompok", user_data.dkm_group.value or "-")
    ]
    
    col1_width, col2_width, col3_width = 45, 5, 130
    for label, value in data_pemohon:
        pdf.set_font("Arial", "", 10)
        pdf.cell(col1_width, 6, label)
        pdf.cell(col2_width, 6, ":")
        pdf.multi_cell(col3_width, 6, str(value))
        pdf.set_y(pdf.get_y() + 0.3)
        
    pdf.ln(4)
    pdf.multi_cell(0, 5, 'Dengan ini mengajukan permohonan masuk menjadi anggota Koperasi "UB Mandiri Sejahtera" dan bersedia memenuhi ketentuan-ketentuan dan persyaratan yang ada yaitu:')
    pdf.ln(2)
    
    persyaratan = [
        "1. Siap mempraktekan sifat 6 Thobiat Luhur\n   (\"Jujur, Amanah, Rukun, Kompak, Kerjasama yang baik, Hemat\")",
        "2. Mentaati Anggaran Dasar dan Anggaran Rumah Tangga (AD-ART) Koperasi UB Mandiri Sejahtera",
        "3. Mentaati segala peraturan yang berlaku di Koperasi UB Mandiri Sejahtera",
        "4. Setoran Simpanan Pokok, Simpanan Wajib dan Simpanan Sukarela berakad Mudharabah (Akad Modal Kerja)",
        "5. Bersedia Menyetorkan Simpanan Pokok sebesar Rp. 100.000,- (Bisa dicicil 2 kali)",
        f"6. Bersedia menyetorkan Simpanan Wajib sebesar Rp. {user_data.mandatory_savings.value} setiap Bulan",
        "7. Melampirkan Fotocopy Kartu Keluarga dan Fotocopy KTP",
        "8. Melampirkan Foto diri ukuran 3x4 berwarna"
    ]
    for poin in persyaratan:
        pdf.multi_cell(0, 5, poin)
        pdf.set_y(pdf.get_y() + 0.8)
        
    pdf.ln(4)
    pdf.multi_cell(0, 5, "Demikian permohonan ini dibuat, untuk menjadi bahan pertimbangan bagi Pengurus. Atas perhatiannya disampaikan terima kasih.")
    pdf.ln(2)
    
    # Simpan posisi awal koordinat Y
    pos_y_ttd = pdf.get_y()

    # =========================================================================
    # BAGIAN ATAS (Kanan: Bogor, Pemohon, Space TTD, Nama Pemohon)
    # =========================================================================
    pdf.set_xy(120, pos_y_ttd)
    pdf.cell(75, 5, f"Bogor, {user_data.submitted_at.strftime('%d-%m-%Y')}", ln=True, align="C")

    pdf.set_x(120)
    pdf.cell(75, 5, "Pemohon", ln=True, align="C")

    pdf.ln(13)  # Space untuk tanda tangan pemohon

    pdf.set_x(120)
    pdf.cell(75, 5, f"( {user_data.full_name} )", ln=True, align="C")


    # =========================================================================
    # BAGIAN TENGAH (Kiri: Disetujui & Tanggal)
    # =========================================================================
    pos_y_tengah = pdf.get_y()

    pdf.set_xy(15, pos_y_tengah - 5)
    pdf.cell(80, 5, "Disetujui :", ln=True)

    pdf.set_x(15)
    pdf.cell(80, 5, f"Tanggal : {user_data.approved_at.strftime('%d-%m-%Y')}", ln=True)

    pdf.set_x(15)
    pdf.cell(80, 5, "Ketua", ln=True, align="C")


    # =========================================================================
    # BAGIAN BAWAIH (Kiri: Space TTD + Ismail | Kanan: Kotak No Anggota + Pass)
    # =========================================================================
    pdf.ln(15) # Space untuk tanda tangan pengurus
    pos_y_bawah = pdf.get_y()

    # Kanan: Kotak No Anggota & Password berbentuk list ke bawah
    pdf.set_xy(115, pos_y_bawah - 10)
    pdf.cell(30, 6, "No Anggota :", border=0)
    pdf.cell(50, 6, f" {user_data.member_id}", border=1, ln=True)

    pdf.set_x(115)
    pdf.cell(30, 6, "Password :", border=0)
    pdf.cell(50, 6, f" {user_data.temporary_password}", border=1)

    # Kiri: Nama Pengurus
    pdf.set_xy(15, pos_y_bawah + 3) # +3 agar center horizontal dengan kotak kanan
    pdf.cell(80, 5, "( Ismail Jayaperkasa )", align="C")
  
    # Return sebagai bytes (tanpa disimpan ke lokal server)
    return pdf.output()