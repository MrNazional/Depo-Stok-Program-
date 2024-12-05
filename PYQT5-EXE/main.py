import sys 
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from Depo_stok import *

#----------------------------------------------------------------------------------------------------------------------------------
#------------------------------------- Pencere Oluşturma ve Pencere Görüntüleme ---------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------

uygulma = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()


#----------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------Veritabanı Kısmı ----------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------
import sqlite3

baglanti = sqlite3.connect("depo.db")
islem = baglanti.cursor()
baglanti.commit()

table = islem.execute('''CREATE TABLE IF NOT EXISTS urun (
                    urunKodu INTEGER PRIMARY KEY,
                    urunAdi TEXT,
                    birimFiyat INTEGER,
                    stokMiktari INTEGER,
                    urunAciklaması TEXT,
                    marka TEXT,
                    kategori TEXT
                )''')

baglanti.commit()
#----------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------- Kayıt Girme ve Ürün Ekleme Kısmı ---------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------

def kayit_ekle():
    UrunKodu = int(ui.lneurunKodu.text())
    UrunAdi = ui.lneurunAd.text()
    BirimFiyat =int(ui.lnebrmFy.text())
    StokMiktar = int(ui.stokmktar.text())
    UrunAciklama = ui.acklama.text()
    Marka = ui.cmbMarka.currentText()
    Kategori = ui.cmbKategory.currentText()
    
    try:
        ekle = "insert into urun (urunKodu, urunAdi, birimFiyat, stokMiktari, urunAciklamasi, marka, kategori) values (?,?,?,?,?,?,?)"
        islem.execute(ekle,(UrunKodu,UrunAdi,BirimFiyat,StokMiktar,UrunAciklama,Marka,Kategori))
        baglanti.commit()
        kayit_listele()
        ui.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı Şekilde Tamamlandİ",3500)
        
    except Exception as error:
        ui.statusbar.showMessage("Kayıt Eklenemedi Hata Çıktı === "+str(error))

#----------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- Tüm Kayıtları Listeleme -----------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------
 
def kayit_listele():
    ui.tbltabloListele.clear()
    ui.tbltabloListele.setHorizontalHeaderLabels(("Ürün Kodu","Ürün Adi","Birim Fiyatı","Stok Miktarı","Ürün Açıklaması","Marka","Kategori"))
    ui.tbltabloListele.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    sorgu = "select * from urun"
    islem.execute(sorgu)
    
    for indexSatir, kayitNumarasi in enumerate(islem):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.tbltabloListele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

#----------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------- Kategorisel Olarak Listeleme -------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------

def kategoriye_gore_listele():
    listelenecek_kategori = ui.cmbKategorylistele.currentText()
    
    sorgu =  "select * from urun where kategori = ?"
    islem.execute(sorgu,(listelenecek_kategori,))
    ui.tbltabloListele.clear()
    
    for indexSatir, kayitNumarasi in enumerate(islem):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.tbltabloListele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

#----------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- Kayıt Silme ----------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------

def kayit_sil():
    sil_mesaj = QMessageBox.question(pencere,"Silme Onayı","Silmek İstediğinizden emin misiniz ?",QMessageBox.Yes | QMessageBox.No)
    
    if sil_mesaj == QMessageBox.Yes:
        secilen_kayit = ui.tbltabloListele.selectedItems()
        silinecek_kayit = secilen_kayit[0].text()
        
        sorgu = "delete from urun where urunKodu = ?"
        try:
            islem.execute(sorgu,(silinecek_kayit,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Başarıyla Silindi")
            kayit_listele()
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Silinirken Hata Çıktı ==="+str(error))
    else:
        ui.statusbar.showMessage("Silme İşlemi İptal Edildi")
 
 #----------------------------------------------------------------------------------------------------------------------------------
 #--------------------------------------------- Ürün Güncelleme --------------------------------------------------------------------
 #----------------------------------------------------------------------------------------------------------------------------------
def kayit_güncelle():
    güncelle_mesaj = QMessageBox.question(pencere,"Güncelleme Onayı","Bu Kaydı Güncellemek İstediğinizden emin misiniz ?",QMessageBox.Yes| QMessageBox.No)
    
    if güncelle_mesaj == QMessageBox.Yes:
        try:
            UrunKodu = ui.lneurunKodu.text()
            UrunAdi = ui.lneurunAd.text()
            BirimFiyat = ui.lnebrmFy.text()
            StokMiktar = ui.stokmktar.text()
            UrunAciklama = ui.acklama.text()
            Marka = ui.cmbMarka.currentText()
            Kategori = ui.cmbKategory.currentText()
            
            
            if UrunAdi == "" and BirimFiyat == "" and StokMiktar == "" and UrunAciklama == "" and Marka == "":
                islem.execute("UPDATE urun SET kategori = ? WHERE urunKodu = ?", (Kategori, UrunKodu))
                
            elif UrunAdi == "" and BirimFiyat == "" and StokMiktar == "" and UrunAciklama == "" and Kategori == "":
                islem.execute("UPDATE urun SET marka = ? WHERE urunKodu = ?", (Marka, UrunKodu))
                
            elif UrunAdi == "" and BirimFiyat == "" and StokMiktar == "" and Marka == "" and Kategori == "":
                islem.execute("UPDATE urun SET urunAciklamasi = ? WHERE urunKodu = ?", (UrunAciklama, UrunKodu))
                
            elif UrunAdi == "" and BirimFiyat == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                islem.execute("UPDATE urun SET stokMiktari = ? WHERE urunKodu = ?", (StokMiktar, UrunKodu))
                
            elif UrunAdi == "" and StokMiktar == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                islem.execute("UPDATE urun SET birimFiyat = ? WHERE urunKodu = ?", (BirimFiyat, UrunKodu))
                
            elif BirimFiyat == "" and StokMiktar == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                islem.execute("UPDATE urun SET urunAdi = ? WHERE urunKodu = ?", (UrunAdi, UrunKodu))
                
            else:
                islem.execute("UPDATE urun SET urunAdi = ?, birimFiyat = ?, stokMiktari = ?, urunAciklamasi = ?, Marka = ?, kategori = ? WHERE urunKodu = ?", 
                              (UrunAdi, BirimFiyat, StokMiktar, UrunAciklama, Marka, Kategori, UrunKodu))

            baglanti.commit()

            kayit_listele()
            ui.statusbar.showMessage("Kayıt Başarıyla Güncellendi")
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Güncellemede Hata Çıktı === " + str(error))
    else:
        ui.statusbar.showMessage("Güncelleme İptal Edildi")
            
                     
            
#----------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- Buton İşlemleri ------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------


ui.btnEkle.clicked.connect(kayit_ekle)
ui.btnurunListele.clicked.connect(kayit_listele)
ui.btnKategorylistele.clicked.connect(kategoriye_gore_listele)
ui.btnSil.clicked.connect(kayit_sil)
ui.btnGuncelle.clicked.connect(kayit_güncelle)


#pencerenin kapatma işlemi için
sys.exit(uygulma.exec_())
