from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from sim import db, bcrypt
from sim.admin.forms import login, profil_F, DataDemog_F, penduduk_F, surat_F, admin_F
from sim.models import Tpenduduk, Tprofil, DataDemog, Tsurat_ket, Tadmin

Sadmin = Blueprint('Sadmin', __name__)



@Sadmin.route("/home2")
def home2():
    return render_template("home_admin.html")



@Sadmin.route("/profil2")
def profil2():
    form=Tprofil.query.all()
    return render_template("profil2.html", form=form)

@Sadmin.route("/daftar",  methods=['GET', 'POST'])
def daftar():
    form=penduduk_F()
    if request.method == 'POST':
        pass_hash = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        data= Tpenduduk(nik=form.nik.data, nama=form.nama.data, tgl_lahir=form.tgl_lahir.data, email=form.email.data, password=pass_hash, alamat=form.alamat.data, tlp=form.tlp.data)
        db.session.add(data)
        db.session.commit()
        flash('Akun berhasil daftar', 'primary')
        return redirect(url_for('Sadmin.daftar'))
    return render_template("daftar2.html",form=form)


@Sadmin.route("/daftar_admin",  methods=['GET', 'POST'])
def daftar_admin():
    form=admin_F()
    if form.validate_on_submit():
        pass_hash = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        add= Tadmin(nama=form.nama.data, username=form.username.data, password=pass_hash)
        db.session.add(add)
        db.session.commit()
        flash(f'Akun berhasil daftar', 'primary')
        return redirect(url_for('Sadmin.admin'))
    return render_template("admin.html",form=form)

@Sadmin.route("/editprofil", methods=['GET','POST'])
def editprofil():
    if request.method == 'POST':
        m_data=Tprofil.query.get(request.form.get('id'))
        m_data.sejarah=request.form['sejarah']
        m_data.profil_kel=request.form['profil_kel']
        m_data.visi_misi=request.form['visi_misi']
        db.session.commit()
        flash('Data berhasisl diubah', 'warning')
        return redirect(url_for('Sadmin.profil2'))

@Sadmin.route("/isi_data_profil", methods=['GET','POST'])
def isi_data_profil():
    form=profil_F()
    if form.validate_on_submit():
        add = Tprofil(sejarah=form.sejarah.data, profil_kel=form.tentang_kel.data, visi_misi=form.visi_misi.data,)
        db.session.add(add)
        db.session.commit()
        flash(f'Data Berhasil Di Input', 'primary')
        return redirect(url_for('Sadmin.profil2'))
    return render_template("edit_profil.html", form=form)

@Sadmin.route("/data_demografis2", methods=['GET','POST'])
def data_demog2():
    Dataa=DataDemog.query.all()
    return render_template("data_demog2.html", Data=Dataa)

@Sadmin.route("/isi_data_demografis", methods=['GET','POST'])
def isi_data_demog():
    form=DataDemog_F()
    if form.validate_on_submit():
        add = DataDemog(rt=form.rt.data, nama_rt=form.nama_ketua_rt.data, jumlah_kk=form.jumlah_kk.data, jumlah_p=form.jumlah_jiwa_p.data, jumlah_l=form.jumlah_jiwa_l.data, jumlah_jiwa=form.jumlah_jiwa.data)
        db.session.add(add)
        db.session.commit()
        flash(f'Data Berhasil Di Input', 'primary')
        return redirect(url_for('Sadmin.data_demog2'))
    return render_template("isidataDemog.html", form=form)



@Sadmin.route("/ketrangan2", methods=['GET', 'POST'])
@login_required
def ketrangan2():
    if not current_user.is_authenticated:
        return redirect(url_for('Sadmin.home2'))
    Data=Tsurat_ket.query.filter_by(penduduk_id=current_user.id)
    all_data=Tsurat_ket.query.all()
    form=surat_F()
    if request.method == 'POST':
        # tambah data pengaduan
        add = Tsurat_ket(kategori=form.kategori.data, keterangan=form.keterangan.data, penduduk=current_user)
        db.session.add(add)
        db.session.commit()
        flash('Data berhasisl ditambahkan', 'warning')
        return redirect(url_for('Sadmin.ketrangan2'))
    return render_template("surat_ket2.html", form=form, Data=Data, all_data=all_data)


@Sadmin.route("/editdatademog", methods=['GET','POST'])
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
        return redirect(url_for('Sadmin.data_demog2'))
    



@Sadmin.route("/editpengaduan2", methods=['GET','POST'])
@login_required
def editpengaduan2():
    if not current_user.is_authenticated:
        return redirect(url_for('Sadmin.home2'))
    if request.method == 'POST':
        m_data=Tsurat_ket.query.get(request.form.get('id'))
        m_data.kategori=request.form['kategori']
        m_data.keterangan=request.form['keterangan']
        db.session.commit()
        flash('Data berhasisl diubah', 'warning')
        return redirect(url_for('Sadmin.ketrangan2'))





@Sadmin.route("/hapus_A2/<id>", methods=['GET', 'POST'])
@login_required
def hapus_A2(id):
    my = Tsurat_ket.query.get(id)
    db.session.delete(my)
    db.session.commit()
    flash('Data berhasisl dihapus', 'warning')
    return redirect(url_for('Sadmin.ketrangan2'))

@Sadmin.route("/admin",  methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        return redirect(url_for('Sadmin.home2'))
    form = admin_F()
    if request.method == 'POST':
        cekusername=Tadmin.query.filter_by(username=form.username.data).first()
        if cekusername and bcrypt.check_password_hash(cekusername.password, form.password.data):
            login_user(cekusername)
            flash('selamat Datang Kembali', 'warning')
            return redirect(url_for('Sadmin.home2'))
        else:
            flash('login gagal, periksa username dan Password!', 'danger')
    return render_template("login_admin.html", form=form)


@Sadmin.route("/logout_admin")
def logout_admin():
    logout_user()
    return redirect(url_for('Suser.home'))