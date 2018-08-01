#!/usr/bin/env python3

import asyncio
import aredis
import websockets
import json
import logging
import signal
from googletrans import Translator

logger = logging.getLogger('websockets.server')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())

connected = set()
translator = Translator()

class WebSocketHandler:
    '''
    Crucial handler that provides websocket connection 
    with Publish/Subscribe object functionality
    '''
    
    @classmethod
    async def create(cls, websocket):
        instance = cls()
        instance.websocket = websocket
        instance.redis = aredis.StrictRedis(host='redis')
        
        # If your application is not interested in the (sometimes noisy) 
        # subscribe/unsubscribe confirmation messages, you can ignore them 
        # by passing ignore_subscribe_messages=True
        instance.pubsub = instance.redis.pubsub(ignore_subscribe_messages=True)
        await instance.pubsub.subscribe('messages')
        
        return instance

    def prepare_response(self, msg):
        '''
        Performs custom translation (EN-RU or <non-EN>-EN) and returns the
        result as JSON encoded string
        '''
        client_info = '({}:{})'.format(*self.websocket.remote_address)
        
        # translation process
        src_lang = translator.detect(msg).lang
        dest_lang = 'en' if src_lang != 'en' else 'ru'
        translated = translator.translate(msg, dest=dest_lang).text
        
        return json.dumps({'client_info': client_info, 
                           'original': msg, 'translated': translated})
    
    
    async def get_messages(self):
        '''
        Asynchronously reads message(s) from subscription channel
        and sends them into the current websocket client connection
        '''
        while True:
            m = await self.pubsub.get_message()
            
            if m:
                await self.websocket.send(m['data'].decode('utf8'))
    
    
    async def handle_websocket(self):
        '''
        Handles incoming websocket data (JSON enconded) with further publication.
        Unsubscribes a client when disconnected with notifying the remaining subscribers
        '''
        while True:
            try:                        
                message = await self.websocket.recv()
                data = json.loads(message)
                
                if 'message' in data:
                    response = self.prepare_response(data['message'])                
                    await self.redis.publish('messages', response)
                                        
                else:
                    logging.error('Client {}:{}, "message" key missing!'
                                  .format(*self.websocket.remote_address), data)
                    
            except websockets.exceptions.ConnectionClosed as e:
                                
                exit_msg = json.dumps({'service_info':'Client ({}:{}) disconnected'
                                       .format(*self.websocket.remote_address)})
                
                # Put notification about the current websocket client is disconnected
                # into the main message channel
                await self.redis.publish('messages', exit_msg)
                await self.pubsub.unsubscribe()
                await self.pubsub.close()
                
                raise e 
        
    
async def process(websocket, path):
    '''
    The main websocket server handler accepting incomming websocket connections
    '''
    wshandler = await WebSocketHandler.create(websocket)
    connected.add(wshandler)
    
    try:
        # handle websocket connection data and subscription channel messages asynchronously
        await asyncio.gather(wshandler.handle_websocket(), wshandler.get_messages())
    except Exception as e:
        logging.error(e)
        connected.remove(wshandler)
            

if __name__ == '__main__':
    addr, port = '0.0.0.0', 5995  # demo parameters
    
    loop = asyncio.get_event_loop()
    
    # Use created websocket server as asynchronous context manager
    # for graceful shutdown
    async def run_server(addr, port, stop):
                
        async with websockets.serve(process, addr, port):
            print(f'Starting websocket server on {addr}:{port}')
            
            await stop
            print('Shutting down websocket server ...')
    
    # Unix-only approach (handling signals)
    stop = asyncio.Future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    loop.add_signal_handler(signal.SIGINT, stop.set_result, None)
    loop.run_until_complete(run_server(addr, port, stop))    
