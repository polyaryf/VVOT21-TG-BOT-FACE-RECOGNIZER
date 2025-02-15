from json import loads
def entrypoint(event, context):
    message = loads(event["messages"][0]["details"]["message"]["body"])
