# meeting_transcript

# run a test locally

<h2>To start up the server</h2>
go to the src folder in server
start rabbit mq and redis:


start rabbit-mq: docker run --rm -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=12345 rabbitmq:3.10-management
start redis: docker run --rm -p 6379:6379 redis:latest
start server: python server.py