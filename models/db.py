# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
import datetime

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.expiration = 3600 * 8  # seconds

auth.settings.extra_fields['auth_user'] = [
    Field("people_info", type="boolean"),
    Field("further_info", type="boolean"),
    Field("medical_docs", type="boolean"),
    Field("genetics_records", type="boolean"),
    Field("professional_cons_records", type="boolean"),
    Field("labs_records", type="boolean"),
    Field("admin_", type="boolean"),
]
auth.define_tables( migrate=False )
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = False

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

genders = ["مرد","زن"]
kid_genders = ["پسر","دختر"]
yes_no = ["خیر","بلی"]
yes_no_space = ["","خیر","بلی"]
races = ["فارس","ترک","لر","کرد","ترک خراسان","ترکمن","کرمانج","سیستانی","بلوچ","عرب","افغان", "مختلط"]
religion = ["اسلام","مسیحی","کلیمی","زرتشتی","سایر"]
sect = ["شیعه","سنی","سایر"]
job = ["بدون شغل","دانش آموز","دانشجو","سرباز","اداری-مالی","آموزشی-فرهنگی","فنی-مهندسی","بهداشتی-درمانی",
       "فناوری اطلاعات","کشاورزی-محیط زیسیت","نظامی-انتظامی","خدمات صنعتی","خدمات شهری","خدمات روستایی",
       "کارگر","بازنشسته","خانه دار",]
marital_condition = ["مجرد","متاهل","نامزد","عقد","طلاق","متارکه","فوت همسر","ازدواج مجدد","ازدواج موقت","تعدد همسر"]      
relativity_condition = ["پسرعمو-دختر عمو","پسر خاله- دخترخاله","پسر دایی-دختر عمه","پسر عمه-دختر دایی",
                        "نوه عمو-نوه عمو","نوه خاله -نوه خاله","نوه عمه-نوه دایی","فامیل دور","ندارند"]

center = ["آشنایی از طریق پزشک","تبلیغات","مراکز پزشکی","اقوام و آشنایان","مدرسه","118","فضای مجازی","سایر موارد"]
genetic_counselor = ["","دکتر صدرنبوی"]

live_con = ["سالم","بیمار","مرده"]
labour_con = ["طبیعی","سزارین","زایمان دشوار"]
yes_no_unknown = ["","بلی","خیر","نامشخص"]
edu_list = ["بدون سواد","خواندن و نوشتن","ابتدایی","راهنمایی","متوسطه","دیپلم","فوق دیپلم","لیسانس","فوق لیسانس ","دکتری حرفه ای","دکتری تخصصی","حوزوی"]
counselor_genetic_reasons = ["","پیش از ازدواج","حین بارداری","پس از بارداری","مشاوره تشخیصی - تشخیص بیماری ارثی در خانواده","سایر",]
special_list = ["","مغز و اعصاب","اطفال"]
test_names = []
test_users = ["آقا","خانم","فرزند","جنین",""]


upload_fields = []
for i in range(1,101):
    upload_fields.append(Field("upload_{}".format(i),"upload",label="آپلود مدرک پزشکی {}".format(i),uploadfolder='C:/Web2Py/applications/optimalinfosystem/static/images',uploadseparate=True)))

genetic_counselling_fields = []
specialist_counselling_fields = []

specialist_price = []
specialist_field = []

kid_info = []
female_rec = []
g_counseling_records = []

genetic_test_rec = []

molecular_diagnosis = []
pnd_1 = []
pnd_2 = []
pnd_1_2 = []
cyto_blood = []
cyto_amniotic = []

infertility_disease = []
infectious_disease = []
malignancies_cancer = []
blood_diseases = []
immune_disorders = []
endocrine_disorders = []
nutritional_disorders = []
autism = []
mental_disorders = []
nervous_diseases = []
visual_disease = []
hearing_diseases = []
cardiovascular_diseases = []
respiratory_system_diseases = []
gastrointestinal_diseases = []
skin_diseases = []
musculoskeletal_diseases = []
genitourinary_diseases = []


edta = []
heparin = []
cvs = []
af = []
abortion_product = []
cortage_product = []
paraffin_texture = []
blood_others = []


pregnancy_weeks = []
pregnancy_days = []
sampler = []
has_infection_history = []
hbv = []
hcv = []
hiv = []
htlv1 = []
other_infections = []


