from flask import Flask, request, jsonify
import aiohttp
import asyncio

app = Flask(__name__)

NODE_URLS = ['http://localhost:8010/mysql', 'http://localhost:8011/mysql', 'http://localhost:8012/mysql']  # Replace with the URLs of your node.py servers

async def post_request(url, data):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    except Exception as e:
        print(f"Request not sent to {url}, Server at {url} is not the leader")
        return {"error": f"Server at {url} is not the leader"}

@app.route('/create_task', methods=['POST'])
def create_task():
    data = request.get_json()
    data['operation'] = 'write'
    print(data)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [loop.create_task(post_request(url, data)) for url in NODE_URLS]
    responses = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    return jsonify(responses)

@app.route('/update_task', methods=['POST'])
def update_task():
    data = request.get_json()
    data['operation'] = 'update'
    print(data)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [loop.create_task(post_request(url, data)) for url in NODE_URLS]
    responses = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    return jsonify(responses)

@app.route('/delete_task', methods=['POST'])
def delete_task():
    data = request.get_json()
    data['operation'] = 'delete'
    print(data)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [loop.create_task(post_request(url, data)) for url in NODE_URLS]
    responses = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    return jsonify(responses)

if __name__ == '__main__':
    app.run(debug=True)