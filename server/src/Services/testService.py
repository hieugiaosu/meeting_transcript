from utils.bridge import rabbit_mq_client
async def test():
    rabbit_mq_client.basic_publish(
        exchange="",
        routing_key="whisper_inference",
        body="hello"
    )
    pass