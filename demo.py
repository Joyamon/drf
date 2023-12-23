# # 根据汇总单号，获取订单退款信息id，获取汇总单号
import requests
import json


def select_Order():
    url = "http://oms.dev.yafex.cn/?c=show_infoMgmt_ebay_order&a=getOrderDetail"
    headers = {
        "cookie": "of_base_language[name]=ZH; PHPSESSID=39kgomvfhfdat93ktnn7vnjre8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    payloads = {
        "data[]": "YA028-5085515-5469931"
    }
    response = requests.post(url=url, data=payloads, headers=headers)
    return response.json()


def get_long(response):
    """
    获取orderRefund长度

    :param response: select_Order数据的响应结果
    :return:
    """
    return len(response['order']['YA028-5085515-5469931']['data']['orderRefund'])


def get_id(response):
    """
    获取orderRefund的ids
    :param response:
    :return:
    """
    ids = []
    for id in response["order"]['YA028-5085515-5469931']['data']['orderRefund']:
        ids.append(id)
    return ids


def structure_params_data(response):
    params_temp={}
    for i in range(get_long(response)):
        for id in get_id(response):
            temp = {
                f"orderData[updateOrderRefund][{id}][refundAmount]": 400,
                f"orderData[updateOrderRefund][{id}][refundState]": 1,
                f"orderData[updateOrderRefund][{id}][originalSku]": "UUU0152825004",
                f"orderData[updateOrderRefund][{id}][refundNotes][applicant]": "曹阳",
                f"orderData[updateOrderRefund][{id}][refundNotes][applyAmount]": 300,
                f"orderData[updateOrderRefund][{id}][refundNotes][applyTime]": "2023-12-23 11:23:10",
                f"orderData[updateOrderRefund][{id}][refundNotes][applyNotes]": "BuyerCancelled",
                f"orderData[updateOrderRefund][{id}][paymentCurrency]": "EUR",
            }
            params_temp.update(temp)

    params_temp["orderData[globalOrder]"] = "YA028-5085515-5469931"
    return params_temp


print(structure_params_data(select_Order()))