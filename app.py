from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin
from flask_login import login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from forms import login, profil_F, DataDemog_F, penduduk_F, admin_F, surat_F

app=Flask(__name__)
app.config['SECRET_KEY'] = "andrian"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data_Demog.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager= LoginManager(app)


# awal table penduduk
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
# akhir table surat keterangan



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/home2")
def home2():
    return render_template("home_admin.html")

@app.route("/profil")
def profil():
    form=Tprofil.query.all()
    return render_template("profil.html", form=form)

@app.route("/profil2")
def profil2():
    form=Tprofil.query.all()
    return render_template("profil2.html", form=form)

@app.route("/daftar",  methods=['GET', 'POST'])
def daftar():
    form=penduduk_F()
    if request.method == 'POST':
        pass_hash = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        data= Tpenduduk(nik=form.nik.data, nama=form.nama.data, tgl_lahir=form.tgl_lahir.data, email=form.email.data, password=pass_hash, alamat=form.alamat.data, tlp=form.tlp.data)
        db.session.add(data)
        db.session.commit()
        flash('Akun berhasil daftar', 'primary')
        return redirect(url_for('daftar'))
    return render_template("daftar.html",form=form)


@app.route("/daftar_admin",  methods=['GET', 'POST'])
def daftar_admin():
    form=admin_F()
    if form.validate_on_submit():
        pass_hash = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        add= Tadmin(nama=form.nama.data, username=form.username.data, password=pass_hash)
        db.session.add(add)
        db.session.commit()
        flash(f'Akun berhasil daftar', 'primary')
        return redirect(url_for('admin'))
    return render_template("admin.html",form=form)

@app.route("/editprofil", methods=['GET','POST'])
def editprofil():
    form=profil_F()
    if request.method == 'POST':
        m_data=Tprofil.query.get(request.form.get('id'))
        m_data.sejarah=request.form['sejarah']
        m_data.profil_kel=request.form['profil_kel']
        m_data.visi_misi=request.form['visi_misi']
        db.session.commit()
        flash('Data berhasisl diubah', 'warning')
        return redirect(url_for('profil'))
    return render_template('edit_profil.html', form=form)

@app.route("/data_demografis", methods=['GET','POST'])
def data_demog():
    Dataa=DataDemog.query.all()
    return render_template("data_demog.html", Data=Dataa)

@app.route("/data_demografis2", methods=['GET','POST'])
def data_demog2():
    Dataa=DataDemog.query.all()
    return render_template("data_demog2.html", Data=Dataa)

@app.route("/isi_data_demografis", methods=['GET','POST'])
def isi_data_demog():
    form=DataDemog_F()
    if form.validate_on_submit():
        add = DataDemog(rt=form.rt.data, nama_rt=form.nama_ketua_rt.data, jumlah_kk=form.jumlah_kk.data, jumlah_p=form.jumlah_jiwa_p.data, jumlah_l=form.jumlah_jiwa_l.data, jumlah_jiwa=form.jumlah_jiwa.data)
        db.session.add(add)
        db.session.commit()
        flash(f'Data Berhasil Di Input', 'primary')
        return redirect(url_for('data_demog'))
    return render_template("isidataDemog.html", form=form)

@app.route("/ketrangan", methods=['GET', 'POST'])
def ketrangan():
    if not current_user.is_authenticated:
        return redirect(url_for('user'))
    Data=Tsurat_ket.query.filter_by(penduduk_id=current_user.id)
    form=surat_F()
    if request.method == 'POST':
        # tambah data pengaduan
        add = Tsurat_ket(kategori=form.kategori.data, keterangan=form.keterangan.data, penduduk=current_user)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasisl ditambahkan', 'warning')
        return redirect(url_for('ketrangan'))
    return render_template("surat_ket.html", form=form, Data=Data)

@app.route("/ketrangan2", methods=['GET', 'POST'])
@login_required
def ketrangan2():
    Data=Tsurat_ket.query.filter_by(penduduk_id=current_user.id)
    all_data=Tsurat_ket.query.all()
    form=surat_F()
    if request.method == 'POST':
        # tambah data pengaduan
        add = Tsurat_ket(kategori=form.kategori.data, keterangan=form.keterangan.data, penduduk=current_user)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasisl ditambahkan', 'warning')
        return redirect(url_for('ketrangan2'))
    return render_template("surat_ket2.html", form=form, Data=Data, all_data=all_data)


@app.route("/editdatademog", methods=['GET','POST'])
def editdatademog():
    if request.method == 'POST':
        m_data=DataDemog.query.get(request.form.get('id'))
        m_data.rt=request.form['rt']
        m_data.nama_rt=request.form['nama_rt']
        m_data.jumlah_kk=request.form['jumlah_kk']
        m_data.jumlah_p=request.form['jumlah_p']
        m_data.jumlah_l=request.form['jumlah_l']
        m_data.jumlah_jiwa=request.form['jumlah_jiwa']
        db.session.commit()
        flash('Data berhasisl diubah', 'warning')
        return redirect(url_for('data_demog'))
    


@app.route("/user",  methods=['GET', 'POST'])
def user():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=login()
    if request.method == 'POST':
        ceknik=Tpenduduk.query.filter_by(nik=form.username.data).first()
        if ceknik and bcrypt.check_password_hash(ceknik.password, form.password.data):
            login_user(ceknik)
            flash('selamat Datang Kembali', 'warning')
            return redirect(url_for('home'))
        else:
            flash('login gagal, periksa username dan Password!', 'danger')
    return render_template("login_user.html", form=form)

@app.route("/editpengaduan", methods=['GET','POST'])
@login_required
def editpengaduan():
    if request.method == 'POST':
        m_data=Tsurat_ket.query.get(request.form.get('id'))
        m_data.kategori=request.form['kategori']
        m_data.keterangan=request.form['keterangan']
        db.session.commit()
        flash('Data berhasisl diubah', 'warning')
        return redirect(url_for('ketrangan'))

@app.route("/editpengaduan2", methods=['GET','POST'])
@login_required
def editpengaduan2():
    if request.method == 'POST':
        m_data=Tsurat_ket.query.get(request.form.get('id'))
        m_data.kategori=request.form['kategori']
        m_data.keterangan=request.form['keterangan']
        db.session.commit()
        flash('Data berhasisl diubah', 'warning')
        return redirect(url_for('ketrangan2'))




@app.route("/hapus_A/<id>", methods=['GET', 'POST'])
@login_required
def hapus_A(id):
    my = Tsurat_ket.query.get(id)
    db.session.delete(my)
    db.session.commit()
    flash('Data berhasisl dihapus', 'warning')
    return redirect(url_for('ketrangan'))

@app.route("/hapus_A2/<id>", methods=['GET', 'POST'])
@login_required
def hapus_A2(id):
    my = Tsurat_ket.query.get(id)
    db.session.delete(my)
    db.session.commit()
    flash('Data berhasisl dihapus', 'warning')
    return redirect(url_for('ketrangan2'))

@app.route("/admin",  methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        return redirect(url_for('home2'))
    form = admin_F()
    if request.method == 'POST':
        cekusername=Tadmin.query.filter_by(username=form.username.data).first()
        if cekusername and bcrypt.check_password_hash(cekusername.password, form.password.data):
            login_user(cekusername)
            flash('selamat Datang Kembali', 'warning')
            return redirect(url_for('home2'))
        else:
            flash('login gagal, periksa username dan Password!', 'danger')
    return render_template("login_admin.html", form=form)


@app.route("/logout_admin")
def logout_admin():
    logout_user()
    return redirect(url_for('home'))

if __name__=="__main__":
    app.run(debug=True)