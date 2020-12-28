from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed


class penduduk_F(FlaskForm):
    nik = StringField('NIK', validators=[DataRequired(), Length(min=10, max=15)])
    nama = StringField('NAMA', validators=[DataRequired()])
    tgl_lahir = StringField('TGL LAHIR', validators=[DataRequired(), Email()])
    email = StringField('EMAIL', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    konf_pass = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    alamat = TextAreaField('Alamat')
    tlp = StringField('TLP', validators=[DataRequired()])
    submit = SubmitField('Tambah')


    def validate_nik(self, nik):
        ceknik = Tpenduduk.query.filter_by(nik=form.nik.data).first()
        if ceknik:
            raise ValidationError('NPM Sudah Terdaftar, Gunakan NPM Yang Lain')

    # cek email
    def validate_email(self, email):
        cekemail = Tpenduduk.query.filter_by(email=form.email.data).first()
        if cekemail:
            raise ValidationError('Email Sudah Terdaftar, Gunakan Email Yang Lain')


class login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')  

class admin_F(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    konf_pass = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Login')  

class profil_F(FlaskForm):
    sejarah = TextAreaField('sejarah')
    tentang_kel = TextAreaField('tentang_kel')
    visi_misi = TextAreaField('visi_misi')
    submit = SubmitField('post')

class DataDemog_F(FlaskForm):
    rt = StringField('RT', validators=[DataRequired()])
    nama_ketua_rt = StringField('NAMA KETUA RT', validators=[DataRequired()])
    jumlah_kk = StringField('JUMLAH KK', validators=[DataRequired()])
    jumlah_jiwa_p = StringField('JUMLAH JIWA P', validators=[DataRequired()])
    jumlah_jiwa_l = StringField('JUMLAH JIWA L', validators=[DataRequired()])
    jumlah_jiwa = StringField('JUMLAH JIWA P/L', validators=[DataRequired()])
    submit = SubmitField('post')

class surat_F(FlaskForm):
    kategori = SelectField(u'Kategori Pengaduan', choices=[('TidakMampu','Keterangan Tidak Mampu'), ('BelumMenika','Keterangan Belum Menika')], validators=[DataRequired()])
    keterangan = TextAreaField('Keterangan', validators=[DataRequired()])
    submit=SubmitField('Kirim')













