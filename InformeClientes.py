
from reportlab.pdfgen import canvas

def informeCliente(clien):

    informe=canvas.Canvas("InformedoCliente"+clien[0][0]+".pdf")

    estiloTexto=informe.beginText()
    estiloTexto.setFont("Times-Bold", 16)
    estiloTexto.setTextOrigin(100,800)



    cadena="Informe sobre la información basica del cliente con DNI: "+clien[0][0]+"."

    estiloTexto.textLines(cadena)
    estiloTexto.moveCursor(10, 50)

    estiloTexto.setFont("Times-Roman",12)

    guion = ["Cliente: " + clien[0][1] +" "+clien[0][2]+", con un/a "+clien[0][3]+" de la marca "+clien[0][4],
             "con matricula "+clien[0][6]+" y año de fabricacion en "+clien[0][7]+" y numero de contacto "+clien[0][5]+"."]



    for linha in guion:
        estiloTexto.textOut(linha)
        estiloTexto.moveCursor(0,15)

    estiloTexto.setFillGray(0.5)
    informe.drawText(estiloTexto)
    informe.showPage()
    informe.save()



