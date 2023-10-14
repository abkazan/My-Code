'''
Demo of async programming to perform requests faster. I would like to implement this tech into our dbconn module. 

I put this file in the module, but it is a stand alone file. Run it on its own like you would any other python file.
'''

from asyncio import (
    run,
    gather,
    to_thread
)

from requests import (
    get
)

from time import (
    time
)

urls = [*map('https://{}.com'.format, [
    'google',
    'facebook',
    'twitter',
    'netflix',
    'bing',
    'wikipedia',
    'openai'
])]

# synchronous baseline test

def sync_get(url: str):
    '''
    Request a status code from a url synchronously
    '''

    r = get(url)
    return r.status_code

start = time()
for url in urls:
    print(sync_get(url))
end = time()
print(f'elapsed time was {end-start:.2} seconds')

# asynchronous test

async def async_get(url: str):
    '''
    Request a status code from a url asynchronously
    '''
    return await to_thread(sync_get, url)

async def main():
    codes = await gather(*[async_get(url) for url in urls])
    [*map(print, codes)]

start = time()
run(main())
end = time()
print(f'elapsed time was {end-start:.2} seconds')