from datetime import date
from line.form import WebForm
class Message():
        
    def __init__(self, *args, **kwargs):
        return
    
    def makemessage(self,meta_dat,car):
        fullname = meta_dat["fullname"]
        line_id = meta_dat["line_id"]
        mobileno = meta_dat["mobileno"]
        branch_name = meta_dat["branch_name"]
        date = meta_dat["date"]
        time = meta_dat["time"]
        # brand = meta_dat["brand"]
        # model = meta_dat["model"]
        service_detail = meta_dat["service_detail"]

        data_push_noti = {
            "to": f"{line_id}",
            "messages": [{
                "type": "flex",
                "altText": "แบบฟอร์มยืนยันการจอง",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [{
                            "type": "text",
                            "text": "จองสำเร็จแล้ว",
                            "color": "#FF3E15",
                            "weight": "bold",
                            "size": "xl",
                            "wrap": True
                        },
                            {
                            "type": "separator",
                            "margin": "xxl"
                        },
                            {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "xxl",
                            "spacing": "sm",
                            "contents": [{
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [{
                                    "type": "text",
                                    "text": "ผู้จอง:",
                                    "size": "md",
                                    "color": "#777777",
                                    "flex": 0
                                },
                                    {
                                    "type": "text",
                                    "text": f"{fullname}",
                                    "size": "md",
                                    "color": "#777777",
                                    "align": "end",
                                    "wrap": True
                                }
                                ]
                            },
                                {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [{
                                    "type": "text",
                                    "text": "ติดต่อ:",
                                    "size": "md",
                                    "color": "#777777",
                                    "flex": 0
                                },
                                    {
                                    "type": "text",
                                    "text": f"{mobileno}",
                                    "size": "md",
                                    "color": "#777777",
                                    "align": "end",
                                    "wrap": True
                                }
                                ]
                            },
                                {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [{
                                    "type": "text",
                                    "text": "**สาขาที่จอง:",
                                    "size": "md",
                                    "color": "#777777",
                                    "flex": 0
                                },
                                    {
                                    "type": "text",
                                    "text": f"{branch_name}",
                                    "size": "md",
                                    "color": "#777777",
                                    "align": "end",
                                    "wrap": True
                                }
                                ]
                            },
                                {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [{
                                    "type": "text",
                                    "text": "วัน, เวลาที่จอง:",
                                    "size": "md",
                                    "color": "#777777",
                                    "flex": 0
                                },
                                    {
                                    "type": "text",
                                    "text": f"{date} , {time}",
                                    "size": "md",
                                    "color": "#777777",
                                    "align": "end",
                                    "wrap": True
                                }
                                ]
                            },
                                {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [{
                                    "type": "text",
                                    "text": "  "
                                }]
                            },
                                {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [{
                                    "type": "text",
                                    "text": "ยี่ห้อรถ:",
                                    "size": "md",
                                    "color": "#777777",
                                    "flex": 0
                                },
                                    {
                                    "type": "text",
                                    "text": f"{car.model.brand.name}",
                                    "size": "md",
                                    "color": "#777777",
                                    "align": "end",
                                    "wrap": True
                                }
                                ]
                            },
                                {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [{
                                    "type": "text",
                                    "text": "รุ่น-ปี:",
                                    "size": "md",
                                    "color": "#777777",
                                    "flex": 0
                                },
                                    {
                                    "type": "text",
                                    "text": f"{car.model.name}",
                                    "size": "md",
                                    "color": "#777777",
                                    "align": "end",
                                    "wrap": True
                                }
                                ]
                            },
                                {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [{
                                    "type": "text",
                                    "text": "เข้ารับบริการ:",
                                    "size": "md",
                                    "color": "#777777",
                                    "flex": 0
                                },
                                    {
                                    "type": "text",
                                    "text": f"{service_detail}",
                                    "size": "md",
                                    "color": "#777777",
                                    "align": "end",
                                    "wrap": True
                                }
                                ]
                            },
                                {
                                "type": "separator",
                                "margin": "xxl"
                            }, {
                                 "type": "button",
                                 "style": "primary",
                                 "color": "#FF3E15",
                                  "action": {
                                  "type": "uri",
                                  "label": "ติดต่อเจ้าหน้าที่",
                                   "uri": "tel:0970968653"
                                }
                            }
                            ]
                        }
                        ]
                    },
                    "styles": {
                        "footer": {
                            "separator": True
                        }
                    }
                }
            }]
        }

        data_notify = f"จองสำเร็จแล้ว\n\nผู้จอง: {fullname}\nติดต่อ: {mobileno}\n**สาขาที่จอง: {branch_name}\nวัน, เวลาที่จอง: {date} , {time}\n\nยี่ห้อรถ: {car.model.brand.name}\nรุ่น-ปี: {car.model.name}\nเข้ารับบริการ: {service_detail}"
        
        return data_push_noti,data_notify

    def makeservice_detail(self, request):
        form = WebForm(request.POST)
        if form.is_valid():
            lst_filt_chkbox = [form.cleaned_data[key] for key in form.cleaned_data]
            service_detail = ''
            count_ser = 1
            # TODO debug ,
            for ser_fact in lst_filt_chkbox:
                if ser_fact:
                    if count_ser > 1:
                        service_detail = service_detail + ',' 
                    service_detail = service_detail + self.__getservicename(count_ser)
                count_ser = count_ser + 1
            return service_detail

    def __getservicename(self, i):
         switcher={
                1:'เปลี่ยนถ่ายนํ้ามันเครื่อง พร้อมไส้กรอง',
                2:'ฟลัชชิ่ง ออยล์ ล้างตะกอนตกค้างภายในเครื่องยนต์',
                3:'เปลี่ยนน้ำมันเกียร์',
                4:'เปลี่ยนน้ำมันเฟืองท้าย',
                5:'เปลี่ยนน้ำมันพวงมาลัยพาวเวอร์',
                6:'เปลี่ยนน้ำยาหม้อน้ำ (คูลแลนท์)',
                7:'เปลี่ยนไส้กรองอากาศ',
                8:'เปลี่ยนน้ำมันเบรค',
                9:'เปลี่ยนก้านปัดน้ำฝน'
             }
         return switcher.get(i,"Invalid number of service")
