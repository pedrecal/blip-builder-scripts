import sys
import json
import ast
from requests import post
from uuid import uuid4

bot_authorization = 'Key Ym1ncm91dGVyaG1nOkJIUWxUZ0NqdWMzYzh0M2lPTWJB'

commands_url = 'https://msging.net/commands'

def getUserContexts(identity, skip=0):
    res = post(
        commands_url,
        headers={
            'Authorization': bot_authorization
        },
        json={
            'id': str(uuid4()),
            'method': 'get',
            'uri': f'/contexts/{identity}?$skip={skip}&$take=100',
        }
    )
    return res

def deleteUserContext(identity, context):
    res = post(
        commands_url,
        headers={
            'Authorization': bot_authorization
        },
        json={
            'id': str(uuid4()),
            'method': 'delete',
            'uri': f'/contexts/{identity}/{context}',
        }
    )
    return res

def getPaginatedUserContexts(identity):
    skip = 0
    res = getUserContexts(identity).content
    res_str = res.decode("UTF-8")
    res_dict = ast.literal_eval(res_str)
    total = res_dict['resource']['total']
    while total == 100:
        skip += 100
        loop_res = getUserContexts(identity, skip).content
        loop_res_str = loop_res.decode("UTF-8")
        loop_res_dict = ast.literal_eval(loop_res_str)
        total = loop_res_dict['resource']['total']
        contexts = res_dict['resource']['items'] + loop_res_dict['resource']['items']
    return contexts



if __name__ == "__main__":
    if bot_authorization == '':
        print(f'add the Athorization Key in the file')
        exit(-1)

    if len(sys.argv) < 2:
        print(f'use: python {__file__} <user identity>')
        exit(-1)

    identity = sys.argv[1]

    contexts = getPaginatedUserContexts(identity)

    async_list = []
    errors = []

    for context in contexts:
        async_item = deleteUserContext(identity, context)
        async_list.append(async_item)

    async.map(async_list)

    if errors:
        print('\x1b[6;30;41m' + 'The following contexts couldn\'t be deleted:' + '\x1b[0m')
        print('\x1b[6;30;43m' + ', '.join(errors) + '\x1b[0m')
    else:
        print('\x1b[6;30;42m' + 'All the contexts were deleted successfully' + '\x1b[0m')


