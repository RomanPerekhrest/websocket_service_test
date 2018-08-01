# websocket_service_test

The current minimal project is for demonstration purpose.  
It's aimed to build and run a distributed messaging service based on WebSocket server powered by:
* [Docker](https://www.docker.com/community-edition) containerization
* Python's [websockets](https://github.com/aaugustin/websockets/) library
* [Redis](https://redis.io/) storage engine/message brocker
* asynchronous [aredis](https://github.com/NoneGG/aredis) client.

### Prerequisites

* Linux OS
* docker >= 17.x
* [docker-compose](https://docs.docker.com/compose/install/)

### Installing
* Clone or download the archieve (with further decompression) of the current project on your local machine.  
* Change your current direcotory to `websocket_service_test` with:  
`cd websocket_service_test`  
* Make auxiliary shell scripts executable with:  
`chmod 755 *_ws_service.sh`
* Run build/run process of websocket service with:  
`./build_ws_service.sh && ./run_ws_service.sh`  
wait untill the process complete. You should see the following output in the end if successful:
```
...
Creating network ws_service_ws_net
Creating service ws_service_redis
Creating service ws_service_web
```
### Testing

You may observe all running websocket server and redis instances with:  
`docker service ps ws_service_web ws_service_redis`  
(the number of websocket server instances defaults to `7`)  
The output should look similar to the following:
```
ID                  NAME                 IMAGE               NODE                DESIRED STATE       CURRENT STATE         ERROR               PORTS
kctdsl6ehnet        ws_service_web.1     ws_server:latest    roman               Running             Running 8 hours ago                       
ybplzdfu5juu        ws_service_redis.1   redis:latest        roman               Running             Running 8 hours ago                       
uh0zkgkgrew6        ws_service_web.2     ws_server:latest    roman               Running             Running 8 hours ago                       
2ongwqpl956s        ws_service_web.3     ws_server:latest    roman               Running             Running 8 hours ago                       
b24tdxjdjdws        ws_service_web.4     ws_server:latest    roman               Running             Running 8 hours ago                       
0t3rkeuwxgme        ws_service_web.5     ws_server:latest    roman               Running             Running 8 hours ago                       
4n9vrv6fpi0h        ws_service_web.6     ws_server:latest    roman               Running             Running 8 hours ago                       
omb9bg0k9bg5        ws_service_web.7     ws_server:latest    roman               Running             Running 8 hours ago 
```

To scale in/out the service you could specify:  
`docker service scale ws_service_web=<number_of_replicas>`  

To test websocket connections use *`ws_client.html`* file in the root of the current working directory(`websocket_service_test`).  
I'll serve as a browser websocket client with default connection `ws://127.0.0.1:5995` (just for testing)  
Open that file in multiple browser tabs or windows (or different browsers).  
The one of possible simple ways to run the file in 3 firefox tabs:  
`for i in {1..3}; do firefox --new-tab ws_client.html & done`

Start writing messages in different tabs/windows (there will be a textbox) and watch how websocket communication(notification) is synchronized.  

To stop and run the service use `./stop_ws_service.sh` and `./run_ws_service.sh` respectively.