use_medicine = []
duration_medicine = []


    
for i in range(1,11):
    genetic_counselling_fields.append(Field("g_counselor_{}".format(i),requires=IS_IN_SET(genetic_counselor, zero=None),label="نام مشاور {}".format(i),default=' '))    
    genetic_counselling_fields.append(Field("reason_{}".format(i),requires=IS_IN_SET(counselor_genetic_reasons, zero=None),label="علت".format(i),))    
    genetic_counselling_fields.append(Field("g_upload_{}".format(i),"upload",label="آپلود فایل {}".format(i),uploadfolder='C:/Web2Py/applications/optimalinfosystem/static/images',uploadseparate=True)))

for i in range(1,11):
    specialist_counselling_fields.append(Field("sp_counselor_{}".format(i),requires=IS_IN_SET(genetic_counselor, zero=None),label="نام مشاور {}".format(i),default=' '))    
    specialist_counselling_fields.append(Field("field_{}".format(i),requires=IS_IN_SET(special_list, zero=None),label="تخصص".format(i),))    
    specialist_counselling_fields.append(Field("sp_upload_{}".format(i),"upload",label="آپلود فایل {}".format(i),uploadfolder='C:/Web2Py/applications/optimalinfosystem/static/images',uploadseparate=True)))
    specialist_counselling_fields.append(Field("price_{}".format(i),"string",label="هزینه".format(i),))

    # specialist_price.append(Field("price_{}".format(i),"string",label="هزینه".format(i),))    



for i in range(1,11):
    
    kid_name.append(Field("kid_{}_name".format(i), "string",label="نام فرزند درگیر عارضه",required=True,default=' '),)        
    kid_info.append(Field("kid_{}_id_code".format(i), "string",label="کدملی",required=True,default=' '),)        
    kid_info.append(Field("kid_{}_birth".format(i), "string",label="تاریخ تولد",required=True,default=' '),)  
    kid_info.append(Field("kid_{}_gender".format(i), requires=IS_IN_SET(kid_genders, zero=None),label="جنسیت",required=True,default=' '),) 
    kid_info.append(Field("kid_{}_live".format(i), requires=IS_IN_SET(live_con, zero=None),label="وضعیت جسمانی فعلی",required=True,default=' '),) 
    kid_info.append(Field("kid_{}_patient".format(i), "string",label="شرح بیماری"),)
    kid_info.append(Field("kid_{}_death".format(i), "string",label="علت فوت"), )
    kid_info.append(Field("kid_{}_number".format(i), "string",label="فرزند چندم",required=True,default=' '), )
    kid_info.append(Field("kid_{}labour".format(i), requires=IS_IN_SET(labour_con, zero=None),label="وضعیت زایمان",required=True,default=' '), )
    kid_info.append(Field("kid_{}_hospitalize_rec".format(i), requires=IS_IN_SET(yes_no_space, zero=None),label="سابقه بستری در دوران نوزادی",required=True,default=' '), )
    kid_info.append(Field("kid_{}_hospitalize_exp".format(i), "string",label="توضیحات",required=True,default=' '), )

#   وضعیت جسمی هنگام تولد

    kid_info.append(Field("kid_{}_weight_mem".format(i), requires=IS_IN_SET(yes_no_space, zero=None),label="وزن را بخاطر دارد",required=True,default=' '), )
    kid_info.append(Field("kid_{}_weight".format(i), "string",label="وزن به کیلوگرم"), )
    kid_info.append(Field("kid_{}_height_mem".format(i), requires=IS_IN_SET(yes_no_space, zero=None),label="قد را بخاطر دارد",required=True,default=' '), )
    kid_info.append(Field("kid_{}_height".format(i), "string",label="قد به سانتیمتر"), )
    kid_info.append(Field("kid_{}_head_mem".format(i), requires=IS_IN_SET(yes_no_space, zero=None),label="دور سر را بخاطر دارد",required=True,default=' '), )
    kid_info.append(Field("kid_{}_head".format(i), "string",label="دور سر به سانتیمتر"), )

