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


def get_params(response, id):
    refundAmount = response['order']['YA028-5085515-5469931']['data']['orderRefund'][f'{id}']['refundAmount']
    refundState = response['order']['YA028-5085515-5469931']['data']['orderRefund'][f'{id}']['refundState']
    originalSku = response['order']['YA028-5085515-5469931']['data']['orderRefund'][f'{id}']['originalSku']
    applicant = response['order']['YA028-5085515-5469931']['data']['orderRefund'][f'{id}']['refundNotes']['applicant']
    applyAmount = response['order']['YA028-5085515-5469931']['data']['orderRefund'][f'{id}']['refundNotes'][
        'applyAmount']
    applyTime = response['order']['YA028-5085515-5469931']['data']['orderRefund'][f'{id}']['refundNotes']['applyTime']
    applyNotes = response['order']['YA028-5085515-5469931']['data']['orderRefund'][f'{id}']['refundNotes']['applyNotes']
    return refundAmount, refundState, originalSku, applicant, applyAmount, applyTime, applyNotes


def structure_params_data(response):
    params_temp = {}
    for i in range(get_long(response)):
        for id in get_id(response):
            params = get_params(response, id)
            temp = {
                f"orderData[updateOrderRefund][{id}][refundAmount]": params[0],
                f"orderData[updateOrderRefund][{id}][refundState]": params[1],
                f"orderData[updateOrderRefund][{id}][originalSku]": params[2],
                f"orderData[updateOrderRefund][{id}][refundNotes][applicant]": params[3],
                f"orderData[updateOrderRefund][{id}][refundNotes][applyAmount]": params[4],
                f"orderData[updateOrderRefund][{id}][refundNotes][applyTime]": params[5],
                f"orderData[updateOrderRefund][{id}][refundNotes][applyNotes]": params[6],
                f"orderData[updateOrderRefund][{id}][paymentCurrency]": "EUR",
            }
            params_temp.update(temp)

    params_temp["orderData[globalOrder]"] = "YA028-5085515-5469931"
    return params_temp

cron_value = '49 15 * * *'
cro_list = str(cron_value).split(' ')

print(len(cro_list))