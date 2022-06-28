from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .forms import Captcha, Organization, DataNeed, ContactPersonal
# Create your views here.
from .models import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import zipfile
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import os, sys
from django.views.decorators.csrf import csrf_exempt

def upload_file(request, name_input_field):
    if name_input_field in request.FILES:
        files = request.FILES[name_input_field]
        path = default_storage.save(f"req/{files.name}", ContentFile(files.read()))
        return path
    return None

def send_req_to_operator(organization_post, contact_person, data_need):
    requester = DataRequester(email=contact_person.cleaned_data['contacts_email'])
    requester.save()
    per_reqester = DataRequesterPersonal(firstname=contact_person.cleaned_data['contacts_firstname'],
                                         lastname=contact_person.cleaned_data['contacts_secname'],
                                         surname=contact_person.cleaned_data['contacts_surname'],
                                         data_requester=requester
                                         )
    per_reqester.save()
    per_phone = DataRequesterPhone(phone=contact_person.cleaned_data['contacts_phone'],
                                   data_requester_personal=per_reqester)
    per_phone.save()
    organization = RequesterOrganization(name=organization_post.cleaned_data['organization'],
                                         data_requester_personal=per_reqester
                                         )
    organization.save()

    org_boss = RequesterOrganizationBoss(firstname=organization_post.cleaned_data['boss_firstname'],
                                         lastname=organization_post.cleaned_data['boss_secname'],
                                         surname=organization_post.cleaned_data['boss_surname'],
                                         requester_organization=organization
                                         )
    org_boss.save()
    data_mode = "Ретроспективно"
    if data_need.cleaned_data['choice_data_type'] == 'realtime':
        data_mode = "Реальное время"
    rets = default_storage.save(f"req/{data_need.cleaned_data['add_file'].name}", ContentFile(data_need.cleaned_data['add_file'].read()))
    request = RequestData(data_requester=requester,
                          request_file=rets,
                          commentary_to_file=data_need.cleaned_data['req_comment'],
                          type_data=data_mode,
                          basis=None
                          )
    request.save()
    return True

def send_email (adresse, subject, body, from_email= "django_req@gsras.com", host = "mailhost.obn.gsras.ru"):
    import smtplib
    server = smtplib.SMTP(host)
    if isinstance(adresse, str):
        server.sendmail(from_email, adresse,  "Subject: " + subject + "\n\n" + body)
    if isinstance(adresse, list):
        for value in adresse:
            server.sendmail(from_email, value, "Subject: "+subject+"\n\n"+body)
    server.quit()


def see_full_news (request, id):
    news = News.objects\
        .select_related("newsimagecontent", "newsmappointfloat")\
        .filter(id= id)\
        .values("id", "body", "title","created", "newsimagecontent__image_storage", "newsmappointfloat__lon", "newsmappointfloat__lat")

    print (news)
    context = {"current_news": news}
    return render(request, 'gsras/full_news.html', context)

def index (request):

    news = News.objects.select_related ("newsimagecontent").values ("id", "body", "title", "newsimagecontent__image_storage")
    context = {"news_block": news}
    return render(request, 'gsras/index.html', context)

def struct (request):
    context = {}
    return render(request, 'gsras/structure.html', context)

def geoform(request):
    captch = Captcha()
    organization = Organization()
    contact_person = ContactPersonal()
    data_need = DataNeed()

    context = {
                "toReqLink":  "",
                "captcha": captch,
                "correct": "",
                "organization": organization,
                "data_need":data_need,
                "contact_person": contact_person
               }
    if request.user.is_authenticated:
        context["toReqLink"] = "<a class = 'btn btn-primary' href = 'req_form'> Список заявок </a>"
    if request.method == 'POST':
        captch = Captcha(request.POST)
        organization = Organization(request.POST)
        contact_person = ContactPersonal(request.POST)
        data_need = DataNeed(request.POST, request.FILES)
        if  data_need.is_valid() and captch.is_valid() and organization.is_valid() and contact_person.is_valid():
            send_req_to_operator(organization, contact_person, data_need)
            context['correct'] = '<div class="container col-12 mt-3 border  text-center bg-primary text-white">' \
                                 '<h4>Заявка отправлена на обработку</h4>' \
                                 '</div>'
            user = get_user_model().objects.filter(username='reader').values('email')
            if user:
                for item in user:
                    send_email(item['email'], "Seismo Data req from user", f"http://{request.get_host()}/req_form")

        else:
            context['correct'] = '<div class="container col-12 mt-3 border  text-center bg-danger text-white">' \
                                 '<h4>Ошибка заполнения формы</h4>' \
                                 '</div>'

    return render(request, 'gsras/geofrom.html', context)


def requsets_list(request):

    if not request.user.is_authenticated:
        return index(request)
    rd = RequestData.objects.select_related("data_requester")\
        .order_by("-id")\
        .values("date_time_create", "request_file", "commentary_to_file", "type_data", "basis", "data_requester__email", "data_requester__id")
    for item in rd:
        sub_sel = DataRequesterPhone.objects.select_related ("data_requester_personal")\
            .filter (data_requester_personal__data_requester__id = item.get("data_requester__id"))\
            .values('phone',
                    "data_requester_personal__firstname",
                    "data_requester_personal__lastname",
                    "data_requester_personal__surname")
        boss = RequesterOrganizationBoss.objects.select_related("requester_organization") \
            .filter (requester_organization__data_requester_personal__data_requester__id = item.get("data_requester__id"))\
            .values(
                    "firstname",
                    "lastname",
                    "surname",
                    "requester_organization__name")
        for it in sub_sel:
            item.update(it)
        for it in boss:
            item.update(it)
    context = {"reqs": rd}
    return render(request, 'gsras/req_form.html', context)      
    
    
