import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.list import ListView
from .models import *

myobj = []
myobjTong = []
lsttieude = []


class details:
    def __init__(self, link, noidung):
        self.link = link
        self.noidung = noidung


class news:
    def __init__(self, id, link, thoigian, tieude, mieuta, noidung, thoigianthucthi):
        self.id = id
        self.link = link
        self.thoigian = thoigian
        self.tieude = tieude
        self.mieuta = mieuta
        self.noidung = noidung
        self.thoigianthucthi = thoigianthucthi


# Create your views here.
mongo_client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
db = mongo_client.anhDung
col = db.TinTucChonLocNew


def getdata(request):
    if request.method == "POST":
        myobj = []
        lsttieude = []
        ngaythang = request.POST.get("datepicker1")
        format_str = '%m/%d/%Y'
        datetime_obj = datetime.datetime.strptime(ngaythang, format_str)
        ngay = datetime_obj.strftime('%Y-%m-%d')
        cursor1 = col.find(({"ThoiGian": str(ngay)}))
        mongo_docs1 = list(cursor1)
        if len(mongo_docs1) > 0:
            for doc in enumerate(mongo_docs1):
                mid = doc[1]["_id"]
                link = doc[1]["Link"]
                tieude = doc[1]["TieuDe"]
                thoigian = doc[1]["ThoiGian"]
                mieuta = doc[1]["MieuTa"]
                noidung = doc[1]["NoiDung"]
                phanloai = doc[1]["phanloai"]
                thoigianthucthi = doc[1]["ThoiGian"]

                if mieuta != "" and noidung != "" and phanloai =="ham" and thoigian == ngay:
                    if tieude not in lsttieude:
                        p = news(mid, link, thoigian, tieude, mieuta, noidung, thoigianthucthi)
                        lsttieude.append(tieude)
                        myobj.append(p)
                        myobjTong.append(p)
            return TemplateResponse(request, 'index.html', {'content': myobj})
        else:
            myobj1 = []
            return TemplateResponse(request, 'index.html', {'content': myobj1})


def homepage(request):
    return TemplateResponse(request, 'index.html', {'content': myobj})


def detail(request, id):
    m_baiviet = []
    if len(myobjTong) > 0:
        for doc in myobjTong:
            if str(doc.id) == str(id):
                link = doc.link
                noidung = doc.noidung
                p = details(link, noidung)
                m_baiviet.append(p)
                return TemplateResponse(request, 'detail.html', {'content': m_baiviet})
                break
    else:
        return TemplateResponse(request, 'detail.html', {'content': id})
