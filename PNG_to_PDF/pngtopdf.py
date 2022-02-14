# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from PIL import Image


def jpg_to_pdf(jpg, pdf_path):
    (w, h) = Image.open(jpg).size
    user = canvas.Canvas(pdf_path, pagesize=portrait((w, h)))
    user.drawImage(jpg, 0, 0, w, h)
    user.showPage()
    user.save()




if __name__ == '__main__':
    jpg_path = r"E:\MyProject\scrapeTest\PNG_to_PDF\JL.png"
    pdf_path = r"E:\MyProject\scrapeTest\PNG_to_PDF\JL.pdf"
    jpg_to_pdf(jpg_path, pdf_path)
