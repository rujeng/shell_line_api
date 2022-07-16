from datetime import datetime
import json
from unicodedata import decimal
class line_message():

    def __init__(self, *args, **kwargs):
        return

    def order_message(self,meta_dat,tran): # location 
        line_id = meta_dat["line_id"]
        branch_name = meta_dat["branch_name"]
        data_push_noti =  {
            "to": f"{line_id}",
            "messages": [{
                "type": "flex",
                "altText": "โปรดรอยืนยันออเดอร์",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "โปรดรอยืนยันออเดอร์",
                            "weight": "bold",
                            "color": "#DC493F",
                            "size": "xl"
                        },
                        {
                            "type": "text",
                            "text": f"{branch_name}",
                            "weight": "bold",
                            "color": "#000000",
                            "margin": "lg",
                            "size": "md"
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
                                    "text": "order number",
                                    "color": "#A0ABB1"
                                },
                                {
                                    "type": "text",
                                    "text": f"{tran.id}",
                                    "size": "sm",
                                    "align": "end",
                                    "weight": "bold",
                                    "color": "#A0ABB1"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "เวลาสั่ง",
                                    "size": "sm",
                                    "color": "#A0ABB1",
                                    "flex": 0,
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": f"{datetime.strftime(tran.created_at, '%m/%d/%Y, %H:%M')}",
                                    "size": "sm",
                                    "color": "#A0ABB1",
                                    "align": "end",
                                    "weight": "bold"
                                }
                                ]
                            }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "sm",
                            "color": "#000000"
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
    
    def confirm_message(self,meta_dat,tran):
        line_id = meta_dat["line_id"]
        branch_name = meta_dat["branch_name"]
        distance = meta_dat["distance"]
        distance_price = meta_dat["distance_price"]
        total_price_food = meta_dat["total_price_food"]
        data_push_noti =  {
            "to": f"{line_id}",
            "messages": [{
                "type": "flex",
                "altText": "ออเดอร์กำลังดำเนินการ",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "ออเดอร์กำลังดำเนินการ",
                            "weight": "bold",
                            "color": "#DC493F",
                            "size": "xl"
                        },
                        {
                            "type": "text",
                            "text": f"{branch_name}",
                            "weight": "bold",
                            "color": "#000000",
                            "margin": "lg",
                            "size": "md"
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
                                    "text": "order number",
                                    "color": "#A0ABB1"
                                },
                                {
                                    "type": "text",
                                    "text": f"{tran.id}",
                                    "size": "sm",
                                    "align": "end",
                                    "weight": "bold",
                                    "color": "#A0ABB1"
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
                                    "color": "#A0ABB1",
                                    "flex": 0,
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": f"{datetime.strftime(tran.created_at, '%m/%d/%Y, %H:%M')}",
                                    "size": "sm",
                                    "color": "#A0ABB1",
                                    "align": "end",
                                    "weight": "bold"
                                }
                                ]
                            },
                            {
                            "type": "separator",
                            "margin": "lg",
                            "color": "#000000"
                            },
                            {
                                "type": "text",
                                "text": "รายการสั่งซื้อ",
                                "weight": "bold",
                                "size": "sm"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "- ค่าอาหาร",
                                    "size": "sm",
                                    "flex": 0,
                                    "margin": "none"
                                },
                                {
                                    "type": "text",
                                    "text": f"{total_price_food} บาท",
                                    "size": "xs",
                                    "align": "end",
                                    "wrap": True
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "- ค่าจัดส่ง",
                                    "size": "sm",
                                    "flex": 0,
                                    "margin": "none"
                                },
                                {
                                    "type": "text",
                                    "text": f"{float(distance_price)} บาท",
                                    "size": "xs",
                                    "align": "end",
                                    "wrap": True
                                }
                                ]
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
                                        "text": "จำนวนเงินที่ต้องชำระ",
                                        "size": "sm",
                                        "flex": 0,
                                        "weight": "bold",
                                        "margin": "none",
                                        "color": "#DC493F"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{float(total_price_food)+float(distance_price)} บาท",
                                        "size": "sm",
                                        "align": "end",
                                        "weight": "bold",
                                        "color": "#DC493F",
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
                            "margin": "lg",
                            "color": "#000000"
                        },
                        {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "วิธีการชำระเงิน",
                                    "size": "sm",
                                    "flex": 0,
                                    "weight": "bold",
                                    "margin": "none"
                                },
                                {
                                    "type": "text",
                                    "text": f"{self.mapping_payment_method(tran.payment_method)}",
                                    "size": "xs",
                                    "align": "end",
                                    "weight": "bold",
                                    "wrap": True
                                }
                                ]
                        }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "uri",
                        "label": "View More Detail",
                        "uri": "https://www.google.co.th"
                        }
                    }
                        ]
                    }
                }
            }]
        }    
        return data_push_noti
    
    def reject_message(self,meta_dat,tran): # location 
        line_id = meta_dat["line_id"]
        branch_name = meta_dat["branch_name"]
        comment = meta_dat["comment"]
        data_push_noti =  {
            "to": f"{line_id}",
            "messages": [{
                "type": "flex",
                "altText": "ออเดอร์ของคุณถูกยกเลิก",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "ออเดอร์ของคุณถูกยกเลิก",
                            "weight": "bold",
                            "color": "#DC493F",
                            "size": "xl"
                        },
                        {
                            "type": "text",
                            "text": f"{branch_name}",
                            "weight": "bold",
                            "color": "#000000",
                            "margin": "lg",
                            "size": "md"
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
                                    "text": "order number",
                                    "color": "#A0ABB1"
                                },
                                {
                                    "type": "text",
                                    "text": f"{tran.id}",
                                    "size": "sm",
                                    "align": "end",
                                    "weight": "bold",
                                    "color": "#A0ABB1"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "เวลาสั่ง",
                                    "size": "sm",
                                    "color": "#A0ABB1",
                                    "flex": 0,
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": f"{datetime.strftime(tran.created_at, '%m/%d/%Y, %H:%M')}",
                                    "size": "sm",
                                    "color": "#A0ABB1",
                                    "align": "end",
                                    "weight": "bold"
                                }
                                ]
                            }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "lg",
                            "color": "#000000"
                        },
                                                {
                            "type": "text",
                            "text": f"สาเหตุ : {comment}",
                            "weight": "bold",
                            "color": "#DC493F",
                            "margin": "lg",
                            "size": "md"
                        },
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

    def mapping_payment_method(self,payment_method):
            str_payment_method = ""
            if payment_method == '1':
                str_payment_method = "เงินสด"
            elif payment_method == '2':
                str_payment_method = "โอนเงิน"
            return str_payment_method
        