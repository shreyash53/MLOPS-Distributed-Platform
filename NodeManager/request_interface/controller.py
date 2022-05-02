from json import loads
from multiprocessing import connection
from socket import timeout
from node_manager.model import RunningServices
from mongoengine.queryset.visitor import Q
from requests import post
from kafka import KafkaConsumer,TopicPartition
from utilities.constants import SLCM_URL, kafka_url
# ###
# import kafka
# ###

consumer = KafkaConsumer(
    bootstrap_servers=[kafka_url],
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)



def build_url(model_):
    if model_.node.nodeUrl:
        return model_.node.nodeUrl
    return '{}:{}'.format(model_.node.nodeIpAddress, model_.node.nodePortNo)

def get_model_data(modelId, data, route):
    print("ModelId: ", modelId)
    # model_ = RunningServices.objects.filter(
    #     Q(serviceId = modelId) &
    #     Q(serviceType = 'model')
    # )
    response = post(SLCM_URL+'/service_lookup', json={
        "service_id" : modelId,
        "service_type" : "model"
    })
    if not response.status_code == 200:
        print('No model found')
        return "No data"
    response = response.json()
    # url = build_url(model_.first())
    url = response['url']
    # url = 'http://localhost:12000'
    print("URL: ",url)
    res = post(url='{}/{}'.format(url, route), json=data).json()
    print("Res ", res)
    return res


def get_sensor_data(sensor_build_id):
    try:
        print('sensor_bind_id: ', sensor_build_id)
        sensor_topic = 'S_{}'.format(sensor_build_id)

        tp = TopicPartition(sensor_topic,int(0))
        consumer.assign([tp])
        tmp = consumer.end_offsets([tp])
        print("tmp: ", tmp)
        offset=0
        for key in tmp:
            # print(tmp[key])
            offset = tmp[key]

        # print("Offset: ",offset)
        if offset > 0:
            consumer.seek(tp,offset-2)

        print('connection successfull')
        for data in consumer:
            print('data recieved in sensor', data.value)
            return data.value

    except Exception as e:
        print('Error in request_interface.get_sensor_data', e)

####
# if __name__ == "__main__":
#     print("Sensor 1: ", get_sensor_data("487548"))
    # print("Sensor 1: ", get_sensor_data("49992"))
    # print("Sensor 1: ", get_sensor_data(3))
    # print("Sensor 1: ", get_sensor_data(4))
###