for i in range(1,6):
    
    genetic_test_rec.append(Field("molecular_diagnosis_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="تشخیص مولکولی", required = True), )
    genetic_test_rec.append(Field("pnd_1_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="مرحله 1 PND",required = True ), )
    genetic_test_rec.append(Field("pnd_2_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="مرحله 2 PND", required = True), )
    genetic_test_rec.append(Field("pnd_1_2_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="مرحله 1 و 2 PND", required = True), )
    genetic_test_rec.append(Field("cyto_blood_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="سیتوژنتیک خون", required = True), )
    genetic_test_rec.append(Field("cyto_amniotic_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="سیتوژنتیک آمنیون",required = True), )
    

    genetic_test_rec.append(Field("infertility_disease_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="بیماری های زنان و نازایی : ناباروری، سقط مکرر، اختلالات قائدگی ",required = True), )
    genetic_test_rec.append(Field("infectious_disease_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="بیماری های عفونی و انگلی ",required = True), )
    genetic_test_rec.append(Field("malignancies_cancer_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="انواع بدخیمی ها و سرطان",required = True), )
    genetic_test_rec.append(Field("blood_diseases_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="بیماری های خون و سیستم خونساز مانند کم خونی ها: کم خونی داسی شکل، تالاسمی ها، هموفیلی",required = True), )
    genetic_test_rec.append(Field("immune_disorders_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="اختلالات ایمنی",required = True), )
    genetic_test_rec.append(Field("endocrine_disorders_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="اختلالات غدد درون ریز :دیابت، بیماری های تیروئید، غده فوق کلیوی، هایپرپلازی مادرزادی آدرنال",required = True), )
    genetic_test_rec.append(Field("nutritional_disorders_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="اختلالات تغذیه",required = True), )
    genetic_test_rec.append(Field("autism_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="اختلالات شناختی رفتاری :اوتیسم، روان پریشی",required = True), )
    genetic_test_rec.append(Field("mental_disorders_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="اختلالات عقب ماندگی ذهنی :سندرم های داوون، ایکس شکننده، پرادرویلی – آنجلمن، سندرم رت",required = True), )
    genetic_test_rec.append(Field("nervous_diseases_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="بیماری های سیستم اعصاب :سکته، سردرد، تشنج، اختلالات حرکتی – حسی، دیستونی، پارکینسون، ام اس ",required = True), )
    genetic_test_rec.append(Field("visual_disease_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="بیماری های سیستم بینایی",required = True), )
    genetic_test_rec.append(Field("hearing_diseases_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="بیماری های سیستم شنوایی",required = True), )
    genetic_test_rec.append(Field("cardiovascular_diseases_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="بیماری های سیستم قلب و گردش خون :کاردیومیوپاتی ها",required = True), )
    genetic_test_rec.append(Field("respiratory_system_diseases_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="بیماری های سیستم تنفسی",required = True), )
    genetic_test_rec.append(Field("gastrointestinal_diseases_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="بیماری های سیستم گوارش",required = True), )
    genetic_test_rec.append(Field("skin_diseases_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="بیماری های بافت پوست و بافت همبند:سندرم مارفان",required = True), )
    genetic_test_rec.append(Field("musculoskeletal_diseases_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="بیماری های سیستم عضلانی :دیستروفی های بکر، دوشن",required = True), )
    genetic_test_rec.append(Field("genitourinary_diseases_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="بیماری های سیستم ادراری تناسلی :ابهام جنسی، اختلالات کلیوی ",required = True), )



    genetic_test_rec.append(Field("edta_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="EDTA خون ",required = True), )
    genetic_test_rec.append(Field("heparin_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="خون هپارینه ",required = True), )
    genetic_test_rec.append(Field("cvs_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="CVS",required = True), )
    genetic_test_rec.append(Field("af_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="AF",required = True), )
    genetic_test_rec.append(Field("abortion_product_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="محصول سقط",required = True), )
    genetic_test_rec.append(Field("cortage_product_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="محصول کورتاژ",required = True), )
    genetic_test_rec.append(Field("paraffin_texture_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="بافت پارافینه",required = True), )
    genetic_test_rec.append(Field("blood_others_{}".format(i), "string",label="سایر",required = True), )
    for j in range(1,6):
        genetic_test_rec.append(Field("use_medicine_{}_{}".format(i,j), "string",label="مصرف دارو",required = True), )
        genetic_test_rec.append(Field("duration_medicine_{}_{}".format(i,j), "string",label="مدت مصرف",required = True), )
    
    genetic_test_rec.append(Field("pregnancy_weeks_{}".format(i), "string",label="هفته چندم بارداری",required = True), )
    genetic_test_rec.append(Field("pregnancy_days_{}".format(i), "string",label="روز چندم بارداری",required = True), )
    genetic_test_rec.append(Field("sampler_{}".format(i), "string",label="پزشک نمونه گیر",required = True), )

    genetic_test_rec.append(Field("has_infection_history_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="سابقه عفونت ندارد",required = True), )
    genetic_test_rec.append(Field("hbv_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="HBV",required = True), )
    genetic_test_rec.append(Field("hcv_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="HCV",required = True), )
    genetic_test_rec.append(Field("hiv_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="HIV",required = True), )
    genetic_test_rec.append(Field("htlv1_{}".format(i), requires=IS_IN_SET(yes_no, zero=None),label="HTLV1",required = True), )
    genetic_test_rec.append(Field("other_infections_{}".format(i), "string",label="سایر",required = True), )
    
for i in range(1,6):
    
    female_rec.append(Field("f_abortion_rec_{}".format(i), requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه سقط",required=True),)
    female_rec.append(Field("f_ab_pregnancy_numebr_{}".format(i), "string",label="بارداری چندم",required=True,default=' '),)
    female_rec.append(Field("f_ab_mother_age_{}".format(i), "string",label="سن مادر",required=True,default=' '),)
    female_rec.append(Field("f_ab_pregnancy_age_{}".format(i), "string",label="سن حاملگی",required=True,default=' '),)
    female_rec.append(Field("f_abortion_reason_{}".format(i).format(i), "string",label="علت",required=True,default=' '),)

    female_rec.append(Field("f_iufd_rec_{}".format(i), requires=IS_IN_SET(yes_no_unknown, zero=None),label="IUFD سابقه",required=True,),)
    female_rec.append(Field("f_iufd_pregnancy_numebr_{}".format(i), "string",label="بارداری چندم",required=True,default=' '),)
    female_rec.append(Field("f_iufd_mother_age_{}".format(i), "string",label="سن مادر",required=True,default=' '),)
    female_rec.append(Field("f_iufd_pregnancy_age_{}".format(i), "string",label="سن حاملگی",required=True,default=' '),)
    female_rec.append(Field("f_iufd_reason_{}".format(i), "string",label="علت",required=True,default=' '),)

signature = db.Table(db, 'signature',
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', db.auth_user, default=auth.user_id),
    Field('updated_on', 'datetime', update=request.now),
    Field('updated_by', db.auth_user, update=auth.user_id))



db.define_table("principal_info",
    # Field("case_number", "string",label="شماره پرونده"),
    Field("date", "date",label="تاریخ", writable = False),    
    Field("time", "time",label="زمان", writable = False),    
    signature,
    Field("case_number", "string",label="شماره پرونده", required=True), 
       
    migrate = True,
    # fake_migrate=False,
    )
# -----------------------Parents Section ------------------------------

db.define_table("people_info", 
    Field("date", "date",label="تاریخ", writable = False),    
    Field("time", "time",label="زمان", writable = False),    
    signature,

    Field("full_name", "string",label="نام و نام خانوادگی", required=True),
    Field("case_number", "string",label="شماره پرونده", writable=False, readable = False),
    Field("id_code", "text",label="کدملی", required=True),
    Field("gender", requires=IS_IN_SET(genders, zero=None),label="جنسیت", required=True),
    Field("father_name", "string",label="نام پدر", required=True),
    Field("birth_date", "string",label="تاریخ تولد", required=True),
    Field("birth_pro", "string",label="استان", required=True),
    Field("birth_city", "string",label="شهر", required=True),
    Field("race", requires=IS_IN_SET(races, zero=None),label="قومیت", required=True),
    Field("religions", requires=IS_IN_SET(religion, zero=None),label="دین"),
    Field("other_religions", "string",label="سایر"),
    Field("sects", requires=IS_IN_SET(sect, zero=None),label="مذهب"),
    Field("other_sects", "string",label="سایر"),
    Field("education", requires=IS_IN_SET(edu_list, zero=None),label="تحصیلات",required=True),
    Field("career", requires=IS_IN_SET(job, zero=None),label="شغل",required=True),
    Field("marital_con", requires=IS_IN_SET(marital_condition, zero=None),label="وضعیت تاهل",required=True)


# مشخصات همسر عنوان

    Field("probound_full_name", "string",label="نام و نام خانوادگی", required=True,default=' '),
    Field("case_number", "string",label="شماره پرونده", writable=False, readable = False),
    Field("probound_id_code", "text",label="کدملی", required=True,default=' '),
    Field("probound_gender", requires=IS_IN_SET(genders, zero=None),label="جنسیت", required=True,default=' '),
    Field("probound_father_name", "string",label="نام پدر", required=True,default=' '),
    Field("probound_birth_date", "string",label="تاریخ تولد", required=True,default=' '),
    Field("probound_birth_pro", "string",label="استان", required=True,default=' '),
    Field("probound_birth_city", "string",label="شهر", required=True,default=' '),
    Field("probound_race", requires=IS_IN_SET(races, zero=None),label="قومیت", required=True),
    Field("probound_religions", requires=IS_IN_SET(religion, zero=None),label="دین"),
    Field("probound_other_religions", "string",label="سایر"),
    Field("probound_sects", requires=IS_IN_SET(sect, zero=None),label="مذهب"),
    Field("probound_other_sects", "string",label="سایر"),
    Field("probound_education", requires=IS_IN_SET(edu_list, zero=None),label="تحصیلات",required=True),
    Field("probound_career", requires=IS_IN_SET(job, zero=None),label="شغل",required=True),
    Field("relativity", requires=IS_IN_SET(relativity_condition, zero=None),label="شغل",required=True),

    migrate = True,
)

# -----------------------Kids Section ------------------------------

db.define_table("kids_info",    
    Field("date", "date",label="تاریخ", writable = False),    
    Field("time", "time",label="زمان", writable = False), 
    signature,   

    Field("case_number", "string",label="شماره پرونده", writable=False, readable = False), 
    Field("son_health", "string",label="تعداد فرزندان پسر سالم",required=True,default=' '),
    Field("son_patient", "string",label="تعداد فرزندان پسر بیمار",required=True,default=' '),
    Field("son_death", "string",label="تعداد فرزندان پسر فوت شده",required=True,default=' '),    
    Field("doughter_health", "string",label="تعداد فرزندان دختر سالم",required=True,default=' '),
    Field("doughter_patient", "string",label="تعداد فرزندان دختر بیمار",required=True,default=' '),
    Field("doughter_death", "string",label="تعداد فرزندان دختر فوت شده",required=True,default=' '),    

#--------------------------------------------------------------------------------
#   if x = (son_patient +  son_death + doughter_patient + doughter_death + son_health + doughter_health) > 0 :
#       open required kid info for x number
#--------------------------------------------------------------------------------

    *kid_info[1:171],


    migrate = True,
)

# ----------------------- Contact Section ------------------------------
db.define_table("contact_info",    
    Field("date", "date",label="تاریخ", writable = False),    
    Field("time", "time",label="زمان", writable = False),    
    signature,

    Field("case_number", "string",label="شماره پرونده", writable=False, readable = False), 

# اطلاعات تماس

    Field("address", "text",label="محل سکونت",required=True,default=' '),
    Field("address_city", "text",label="شهرستان",required=True,default=' '),
    Field("tel", "string",label="تلفن",required=True,default=' '),    
    Field("cellphone", "string",label=" تلفن همراه",required=True,default=' '),    
    Field("e_mail", "string",label="ایمیل"),

# نحوه آشنایی با مرکز

    Field("knowing_centre", requires=IS_IN_SET(center, zero=None),label="نحوه آشنایی با مرکز",required=True,default=' '),  
    Field("center_others", "string",label="سایر موارد"),      
    migrate = True,
)

#-------------------- Further info Section -------------------------------

db.define_table("further_info_section",
    Field("date", "date",label="تاریخ", writable = False),    
    Field("time", "time",label="زمان", writable = False),    
    signature,

    Field("case_number", "string",label="شماره پرونده", writable=False, readable = False),

#  برای خانم /زن / دختر
### -------مجاورت با عوامل محیطی 

    Field("f_alc_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه مصرف الکل"),
    Field("f_alc_day_rec", "string",label="مدت: روز"),
    Field("f_alc_month_rec", "string",label="مدت: ماه"),
    Field("f_alc_year_rec", "string",label="مدت: سال"),
    Field("f_alc_age_from", "string",label="مقطع سنی از"),
    Field("f_alc_age_until", "string",label="مقطع سنی تا"),


    Field("f_cigar_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه مصرف سیگار"),
    Field("f_cigar_day_rec", "string",label="مدت: روز"),
    Field("f_cigar_month_rec", "string",label="مدت: ماه"),
    Field("f_cigar_year_rec", "string",label="مدت: سال"),    
    Field("f_cigar_age_from", "string",label="مقطع سنی از"),
    Field("f_cigar_age_until", "string",label="مقطع سنی تا"),    

    Field("f_op_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه مصرف دخانیات"),
    Field("f_op_type", "string",label="ماده مصرفی"),
    Field("f_op_day_rec", "string",label="مدت: روز"),
    Field("f_op_month_rec", "string",label="مدت: ماه"),
    Field("f_op_year_rec", "string",label="مدت: سال"), 
    Field("f_op_age_from", "string",label="مقطع سنی از"),
    Field("f_op_age_until", "string",label="مقطع سنی تا"),          

    
    Field("f_chem_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه مجاورت با مواد شیمیایی"),
    Field("f_chem_type", "string",label="نام ماده"),
    Field("f_chem_day_rec", "string",label="مدت: روز"),
    Field("f_chem_month_rec", "string",label="مدت: ماه"),
    Field("f_chem_year_rec", "string",label="مدت: سال"),  
    Field("f_chem_age_from", "string",label="مقطع سنی از"),
    Field("f_chem_age_until", "string",label="مقطع سنی تا"),        


    Field("f_sex_organ_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه ابتلا به عفونت تناسلی"),
    Field("f_sex_organ_day_rec", "string",label="مدت: روز"),
    Field("f_sex_organ_month_rec", "string",label="مدت: ماه"),
    Field("f_sex_organ_year_rec", "string",label="مدت: سال"),  
    Field("f_sex_organ_age_from", "string",label="مقطع سنی از"),
    Field("f_sex_organ_age_until", "string",label="مقطع سنی تا"),   



    Field("f_xray_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه تماس با اشعه حین بارداری"),
    Field("f_xray_type", "string",label="نوع رادیوگرافی"),
    Field("f_xray_pregnancy_numebr", "string",label="بارداری چندم"),
    Field("f_xray_times", "string",label="تعداد دفعات رادیوگرافی"),  
  

    Field("f_drug_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سایقه مصرف دارو حین بارداری"),
    Field("f_drug_type", "string",label="نوع دارو"),
    Field("f_drug_pregnancy_numebr", "string",label="بارداری چندم"),




    ###--------------- ناباروری و سقط ----------------

    Field("f_infertility_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه عدم باروری"),
    Field("f_infertility_year", "string",label="مدت: سال"),
    Field("f_infertility_reason", "string",label="علت"),

    *female_rec[1:61]

    Field("infertility_treatments", requires=IS_IN_SET(yes_no_unknown, zero=None),label="اقدامات درمانی ناباروری"),
    Field("medicine_treatments", "string",label="درمان دارویی"),
    Field("iui",requires=IS_IN_SET(yes_no_space, zero=None),label="IUI"),
    Field("ivf",requires=IS_IN_SET(yes_no_space, zero=None),label="IVF"),
    Field("egg_donation",requires=IS_IN_SET(yes_no_space, zero=None),label="اهدای تخمک"),
    Field("embryo_donation",requires=IS_IN_SET(yes_no_space, zero=None),label="اهدای جنین"),
    Field("whoomb_rent",requires=IS_IN_SET(yes_no_space, zero=None),label="رحم اجاره ای"),
    Field("sprem_donation",requires=IS_IN_SET(yes_no_space, zero=None),label="اهدای اسپرم"),
    Field("other_treatments","string",label="سایر روش ها"),
    Field("f_explanation", "text",label="توضیحات"),


#    برای آقا / مرد / پسر
# سابقه ناباروری

    Field("m_alc_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه مصرف الکل"),
    Field("m_alc_day_rec", "string",label="مدت: روز"),
    Field("m_alc_month_rec", "string",label="مدت: ماه"),
    Field("m_alc_year_rec", "string",label="مدت: سال"),
    Field("m_alc_age_from", "string",label="مقطع سنی از"),
    Field("m_alc_age_until", "string",label="مقطع سنی تا"),

    Field("m_cigar_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه مصرف سیگار"),
    Field("m_cigar_day_rec", "string",label="مدت: روز"),
    Field("m_cigar_month_rec", "string",label="مدت: ماه"),
    Field("m_cigar_year_rec", "string",label="مدت: سال"),    
    Field("m_cigar_age_from", "string",label="مقطع سنی از"),
    Field("m_cigar_age_until", "string",label="مقطع سنی تا"),    

    Field("m_op_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه مصرف دخانیات"),
    Field("m_op_type", "string",label="ماده مصرفی"),
    Field("m_op_day_rec", "string",label="مدت: روز"),
    Field("m_op_month_rec", "string",label="مدت: ماه"),
    Field("m_op_year_rec", "string",label="مدت: سال"), 
    Field("m_op_age_from", "string",label="مقطع سنی از"),
    Field("m_op_age_until", "string",label="مقطع سنی تا"),          

    Field("m_chem_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه مجاورت با مواد شیمیایی"),
    Field("m_chem_type", "string",label="نام ماده"),
    Field("m_chem_day_rec", "string",label="مدت: روز"),
    Field("m_chem_month_rec", "string",label="مدت: ماه"),
    Field("m_chem_year_rec", "string",label="مدت: سال"),  
    Field("m_chem_age_from", "string",label="مقطع سنی از"),
    Field("m_chem_age_until", "string",label="مقطع سنی تا"),        

    Field("m_sex_organ_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه ابتلا به عفونت تناسلی"),
    Field("m_sex_organ_day_rec", "string",label="مدت: روز"),
    Field("m_sex_organ_month_rec", "string",label="مدت: ماه"),
    Field("m_sex_organ_year_rec", "string",label="مدت: سال"),  
    Field("m_sex_organ_age_from", "string",label="مقطع سنی از"),
    Field("m_sex_organ_age_until", "string",label="مقطع سنی تا"),   

    Field("m_infertility_rec", requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه عدم باروری"),
    Field("m_infertility_year", "string",label="مدت: سال"),
    Field("m_infertility_reason", "string",label="علت"),
    Field("m_explanation", "text",label="توضیحات"),

    migrate = True,    
)



db.define_table("physician_docs",   
    Field("date", "date",label="تاریخ", writable = False),    
    Field("time", "time",label="زمان", writable = False),  
    signature,  

    Field("case_number", "string",label="شماره پرونده", writable=False, readable = False), 

    Field("pedigree", "upload",label="آپلود شجره نامه", uploadfolder='C:/Web2Py/applications/optimalinfosystem/static/images',uploadseparate=True),
    *upload_fields[1:101]

    migrate = True,   

)



db.define_table("genetics_counseling_records",   
    Field("date", "date",label="تاریخ", writable = False),    
    Field("time", "time",label="زمان", writable = False), 
    signature,   

    Field("case_number", "string",label="شماره پرونده", writable=False, readable = False), 
    *genetic_counselling_fields[1:11],

    migrate = True,   

)

db.define_table("special_counseling_records",   
    Field("date", "date",label="تاریخ", writable = False),    
    Field("time", "time",label="زمان", writable = False),    
    signature,

    Field("case_number", "string",label="شماره پرونده", writable=False, readable = False), 
    *specialist_counselling_fields[1:11],

    migrate = True,   

)


db.define_table("genetic_test_records",
    Field("date", "date",label="تاریخ", writable = False),    
    Field("time", "time",label="زمان", writable = False),    
    signature,
    Field("case_number", "string",label="شماره پرونده", writable=False, readable = False), 

    Field("test_user", requires=IS_IN_SET(test_users, zero=None),label="تست برای", ), 
    Field("test_name", requires=IS_IN_SET(test_names, zero=None),label="نام آزمایش", ), 
    Field("referred_physician", "string",label="پزشک ارجاع دهنده", required = True, default = ' '), 
    Field("referred_physician_sp", "string",label="تخصص", required = True, default = ' '), 

    *genetic_test_rec[1:6]
 
    migrate = True,
)    
