# from weasyprint import HTML


# def generate_pdf(html_content: str, output_path: str):
#     HTML(
#         string=html_content,
#         base_url="."
#     ).write_pdf(output_path)

# import os
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import mm
# from pathlib import Path
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont

# def draw_label_value(pdf, y, label, value):
#     pdf.drawString(20 * mm, y, label)
#     pdf.drawString(70 * mm, y, ":")
#     pdf.drawString(75 * mm, y, str(value or ""))


# def generate_member_pdf(member):
#     output_path = f"temp/member_{member.id}.pdf"

#     pdf = canvas.Canvas(
#         output_path,
#         pagesize=A4
#     )

#     width, height = A4

#     # =====================
#     # LOGO
#     # =====================

#     logo_kiri = Path("static/img/logo-koperasi-indonesia.png")
#     logo_kanan = Path("static/img/logo_1.png")

#     pdf.drawImage(
#         str(logo_kiri),
#         10 * mm,
#         height - 35 * mm,
#         width=25 * mm,
#         height=25 * mm,
#         preserveAspectRatio=True
#     )

#     pdf.drawImage(
#         str(logo_kanan),
#         width - 35 * mm,
#         height - 35 * mm,
#         width=25 * mm,
#         height=25 * mm,
#         preserveAspectRatio=True
#     )

#     # =====================
#     # HEADER
#     # =====================

#     pdf.setFont("Helvetica-Bold", 18)

#     pdf.drawCentredString(
#         width / 2,
#         height - 15 * mm,
#         "KOPERASI"
#     )

#     pdf.drawCentredString(
#         width / 2,
#         height - 25 * mm,
#         "UB MANDIRI SEJAHTERA"
#     )

#     pdf.setFont("Helvetica", 11)

#     pdf.drawCentredString(
#         width / 2,
#         height - 33 * mm,
#         "Jl. Lodaya Ujung No 09, RT 03, RW 07 Kel. Babakan Bogor"
#     )

#     # =====================
#     # GARIS KOP SURAT
#     # =====================

#     y_garis = height - 42 * mm

#     # garis tipis bawah
#     pdf.setLineWidth(0.5)
#     pdf.line(
#         10 * mm,
#         y_garis - 2 * mm,
#         width - 10 * mm,
#         y_garis - 2 * mm
#     )

#     # garis tipis bawah
#     pdf.setLineWidth(0.5)
#     pdf.line(
#         10 * mm,
#         y_garis - 2 * mm,
#         width - 10 * mm,
#         y_garis - 2 * mm
#     )

#     # garis tebal
#     pdf.setLineWidth(2)
#     pdf.line(
#         10 * mm,
#         y_garis,
#         width - 10 * mm,
#         y_garis
#     )

#     # =====================
#     # JUDUL SURAT
#     # =====================

#     pdf.setFont("Helvetica-Bold", 13)

#     pdf.drawCentredString(
#         width / 2,
#         height - 58 * mm,
#         "SURAT PERMOHONAN MENJADI ANGGOTA"
#     )

#     # =====================
#     # DATA ANGGOTA
#     # =====================

#     y = height - 75 * mm

#     pdf.setFont("Helvetica", 11)

#     pdf.drawString(
#         20 * mm,
#         y,
#         "Yang bertanda tangan di bawah ini :"
#     )

#     y -= 10 * mm

#     draw_label_value(
#         pdf,
#         y,
#         "Nama Lengkap",
#         member.full_name
#     )

#     y -= 7 * mm

#     draw_label_value(
#         pdf,
#         y,
#         "Tempat Lahir",
#         member.birth_place
#     )

#     y -= 7 * mm

#     draw_label_value(
#         pdf,
#         y,
#         "Tanggal Lahir",
#         member.birth_date.strftime("%d %B %Y")
#     )

#     y -= 7 * mm

#     draw_label_value(
#         pdf,
#         y,
#         "Jenis Kelamin",
#         member.gender
#     )

#     y -= 7 * mm

#     draw_label_value(
#         pdf,
#         y,
#         "Alamat Rumah",
#         member.address
#     )

#     y -= 7 * mm

#     draw_label_value(
#         pdf,
#         y,
#         "Nomor Kartu Keluarga",
#         member.family_card_number
#     )

#     y -= 7 * mm

#     draw_label_value(
#         pdf,
#         y,
#         "Nomor KTP",
#         member.identity_number
#     )

#     y -= 7 * mm

#     draw_label_value(
#         pdf,
#         y,
#         "No Telp / HP",
#         member.phone_number
#     )

#     y -= 7 * mm

#     draw_label_value(
#         pdf,
#         y,
#         "Nama Suami / Istri",
#         member.spouse_name
#     )

#     y -= 7 * mm

#     draw_label_value(
#         pdf,
#         y,
#         "Kelompok",
#         member.dkm_group
#     )

#     # =====================
#     # ISI SURAT
#     # =====================

#     y -= 15 * mm

#     lines = [
#         'Dengan ini mengajukan permohonan masuk menjadi anggota',
#         'Koperasi "UB Mandiri Sejahtera" dan bersedia memenuhi',
#         'dan bersedia memenuhi ketentuan-ketentuan dan persyaratan yang ada, yaitu:'
#     ]

#     for line in lines:
#         pdf.drawString(
#             20 * mm,
#             y,
#             line
#         )
#         y -= 6 * mm

#     y -= 2 * mm

#     rules = [
#         '1. Siap mempraktekan sifat 6 Thobiat Luhur (Jujur, Amanah, Rukun, Kompak, Kerjasama yang baik, Hemat)',
#         '2. Mentaati anggaran dasar dan anggaran rumah tangga (AD/ART) Koperasi UB Mandiri Sejahtera',
#         '3. Mentaati seluruh peraturan yang berlaku di Koperasi UB Mandiri Sejahtera',
#         '4. Setoran simpanan pokok, simpanan wajib dan simpanan sukarela berakad Mudharabah (Akad modal kerja)',
#         '5. Bersedia menyetorkan simpanan pokok sebesar Rp100.000 (Bisa dicicil 2 kali)',
#         '6. Bersedia menyetorkan simpanan wajib setiap bulan sesuai kesanggupan',
#         '7. Melampirkan fotocopy kartu keluarga dan fotocopy KTP',
#         '8. Melampirkan foto diri ukuran 3x4 berwarna'
#     ]

#     for item in rules:
#         pdf.drawString(
#             25 * mm,
#             y,
#             item
#         )
#         y -= 7 * mm

#     lines = [
#         'Demikian permohonan ini dibuat untuk menjadi bahan pertimbangan bagi pengurus.',
#         'Atas perhatiannya disampaikan terima kasih.'
#     ]

#     for line in lines:
#         pdf.drawString(
#             20 * mm,
#             y,
#             line
#         )
#         y -= 6 * mm

#     # =====================
#     # TANDA TANGAN
#     # =====================

#     y -= 15 * mm

#     pdf.drawString(
#         120 * mm,
#         y,
#         "Bogor, ........................."
#     )

#     y -= 10 * mm

#     pdf.drawString(
#         40 * mm,
#         y,
#         "Pemohon"
#     )

#     pdf.drawString(
#         130 * mm,
#         y,
#         "Pengurus"
#     )

#     y -= 30 * mm

#     pdf.drawString(
#         30 * mm,
#         y,
#         f"( {member.full_name} )"
#     )

#     pdf.drawString(
#         120 * mm,
#         y,
#         "( ................................ )"
#     )

#     pdf.save()

#     return output_path