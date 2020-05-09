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

upload_fields = []
for i in range(1,101):
    upload_fields.append(Field("upload_{}".format(i),"upload",label="آپلود مدرک پزشکی {}".format(i),uploadfolder='C:/Web2Py/applications/optimalinfosystem/static/images',uploadseparate=True)))

counselor_name = []
counselor_gen_reason = []
upload_fields_counselling = []
specialist_price = []
specialist_field = []

kid_name = []
kid_id_code = []
kid_birth = []
kid_gender = []
kid_live = []
kid_patient = []
kid_death = []
kid_number = []
kid_labour = []
kid_hospitalize_rec = []
kid_hospitalize_exp = []
kid_weight_mem = []
kid_weight = []
kid_height_mem = []
kid_height = []
kid_head_mem = []
kid_head = []

f_abortion_rec = []
f_ab_pregnancy_numebr = []
f_ab_mother_age = []
f_ab_pregnancy_age = []
f_abortion_reason = []


f_iufd_rec = []
f_iufd_pregnancy_numebr = []
f_iufd_mother_age = []
f_iufd_pregnancy_age = []
f_iufd_reason = []


for i in range(1,21):
    counselor_name.append(Field("counselor_{}".format(i),requires=IS_IN_SET(genetic_counselor, zero=None),label="نام مشاور {}".format(i),))    
    upload_fields_counselling.append(Field("upload_{}".format(i),"upload",label="آپلود فایل {}".format(i),uploadfolder='C:/Web2Py/applications/optimalinfosystem/static/images',uploadseparate=True)))

for j in range(1,11):
    counselor_gen_reason.append(Field("reason_{}".format(i),requires=IS_IN_SET(counselor_genetic_reasons, zero=None),label="علت".format(i),))    
    specialist_price.append(Field("price_{}".format(i),"string",label="هزینه".format(i),))    
    specialist_field.append(Field("field_{}".format(i),requires=IS_IN_SET(special_list, zero=None),label="تخصص".format(i),))    



for i in range(1,11):
    
    kid_name.append(Field("kid_{}_name".format(i), "string",label="نام فرزند درگیر عارضه",required=True),)        
    kid_id_code.append(Field("kid_{}_id_code".format(i), "string",label="کدملی",required=True),)        
    kid_birth.append(Field("kid_{}_birth".format(i), "string",label="تاریخ تولد",required=True),)  
    kid_gender.append(Field("kid_{}_gender".format(i), requires=IS_IN_SET(kid_genders, zero=None),label="جنسیت",required=True),) 
    kid_live.append(Field("kid_{}_live".format(i), requires=IS_IN_SET(live_con, zero=None),label="وضعیت جسمانی فعلی",required=True),) 
    kid_patient.append(Field("kid_{}_patient".format(i), "string",label="شرح بیماری"),)
    kid_death.append(Field("kid_{}_death".format(i), "string",label="علت فوت"), )
    kid_number.append(Field("kid_{}_number".format(i), "string",label="فرزند چندم",required=True), )
    kid_labour.append(Field("kid_{}labour".format(i), requires=IS_IN_SET(labour_con, zero=None),label="وضعیت زایمان",required=True), )
    kid_hospitalize_rec.append(Field("kid_{}_hospitalize_rec".format(i), requires=IS_IN_SET(yes_no_space, zero=None),label="سابقه بستری در دوران نوزادی",required=True), )
    kid_hospitalize_exp.append(Field("kid_{}_hospitalize_exp".format(i), "string",label="توضیحات",required=True), )

#   وضعیت جسمی هنگام تولد

    kid_weight_mem.append(Field("kid_{}_weight_mem".format(i), requires=IS_IN_SET(yes_no_space, zero=None),label="وزن را بخاطر دارد",required=True), )
    kid_weight.append(Field("kid_{}_weight".format(i), "string",label="وزن به کیلوگرم"), )
    kid_height_mem.append(Field("kid_{}_height_mem".format(i), requires=IS_IN_SET(yes_no_space, zero=None),label="وزن را بخاطر دارد",required=True), )
    kid_height.append(Field("kid_{}_height".format(i), "string",label="قد به سانتیمتر"), )
    kid_head_mem.append(Field("kid_{}_head_mem".format(i), requires=IS_IN_SET(yes_no_space, zero=None),label="وزن را بخاطر دارد",required=True), )
    kid_head.append(Field("kid_{}_head".format(i), "string",label="دور سر به سانتیمتر"), )


    

    
