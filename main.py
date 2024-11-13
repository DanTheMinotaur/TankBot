from lib.web import dns_handler, app, start_access_point
from lib.motor import DCMotor
import asyncio


m1 = DCMotor(9, 10)
m2 = DCMotor(6,7)

def forward():
    m1.forward()
    m2.forward()

def reverse():
    m1.reverse()
    m2.reverse()

def stop():
    m1.stop()
    m2.stop()

def left():
    m1.reverse()
    m2.forward()

def right():
    m1.forward()
    m2.reverse()

commands = {
    "forward": forward,
    "reverse": reverse,
    "left": left,
    "right": right,
    "stop": stop
}

@app.route('/command', ['POST'])
async def command_post(request):
    print(f'Command: {request.json}')
    command = request.json['command']

    if command not in commands:
        return {}, 406

    commands[command]()

    return {}, 202


async def main():
    await start_access_point()
    server = asyncio.create_task(app.start_server(port=80))
    asyncio.create_task(dns_handler())
    print('Done')

    await server


# asyncio.run(main())

