from lambdas.cloudwatch_subscription_lambda import *

def event() -> dict:
    return {"awslogs": {"data": "H4sIAAAAAAAAAIVRy27bMBD8FYPoMYSWFJ+6qa1tBIlbwFKbQ2oUlEQpBGRJpaS6RZB/z7oPoLdiL8vhYnZ25pmc/Ty7zpc/J08y8j4v86+HbVHk+y25IeNl8BFhxbgwqeVCaUC4H7t9HNcJfxJ3mZPenavGJRXiFN/U925eQj17F+sn2obon8bZUzfRMoau83G3DvUSxoGyWzgc3vLy0/HD3fE3c7FE785IzYGZhLGE2eTxzX1ebovyJHiTShCqraARjXOWs1ZVDUArGu10ihTzWs11DNOVfxf6xceZZI/k/+IC7S7U/3Dnqfe07se1ubgFR95d24dre4/q/mGnD9zsgB0+3u13lpx+qd9+98NyXfhMQoNHpEIA56A5CCxpjbESpJESLbUcuGFKM6YYgAapU2VNiqU5HrIEzGZBOSRjUnCFCfDUGnbzNzOkL8r8WG6O/tuKo7dNtmGmNRWTmvqaA2XMG1q1WlJoK6vrSijg9eYzeoL6s80fW78M5OX08grvTTW4DAIAAA=="}}

def test_decode_event():
    assert decode_event(event()) == {'messageType': 'DATA_MESSAGE', 'owner': '612483924670', 'logGroup': '/aws/lambda/blog-aws-elasticsearch-firehose-ap-TriggerFunction-1I0MMB2TURNKR', 'logStream': '2018/11/19/[$LATEST]42d35046fb0d4daa921f6bd00f4d7a73', 'subscriptionFilters': ['blog-aws-elasticsearch-firehose-api-gw-example-cloudwatch-CloudWatchLogSubscription-W28F01MOKGF9'], 'logEvents': [{'id': '34402207204040598895058556129202816711610070573698383872', 'timestamp': 1542648323981, 'message': 'START RequestId: 18f8b157-ec20-11e8-bf75-0fb97cb4602c Version: $LATEST\n'}]}

