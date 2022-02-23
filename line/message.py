from datetime import date,datetime
from line.form import WebForm
from dateutil.relativedelta import relativedelta
import json
class Message():
        
    def __init__(self, *args, **kwargs):
        return
    
    def next_maintanance(self, datetime):
        next_service = datetime + relativedelta(months=1)
        return next_service.strftime('%d/%m/%Y')

    def make_summary_item_to_noti(self,tran_detail):
        message_summary =  {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": f"{tran_detail.item.name} ",
                                    "size": "xxs",
                                    "flex": 0,
                                    "weight": "bold",
                                    "margin": "none"
                                },
                                {
                                    "type": "text",
                                    "text": f"{tran_detail.sell_price}",
                                    "size": "xxs",
                                    "align": "end",
                                    "weight": "bold",
                                    "offsetTop": "3px",
                                    "wrap": True
                                }
                                ]
                            }
        return message_summary

    def make_discount_price_to_noti(self,discount_price):
        message_discount =  {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "ส่วนลด ",
                                            "color": "#FF3E15",
                                            "size": "sm",
                                            "flex": 0,
                                            "weight": "bold",
                                            "margin": "none"
                                        },
                                        {
                                            "type": "text",
                                            "text": f"- {discount_price} บาท",
                                            "color": "#FF3E15",
                                            "size": "sm",
                                            "align": "end",
                                            "weight": "bold",
                                            "offsetTop": "3px",
                                            "wrap": True
                                        }
                                        ],

                                    }
        return message_discount

    def make_summary_price_to_noti(self,summary_price):
        message_discount =  {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "ยอดสุทธิ ",
                                            "color": "#00B900",
                                            "size": "md",
                                            "flex": 0,
                                            "weight": "bold",
                                            "margin": "none"
                                        },
                                        {
                                            "type": "text",
                                            "text": f"{summary_price} บาท",
                                            "color": "#00B900",
                                            "size": "md",
                                            "align": "end",
                                            "weight": "bold",
                                            "offsetTop": "3px",
                                            "wrap": True
                                        }
                                        ],

                                    }
        return message_discount

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
                                   "uri": "tel:033641010"
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
            count_num = 1
            # TODO debug , // [true true true]
            for ser_fact in lst_filt_chkbox:
                if ser_fact:
                    if count_num > 1:
                        service_detail = service_detail + ',' 
                    service_detail = service_detail + self.__getservicename(count_ser)
                    count_num = count_num + 1
                count_ser = count_ser + 1
            return service_detail

    def __getservicename(self, i):
         switcher={
                1:'เปลี่ยนถ่ายนํ้ามันเครื่อง พร้อมไส้กรอง',
                2:'ฟลัชชิ่ง ออยล์ ล้างตะกอนตกค้างภายในเครื่องยนต์',
                3:'เปลี่ยนน้ำมันเฟืองท้าย',
                4:'เปลี่ยนน้ำมันพวงมาลัยพาวเวอร์',
                5:'เปลี่ยนน้ำยาหม้อน้ำ (คูลแลนท์)',
                6:'เปลี่ยนไส้กรองอากาศ',
                7:'เปลี่ยนน้ำมันเบรค',
                8:'เปลี่ยนก้านปัดน้ำฝน',
                9:'เปลี่ยนน้ำมันเกียร์'
             }
         return switcher.get(i,"Invalid number of service")

    def makemessage_job_4_month(self,meta_dat,tran):
        line_id = meta_dat["line_id"]
        maintanace_day = self.next_maintanance(tran.appointed_date)
        data_push_noti =  {
            "to": f"{line_id}",
            "messages": [{
                "type": "flex",
                "altText": "แจ้งเตือนบำรุงรักษา",
                "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "แจ้งเตือนบำรุงรักษา",
                        "weight": "bold",
                        "color": "#FF3E15",
                        "size": "xxl"
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": "#000000"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "spacing": "xs",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": "ทะเบียน",
                                "size": "md",
                                "flex": 0,
                                "weight": "bold",
                                "margin": "none"
                            },
                            {
                                "type": "text",
                                "text": f"{tran.car.car_register}",
                                "size": "md",
                                "align": "end",
                                "weight": "bold"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": "ครบกำหนดบำรุงรักษา",
                                "size": "md",
                                "color": "#555555",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": f"{maintanace_day}",
                                "size": "md",
                                "color": "#111111",
                                "align": "end"
                            }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "จองคิวรับบริการ",
                            "align": "center",
                            "size": "xxl",
                            "weight": "bold",
                            "color": "#FFFFFF",
                            "action": {
                                "type": "uri",
                                "label": "action",
                                "uri": "https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=1655193304&redirect_uri=http://139.59.119.129/line/webhook?reqo=1,form&state=12345abcde&scope=profile%20openid&nonce=09876xyz"
                            }
                        }
                        ],
                        "backgroundColor": "#FF3E15",
                        "cornerRadius": "10px"
                    },
                    {
                        "type": "separator",
                        "margin": "xxl",
                        "color": "#000000"
                    },
                    {
                        "type": "text",
                        "text": "ขอบคุณที่ใช้บริการ",
                        "align": "center",
                        "margin": "sm",
                        "size": "lg",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "Shell Helix Oilchange+",
                        "margin": "none",
                        "size": "lg",
                        "align": "center",
                        "weight": "bold"
                    },
                    {
                        "type": "separator",
                        "color": "#000000",
                        "margin": "xs"
                    },
                    {
                        "type": "text",
                        "text": "สิทธิพิเศษเฉพาะคุณ จองคิว วันนี้",
                        "align": "center",
                        "color": "#f75836",
                        "margin": "sm",
                        "weight": "bold",
                        "size": "sm",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": "รับส่วนลด ฟลัชชิ่งออยล์ ทันที 100 บาท",
                        "align": "center",
                        "color": "#f75836",
                        "margin": "none",
                        "weight": "bold",
                        "size": "sm",
                        "wrap": True
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
        return data_push_noti

    def makemessage_job_done(self,meta_dat,tran):
        line_id = meta_dat["line_id"]
        branch_name = meta_dat["branch_name"]
        tran_details = tran.sale_detail.all()
        total_price = 0
        summary_price = 0
        for detail in tran_details:
            total_price += detail.sell_price
        summary_price = total_price - tran.discount_price
        data_push_noti =  {
            "to": f"{line_id}",
            "messages": [{
                "type": "flex",
                "altText": "ใบเสร็จรับบริการ (e-Receipt)",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "ดำเนินการสำเร็จ",
                            "weight": "bold",
                            "color": "#FF3E15",
                            "size": "xxl"
                        },
                        {
                            "type": "separator",
                            "margin": "lg",
                            "color": "#000000"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "spacing": "xs",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "size": "sm",
                                    "flex": 0,
                                    "weight": "bold",
                                    "margin": "none",
                                    "text": "ทะเบียน"
                                },
                                {
                                    "type": "text",
                                    "text": f"{tran.car.car_register}",
                                    "size": "sm",
                                    "align": "end",
                                    "weight": "bold"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "วันที่",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0,
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": f"{datetime.strftime(tran.appointed_date, '%d/%m/%Y')}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end",
                                    "weight": "bold"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "สาขา ",
                                    "size": "sm",
                                    "flex": 0,
                                    "weight": "bold",
                                    "margin": "none"
                                },
                                {
                                    "type": "text",
                                    "text": f"{branch_name}",
                                    "size": "xs",
                                    "align": "end",
                                    "weight": "bold",
                                    "wrap": True
                                }
                                ]
                            },
                            {
                                "type": "text",
                                "text": "รายการรับบริการ",
                                "weight": "bold",
                                "size": "sm"
                            }                    
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [                            
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "รวม",
                                        "size": "sm",
                                        "flex": 0,
                                        "weight": "bold",
                                        "margin": "none"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{total_price} บาท",
                                        "size": "sm",
                                        "align": "end",
                                        "weight": "bold",
                                        "wrap": True
                                    }
                                ]
                            }]
                            }
                            ],
                            "margin": "md"
                        },
                        {
                            "type": "separator",
                            "margin": "sm",
                            "color": "#000000"
                        },
                        {
                            "type": "text",
                            "text": "ขอบคุณที่ใช้บริการ",
                            "align": "center",
                            "margin": "sm",
                            "size": "lg",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "Shell Helix Oilchange+",
                            "margin": "none",
                            "size": "lg",
                            "align": "center",
                            "weight": "bold"
                        },
                        {
                            "type": "separator",
                            "color": "#000000",
                            "margin": "xs"
                        },
                        {
                            "type": "text",
                            "text": "สิทธิพิเศษเฉพาะคุณ ซื้อกาแฟ 1 แถม 1",
                            "align": "center",
                            "color": "#f75836",
                            "margin": "sm",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "สิทธินี้ใช้ได้ภายใน 7 วัน หลังจากวันที่ทำรายการ",
                            "align": "center",
                            "color": "#f75836",
                            "margin": "none",
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True
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
        for detail in tran_details:
            message_summary = self.make_summary_item_to_noti(detail)
            data_push_noti['messages'][0]['contents']['body']['contents'][2]['contents'].append(message_summary)
        if tran.discount_price > 0:
            message_discount = self.make_discount_price_to_noti(tran.discount_price)
            data_push_noti['messages'][0]['contents']['body']['contents'][3]['contents'].append(message_discount)
            message_summary_price = self.make_summary_price_to_noti(summary_price)
            data_push_noti['messages'][0]['contents']['body']['contents'][3]['contents'].append(message_summary_price)
        return data_push_noti