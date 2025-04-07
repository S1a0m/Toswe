from reportlab.pdfgen import canvas
from io import BytesIO
from fastapi.responses import StreamingResponse

def generate_order_pdf(order):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    
    pdf.drawString(100, 800, f"Commande #{order.id_order}")
    pdf.drawString(100, 780, f"Client : {order.client_name}")
    
    y = 760
    for item in order.items:
        pdf.drawString(100, y, f"- {item.name} x {item.quantity} → {item.total_price} FCFA")
        y -= 20

    pdf.drawString(100, y - 20, f"Total : {order.total} FCFA")
    pdf.save()

    buffer.seek(0)
    return StreamingResponse(buffer, media_type='application/pdf', headers={
        "Content-Disposition": f"inline; filename=commande_{order.id_order}.pdf"
    })
