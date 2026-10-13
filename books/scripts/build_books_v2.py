#!/usr/bin/env python3
"""Assemble completed V2 coloring-book art into KDP-ready PDFs."""
from __future__ import annotations
import csv, re
from pathlib import Path
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from pypdf import PdfReader
from PIL import Image
from facts_v2 import fact_for

ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/"books/prompts/manifest-v2.csv"
ART=ROOT/"books/art/interior-v2"
OUT=ROOT/"books/archive/final-kids-v2"
TRIM_W,TRIM_H=8.5*72,11*72
PAGE_COUNT=60
SPINE=PAGE_COUNT*.002252*72
COVER_W,COVER_H=17.25*72+SPINE,11.25*72

def slugify(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")

def image_for(book,page,label):
    p=ART/book/f"page-{int(page):02d}-{slugify(label)}.png"
    if not p.exists():
        matches=list((ART/book).glob(f"page-{int(page):02d}-*.png"))
        if len(matches)==1: return matches[0]
    return p

def fit_image(c,path,x,y,w,h):
    with Image.open(path) as im: iw,ih=im.size
    scale=min(w/iw,h/ih); dw,dh=iw*scale,ih*scale
    c.drawImage(ImageReader(str(path)),x+(w-dw)/2,y+(h-dh)/2,dw,dh,mask='auto')

def build_interior(book,title,rows):
    path=OUT/f"{book}-interior-8.5x11.pdf"; c=canvas.Canvas(str(path),pagesize=(TRIM_W,TRIM_H),pageCompression=1)
    c.setTitle(title); c.setAuthor("Independent Publisher")
    c.setFont("Helvetica-Bold",32); c.drawCentredString(TRIM_W/2,TRIM_H*.64,title.upper())
    c.setFont("Helvetica",16); c.drawCentredString(TRIM_W/2,TRIM_H*.58,"A BIG, EASY COLORING BOOK")
    c.setFont("Helvetica-Bold",12); c.drawCentredString(TRIM_W/2,TRIM_H*.18,"26 NAMED PICTURES AND FUN FACTS FOR AGES 5-9"); c.showPage()
    c.setFont("Helvetica-Bold",17); c.drawString(54,TRIM_H-85,"Copyright and use")
    c.setFont("Helvetica",10); t=c.beginText(54,TRIM_H-115); t.setLeading(16)
    for line in ["Copyright © 2026. All rights reserved.","","For personal use by the purchaser. No part may be reproduced or distributed.","","Artwork was created with generative AI and reviewed, selected, and arranged by the publisher.","Place a protective sheet behind each page when using markers."]: t.textLine(line)
    c.drawText(t); c.showPage()
    c.setFont("Helvetica-Bold",24); c.drawCentredString(TRIM_W/2,TRIM_H*.64,"THIS BOOK BELONGS TO")
    c.setLineWidth(2); c.line(110,TRIM_H*.53,TRIM_W-110,TRIM_H*.53); c.showPage()
    c.setFont("Helvetica-Bold",20); c.drawString(54,TRIM_H-80,"TRY YOUR COLORS")
    c.setFont("Helvetica",11); c.drawString(54,TRIM_H-102,"Test crayons, colored pencils, or markers here.")
    for rr in range(6):
        for col in range(5): c.circle(82+col*112,TRIM_H-170-rr*88,28,stroke=1,fill=0)
    c.showPage()
    for row in rows:
        art=image_for(book,row['page'],row['object_name'])
        fit_image(c,art,45,132,TRIM_W-90,TRIM_H-178)
        label=row['object_name'].upper(); fact=fact_for(title,row['object_name']); c.setFont("Helvetica-Bold",20)
        tw=c.stringWidth(label,"Helvetica-Bold",20); bw=min(TRIM_W-70,max(390,tw+50)); bx=(TRIM_W-bw)/2
        c.setLineWidth(1.6); c.roundRect(bx,33,bw,78,12,stroke=1,fill=0); c.drawCentredString(TRIM_W/2,78,label)
        c.setFont("Helvetica",9.2); c.drawCentredString(TRIM_W/2,53,fact); c.showPage()
        c.setFont("Helvetica",7); c.drawCentredString(TRIM_W/2,18,"This page is intentionally blank to help prevent bleed-through."); c.showPage()
    c.setFont("Helvetica-Bold",25); c.drawCentredString(TRIM_W/2,TRIM_H*.62,"GREAT COLORING!")
    c.setFont("Helvetica",12); c.drawCentredString(TRIM_W/2,TRIM_H*.56,"You discovered 26 different creatures."); c.showPage()
    c.showPage(); c.showPage(); c.showPage(); c.save(); return path

def build_cover(book,title,color,rows):
    path=OUT/f"{book}-cover-full-wrap.pdf"; c=canvas.Canvas(str(path),pagesize=(COVER_W,COVER_H),pageCompression=1)
    col=HexColor(color); c.setFillColor(col); c.rect(0,0,COVER_W,COVER_H,fill=1,stroke=0)
    front_x=.125*72+8.5*72+SPINE
    c.setFillColor(white); c.roundRect(front_x+28,35,8.5*72-68,COVER_H-70,24,fill=1,stroke=0)
    c.setStrokeColor(col); c.setLineWidth(2); c.roundRect(front_x+42,49,8.5*72-96,COVER_H-98,20,fill=0,stroke=1)
    fit_image(c,image_for(book,rows[0]['page'],rows[0]['object_name']),front_x+95,190,8.5*72-190,430)
    c.setFillColor(col); c.setFont("Helvetica-Bold",34); c.drawCentredString(front_x+4.25*72,COVER_H-105,title.upper())
    c.setFont("Helvetica-Bold",14); c.drawCentredString(front_x+4.25*72,92,"26 BIG PICTURES WITH NAMES AND FUN FACTS")
    c.setFillColor(white); c.setFont("Helvetica-Bold",20); c.drawString(54,COVER_H-90,title.upper())
    c.setFont("Helvetica",12); c.drawString(54,COVER_H-120,"A COLORING BOOK FOR AGES 5-9")
    t=c.beginText(54,COVER_H-180); t.setLeading(20)
    for line in ["Meet 26 different creatures, each with", "a big picture, its name, and a fun fact.","","Simple backgrounds","Bold outlines","Single-sided coloring pages","Large 8.5 x 11 inch format"]: t.textLine(line)
    c.drawText(t); c.setFillColor(white); c.rect(54,50,144,86,fill=1,stroke=0); c.save(); return path

def main():
    OUT.mkdir(parents=True,exist_ok=True); rows=list(csv.DictReader(MANIFEST.open()))
    books={}
    for r in rows: books.setdefault(r['book_slug'],[]).append(r)
    built=[]
    for book,items in books.items():
        if not all(image_for(book,r['page'],r['object_name']).exists() for r in items): continue
        build_interior(book,items[0]['book_title'],items); build_cover(book,items[0]['book_title'],items[0]['cover_color'],items); built.append(book)
    for p in OUT.glob('*.pdf'):
        pages=len(PdfReader(str(p)).pages); assert pages==(60 if 'interior' in p.name else 1),(p,pages)
    print('built',','.join(built) if built else 'none')

if __name__=='__main__': main()
