from datetime import datetime
from sim import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(admin_id):
    return Tadmin.query.get(int(admin_id))

# awal table admin
class Tadmin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Tprofil('{self.nama}', '{self.username}', '{self.password}')"
# akhir table admin

# awal table demografi
class DataDemog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rt = db.Column(db.String(3), nullable=False)
    nama_rt = db.Column(db.String(100), nullable=False, default='Nama')
    jumlah_kk = db.Column(db.String(5), nullable=False)
    jumlah_p = db.Column(db.String(5), nullable=False)
    jumlah_l = db.Column(db.String(5), nullable=False)
    jumlah_jiwa = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return f"DataDomog('{self.rt}','{self.nama_rt}','{self.jumlah_kk}','{self.jumlah_p}','{self.jumlah_l}','{self.jumlah_jiwa}')"
# akhir table demografi

# awal table profil
class Tprofil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sejarah = db.Column(db.Text, nullable=False)
    profil_kel = db.Column(db.Text, nullable=False)
    visi_misi = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Tprofil('{self.sejarah}', '{self.profil_kel}', '{self.visi_misi}')"
# akhir table profil

# awal table penduduk
@login_manager.user_loader
def load_user(penduduk_id):
    return Tpenduduk.query.get(int(penduduk_id))

class Tpenduduk(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(25), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    tgl_lahir = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    alamat = db.Column(db.String(50), nullable=False)
    tlp = db.Column(db.String(12), nullable=False)
    surat = db.relationship('Tsurat_ket', backref='penduduk', lazy=True)

    def __repr__(self):
        return f"Tpenduduk('{self.nik}','{self.nama}','{self.tgl_lahir}','{self.email}','{self.password}','{self.alamat}', '{self.tlp}')"
# akhir table penduduk

# awal table surat keterangan
class Tsurat_ket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kategori = db.Column(db.String(50), nullable=False)
    keterangan = db.Column(db.String(300), nullable=False)
    tgl_post = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)
    penduduk_id = db.Column(db.Integer, db.ForeignKey('tpenduduk.id'))

    def __repr__(self):
        return f"Tsurat_ket('{self.kategori}', '{self.keterangan}', '{self.tgl_post}')"