for i in range(1,6):
    
    f_abortion_rec.append(Field("f_abortion_rec_{}".format(i), requires=IS_IN_SET(yes_no_unknown, zero=None),label="سابقه سقط"),)
    f_ab_pregnancy_numebr.append(Field("f_ab_pregnancy_numebr_{}".format(i), "string",label="بارداری چندم"),)
    f_ab_mother_age.append(Field("f_ab_mother_age_{}".format(i), "string",label="سن مادر"),)
    f_ab_pregnancy_age.append(Field("f_ab_pregnancy_age_{}".format(i), "string",label="سن حاملگی"),)
    f_abortion_reason.append(Field("f_abortion_reason_{}".format(i), "string",label="علت"),)

    f_iufd_rec.append(Field("f_iufd_rec_{}", requires=IS_IN_SET(yes_no_unknown, zero=None),label="IUFD سابقه"),)
    f_iufd_pregnancy_numebr.append(Field("f_iufd_pregnancy_numebr_{}", "string",label="بارداری چندم"),)
    f_iufd_mother_age.append(Field("f_iufd_mother_age_{}", "string",label="سن مادر"),)
    f_iufd_pregnancy_age.append(Field("f_iufd_pregnancy_age_{}", "string",label="سن حاملگی"),)
    f_iufd_reason.append(Field("f_iufd_reason_{}", "string",label="علت"),)

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

    Field("probound_full_name", "string",label="نام و نام خانوادگی", required=True),
    Field("case_number", "string",label="شماره پرونده", writable=False, readable = False),
    Field("probound_id_code", "text",label="کدملی", required=True),
    Field("probound_gender", requires=IS_IN_SET(genders, zero=None),label="جنسیت", required=True),
    Field("probound_father_name", "string",label="نام پدر", required=True),
    Field("probound_birth_date", "string",label="تاریخ تولد", required=True),
    Field("probound_birth_pro", "string",label="استان", required=True),
    Field("probound_birth_city", "string",label="شهر", required=True),
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
    Field("son_health", "string",label="تعداد فرزندان پسر سالم",required=True),
    Field("son_patient", "string",label="تعداد فرزندان پسر بیمار",required=True),
    Field("son_death", "string",label="تعداد فرزندان پسر فوت شده",required=True),    
    Field("doughter_health", "string",label="تعداد فرزندان دختر سالم",required=True),
    Field("doughter_patient", "string",label="تعداد فرزندان دختر بیمار",required=True),
    Field("doughter_death", "string",label="تعداد فرزندان دختر فوت شده",required=True),    

#--------------------------------------------------------------------------------
#   if x = (son_patient +  son_death + doughter_patient + doughter_death + son_health + doughter_health) > 0 :
#       open required kid info for x number
#--------------------------------------------------------------------------------

    *kid_name[1:11],
    *kid_id_code[1:11],
    *kid_birth[1:11],
    *kid_gender[1:11],
    *kid_live[1:11],
    *kid_patient[1:11],
    *kid_death[1:11],
    *kid_number[1:11],
    *kid_labour[1:11],
    *kid_hospitalize_rec[1:11],
    *kid_hospitalize_exp[1:11],
    #   وضعیت جسمی هنگام تولد
    *kid_weight_mem[1:11],
    *kid_weight[1:11],
    *kid_height_mem[1:11],
    *kid_height[1:11],
    *kid_head_mem[1:11],
    *kid_head[1:11],

    migrate = True,
)

# ----------------------- Contact Section ------------------------------
db.define_table("contact_info",    
    Field("date", "date",label="تاریخ", writable = False),    
    Field("time", "time",label="زمان", writable = False),    
    signature,

    Field("case_number", "string",label="شماره پرونده", writable=False, readable = False), 

# اطلاعات تماس

    Field("address", "text",label="محل سکونت",required=True),
    Field("address_city", "text",label="شهرستان",required=True),
    Field("tel", "string",label="تلفن",required=True),    
    Field("cellphone", "string",label=" تلفن همراه",required=True),    
    Field("e_mail", "string",label="ایمیل"),

# نحوه آشنایی با مرکز

    Field("knowing_centre", requires=IS_IN_SET(center, zero=None),label="نحوه آشنایی با مرکز",required=True),  
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
    *f_abortion_rec[1:6],
    *f_ab_pregnancy_numebr[1:6],
    *f_ab_mother_age[1:6],
    *f_ab_pregnancy_age[1:6],
    *f_abortion_reason[1:6],

    *f_iufd_rec[1:6],
    *f_iufd_pregnancy_numebr[1:6],
    *f_iufd_mother_age[1:6],
    *f_iufd_pregnancy_age[1:6],
    *f_iufd_reason[1:6],

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
    *counselor_name[1:11],
    *counselor_gen_reason[1:11],
    *upload_fields_counselling[1:11],

    

  migrate = True,   

)

db.define_table("special_counseling_records",   
    Field("date", "date",label="تاریخ", writable = False),    
    Field("time", "time",label="زمان", writable = False),    
    signature,

    Field("case_number", "string",label="شماره پرونده", writable=False, readable = False), 
    *counselor_name[11:21],
    *specialist_field[1:11],
    *upload_fields_counselling[11:21],
    *specialist_price[1:11]

  migrate = True,   

)


# db.define_table('log', Field('event'),
#                         Field('event_time', 'datetime'),
#                         Field('severity', 'integer'))