def GetFileName(st,format):
    filename = "GSRAS_"
    filename=filename+str(st[0].stats['network'])+"_"
    filename=filename+str(st[0].stats['station'])
    if 'css' not in format:
        filename=filename+".msd"
    return filename

def ListFilterW(lst):
    lst2=[]
    for i in lst:
        if ".w" in i:
            lst2.append(i)
    return lst2

def main_page(request):
    return render(request,'gsras/main_page.html',{})

@csrf_exempt
def dataselect(request):
    if request.method =="POST":
        try:
            client = Client("http://172.20.1.37:8090")
            t = UTCDateTime("2022-02-01T00:00:00")
            starttime = request.POST['starttime']
            endtime = request.POST['endtime']
            startdate = request.POST['startdate']
            enddate = request.POST['enddate']

            starttime = UTCDateTime(startdate + "T" + starttime)
            endtime = UTCDateTime(enddate + "T" + endtime)

            if len(request.POST['network'])>0:
                net = request.POST['network']
            else:
                net="*"
            if len(request.POST['station']) > 0:
                sta = request.POST['station']
            else:
                sta = "*"
            if len(request.POST['location']) > 0:
                loc = request.POST['location']
            else:
                loc = "*"
            if len(request.POST['channel']) > 0:
                ch = request.POST['channel']
            else:
                ch = "*"

            #nodata = request.POST['nodata']

            st = client.get_waveforms(net, sta, loc, ch, starttime, endtime,attach_response=True)
            FName=GetFileName(st,request.POST['format'])
            st.write(FName,format="MSEED")


            if 'css3' in request.POST['format'].lower():
                if 'win' in sys.platform:
                    os.system("wavetapc -d=w {}".format(FName))
                else:
                    os.system("./waveTapc -d=w {}".format(FName))

                flist=ListFilterW(os.listdir())
                with zipfile.ZipFile('{}.zip'.format(FName), 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for obj in flist:
                        zipf.write(obj)

                response = HttpResponse(open(FName+".zip",'rb'))
                response['Content-Type'] = 'application/zip'
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(FName+".zip")
                for obj in flist:
                    os.remove(obj)
                os.remove(FName+".zip")
            else:
                response = HttpResponse(open(FName,'rb'))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(FName)

            os.remove(FName)
            return response
        except:
            return render(request,'fdsnws/error.html',{"message":"Error! введите корректные данные"})
    return render(request,'gsras/dataselect.html',{})

@csrf_exempt
def station(request):
    if request.method == "POST":
        try:
            try:
                startdate = UTCDateTime(request.POST['startdate'])
                enddate = UTCDateTime(request.POST['enddate'])
            except:
                startdate=UTCDateTime(2000,1,1)
                enddate=UTCDateTime().now()

            if len(request.POST['network']) > 0:
                net = request.POST['network']
            else:
                net = "*"
            if len(request.POST['station']) > 0:
                sta = request.POST['station']
            else:
                sta = "*"
            if len(request.POST['location']) > 0:
                loc = request.POST['location']
            else:
                loc = "*"
            if len(request.POST['channel']) > 0:
                ch = request.POST['channel']
            else:
                ch = "*"
            loc1=request.POST['location1']
            if 'box' in loc1:
                minlat=request.POST['minlatitude']
                maxlat = request.POST['maxlatitude']
                minlon = request.POST['minlongitude']
                maxlon = request.POST['maxlongitude']
            elif 'cir' in loc1:
                lat=request.POST['latitude']
                lon=request.POST['longitude']
                minrad=request.POST['minradius']
                maxrad=request.POST['maxradius']
            else:
                pass
            form=request.POST['format']
            nodata = request.POST['nodata']
            level=request.POST['level']

            client = Client("http://172.20.1.37:8090")


            inv=client.get_stations(network=net,station=sta,location=loc,channel=ch,starttime=startdate,endtime=enddate,level=level)

            if 'box' in loc1:
                inv=client.get_stations(network=net,station=sta,location=loc,channel=ch,starttime=startdate,endtime=enddate,level=level, minlatitude=minlat,maxlatitude=maxlat,
                                        minlongitude=minlon,maxlongitude=maxlon)

            if 'cir' in loc1:
                inv=client.get_stations(network=net,station=sta,location=loc,channel=ch,starttime=startdate,endtime=enddate,level=level,
                                        longitude=lon,latitude=lat,minradius=minrad,maxradius=maxrad)


            inv.write("GSRAS_inv.xml",format="STATIONXML")
            response = HttpResponse(open("GSRAS_inv.xml","r",encoding="utf-8"))
            if "XML" in form:
                response['Content-Type'] = 'text/xml'
            else:
                response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename="GSRAS_inv.xml"'
            os.remove("GSRAS_inv.xml")
            return response
        except:
            return render(request, 'gsras/error.html', {"message": "Error! введите корректные данные"})

    return render(request,'gsras/station.html',{})
