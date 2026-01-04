from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generate_invoice_pdf(data_complex):
    """
    Genereaza PDF detaliat.
    data_complex: Dictionarul returnat de fetch_invoice_details_complex
    """
    if not data_complex: return None
    
    head = data_complex['header']
    piese = data_complex['piese']
    manopera = data_complex['manopera']
    
    # Despachetare Header
    serie = head[1]
    data_em = head[2]
    total_cu_tva = head[5]
    nume_c = head[6] + " " + head[7]
    adresa = head[8]
    cui = head[10]
    masina = f"{head[11]} {head[12]} ({head[13]})"

    filename = f"Factura_{serie}.pdf"
    
    try:
        c = canvas.Canvas(filename, pagesize=A4)
        w, h = A4
        
        # --- HEADER COMPANIE ---
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, h - 50, "SERVICE AUTO MANAGER SRL")
        c.setFont("Helvetica", 10)
        c.drawString(50, h - 70, "Str. Exemplului Nr. 1, Bucuresti")
        c.drawString(50, h - 85, "CUI: RO123456 | Reg.Com: J40/1/2024")
        c.line(50, h - 100, 550, h - 100)

        # --- INFO FACTURA & CLIENT ---
        y_anchor = h - 140
        
        # Stanga: Client
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_anchor, "Beneficiar:")
        c.setFont("Helvetica", 12)
        c.drawString(50, y_anchor - 20, nume_c)
        c.setFont("Helvetica", 10)
        c.drawString(50, y_anchor - 35, f"Adresa: {adresa if adresa else '-'}")
        c.drawString(50, y_anchor - 50, f"Auto: {masina}")
        if cui: c.drawString(50, y_anchor - 65, f"CUI: {cui}")

        # Dreapta: Factura
        c.setFont("Helvetica-Bold", 14)
        c.drawString(350, y_anchor, f"FACTURA: {serie}")
        c.setFont("Helvetica", 12)
        c.drawString(350, y_anchor - 20, f"Data: {data_em}")
        
        # --- TABEL PRODUSE/SERVICII ---
        y = y_anchor - 100
        
        # Cap Tabel
        c.setFillColor(colors.lightgrey)
        c.rect(50, y, 500, 20, fill=1, stroke=0)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y+6, "Denumire Produs / Serviciu")
        c.drawString(300, y+6, "Cant/Ore")
        c.drawString(380, y+6, "Pret Unit.")
        c.drawString(480, y+6, "Total")
        
        y -= 25
        c.setFont("Helvetica", 10)
        
        total_verify = 0
        
        # Iterare Manopera
        if manopera:
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y, ">> MANOPERA")
            c.setFont("Helvetica", 10)
            y -= 15
            for m in manopera:
                den, ore, tarif, total = m
                c.drawString(60, y, str(den))
                c.drawString(310, y, f"{ore} h")
                c.drawString(380, y, str(tarif))
                c.drawString(480, y, str(total))
                y -= 15
                total_verify += float(total)
                
        y -= 5
        
        # Iterare Piese
        if piese:
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y, ">> PIESE SCHIMB")
            c.setFont("Helvetica", 10)
            y -= 15
            for p in piese:
                den, cant, pret, total = p
                c.drawString(60, y, str(den))
                c.drawString(310, y, f"{cant} buc")
                c.drawString(380, y, str(pret))
                c.drawString(480, y, str(total))
                y -= 15
                total_verify += float(total)

        # Linie Total
        y -= 10
        c.setLineWidth(1)
        c.line(50, y, 550, y)
        y -= 25
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(350, y, "TOTAL DE PLATA:")
        c.drawString(480, y, f"{total_cu_tva} RON")
        
        # Footer
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(50, 50, "Factura generata automat din aplicatia Service Auto Manager.")
        
        c.save()
        return filename
        
    except Exception as e:
        print(f"PDF Gen Error: {e}")
        return None