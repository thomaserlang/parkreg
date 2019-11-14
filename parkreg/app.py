import os, click, zeep, asyncio
from zeep.asyncio import AsyncTransport
from tornado import web, httpserver, ioloop
import logging

class MainHandler(web.RequestHandler):

    def get(self):
        self.render('index.html')

    async def post(self):
        client = self.application.settings['zeep_client']
        r = await client.service.RegisterPermissionLingual(
            self.application.settings['parkzone_device_id'],
            self.application.settings['parkzone_password'],
            self.get_argument('number_plate'),
            self.get_argument('mobile_number'),
            'da',
        )
        if r.Success:
            self.write(r.OkMessage.replace('\n', '<br />'))
        else:
            self.set_status(500)
            self.write(r.ErrorMessage.replace('\n', '<br />'))

def make_app(device_id, password, debug, zeep_client):
    urls = [
        (r'/', MainHandler),
    ]
    return web.Application(
        urls,
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        parkzone_device_id=device_id,
        parkzone_password=password,
        debug=debug,
        zeep_client=zeep_client,
    )

@click.command()
@click.option('--port', default=9000)
@click.option('--wsdl', default='https://parkcaredevicebackend.parkzone.dk/service.asmx?WSDL', help='WSDL url for ParkZone')
@click.option('--device-id', required=True, help='Device id for ParkZone')
@click.option('--password', required=True, help='Password for ParkZone')
@click.option('--debug', default=False)
def run(port, wsdl, device_id, password, debug):
    transport = AsyncTransport(asyncio.get_event_loop(), cache=None)
    client = zeep.Client(wsdl, transport=transport)

    app = make_app(device_id, password, debug, client)
    app.listen(port)
    ioloop.IOLoop.current().start()

if __name__ == '__main__':
    run()