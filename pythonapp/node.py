#!/usr/bin/env python3.6

import raftos
import asyncio
import argparse
import mysql.connector
import random
from aiohttp import web

PORTS = [8000, 8001, 8002]

parser = argparse.ArgumentParser()
parser.add_argument('--node')
args = parser.parse_args()

NODE_ID = int(args.node)

PORT = PORTS[NODE_ID-1]
HTTPPORT = PORT + 10
NODE_LOGFILE = f'node{NODE_ID}_CUSTOMLOG.log'
# Since this is run for each 'node', we're telling this node
# what ports the other nodes are running on.
other_node_ids = [id for id in [1,2,3] if id != NODE_ID]
other_nodes_ports = [p for p in [8000, 8001, 8002] if p != PORT]

raftos.configure({
    'log_path': './',
    'serializer': raftos.serializers.JSONSerializer
})
loop = asyncio.get_event_loop()

# Each port is simulating a real life
# node/machine connected over a network.
this_node_address = f'127.0.0.1:{PORT}'
sleep_time = random.randint(1, 5)

loop.create_task(
    raftos.register(
        this_node_address,

        # Telling raft which ones are 
        # part of this node's cluster
        cluster=[
            f'127.0.0.1:{other_nodes_ports[0]}',
            f'127.0.0.1:{other_nodes_ports[1]}'
        ]
    )
)

## Connection to Database
def connect_to_database(node_id):
    connection = mysql.connector.connect(user='root', password='mysql',
                            host='localhost', port=int(f'3306{node_id}'),
                            database='taskmanager')

    return connection

## updation logic
def updatedb(id, data, operation):
    connection = connect_to_database(id)
    cursor = connection.cursor()
    
    if operation == 'write':
        cursor.execute("INSERT INTO tasks (task, assigned_to, priority, status) VALUES (%s, %s, %s, %s)", (data["task"], data["assigned_to"], data["priority"], data["status"]))
    
    elif operation == 'update':
        cursor.execute(f"UPDATE tasks SET {data['field']} = %s WHERE task_id = %s", (data['new_value'], data['task_id']))
        
    elif operation == 'delete':
        cursor.execute("DELETE FROM tasks WHERE task_id = %s", (data['task_id'],))
    
    connection.commit()
    connection.close()

with open(NODE_LOGFILE, 'w') as log_file:
    pass

async def run(loop):
    # Non leaders get stuck in this loop!
    old_leader = None
    while raftos.get_leader() != this_node_address:

        await asyncio.sleep(sleep_time)

        with open(NODE_LOGFILE, 'a') as log_file:
            current_leader = raftos.get_leader()
            
            if current_leader != old_leader:
                log_file.write(f'Leader is now: {current_leader}\n')
                
            old_leader = current_leader

    # A node that reaches here has to be the leader.
    await asyncio.sleep(sleep_time)
    
    print(f"Node {NODE_ID} is starting the server...")
    with open(NODE_LOGFILE, 'a') as log_file:
        app = web.Application()
        app.router.add_post('/mysql', handle_mysql_request)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', HTTPPORT)
        await site.start()

        # Client Command executed;    
        log_file.write(f'Node {NODE_ID} has performed the updates!')

async def handle_mysql_request(request):
    # Extract operation details from the request
    request_data = await request.json()
    operation = request_data.get('operation')
    # Perform the operation on the leader node
    if raftos.get_leader() == this_node_address:
        
        updatedb(NODE_ID, request_data, operation)

        # Replication logic:
        
        for i in other_node_ids:
            updatedb(i, request_data, operation)

    return web.Response(text='Operation completed')

loop.run_until_complete(run(loop))
loop.run_forever()
