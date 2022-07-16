from datetime import datetime
import json
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
        data_push_noti =  {
            "to": f"{line_id}",
            "messages": [{
                "type": "flex",
                "altText": "Confirm your order",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Confirm your order",
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
                                    "text": "order number"
                                },
                                {
                                    "type": "text",
                                    "text": f"1234",
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
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "วิธีการจ่ายตัง ",
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
                                "text": "รายการซื้อ",
                                "weight": "bold",
                                "size": "sm"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "-ค่าอาหาร",
                                    "size": "sm",
                                    "flex": 0,
                                    "weight": "bold",
                                    "margin": "none"
                                },
                                {
                                    "type": "text",
                                    "text": "{food price}",
                                    "size": "xs",
                                    "align": "end",
                                    "weight": "bold",
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
                                    "text": "-ค่าส่ง",
                                    "size": "sm",
                                    "flex": 0,
                                    "weight": "bold",
                                    "margin": "none"
                                },
                                {
                                    "type": "text",
                                    "text": "{delivery price}",
                                    "size": "xs",
                                    "align": "end",
                                    "weight": "bold",
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
                                        "text": "รวม",
                                        "size": "sm",
                                        "flex": 0,
                                        "weight": "bold",
                                        "margin": "none"
                                    },
                                    {
                                        "type": "text",
                                        "text": "200 บาท",
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
                        "uri": "{Link ...}"
                        }
                    }
                        ]
                    }
                }
            }]
        }    
        return
    
    def reject_message(self,meta_dat,tran):
        line_id = meta_dat["line_id"]
        branch_name = meta_dat["branch_name"]
        data_push_noti =  {
            "to": f"{line_id}",
            "messages": [{
                "type": "flex",
                "altText": "Reject your order",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Reject your order",
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
                                    "text": "order number"
                                },
                                {
                                    "type": "text",
                                    "text": f"1234",
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
                            }                  
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "sm",
                            "color": "#000000"
                        },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "สาเหตุ ",
                                    "size": "sm",
                                    "flex": 0,
                                    "weight": "bold",
                                    "margin": "none"
                                },
                                {
                                    "type": "text",
                                    "text": "{reason}",
                                    "size": "xs",
                                    "align": "end",
                                    "weight": "bold",
                                    "wrap": True
                                }
                                ]
                            }
                        ]
                    }
                }
            }]
        }
        return