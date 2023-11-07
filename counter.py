import requests
import time
import sys
import os

def process_response(response):
    result = dict()
    result['queryId'] = response.get('requestId')
    count = response.get("resultTable").get("rows")[0][0]
    result['count'] = count

    fields = ['numSegmentsQueried', 'numSegmentsProcessed', 'numSegmentsMatched', 
              'numConsumingSegmentsQueried', 'numConsumingSegmentsProcessed', 'numConsumingSegmentsMatched',
              'numDocsScanned', 'totalDocs', 'timeUsedMs']
    renamed_fields = ['segQueried', 'segProcessed', 'segMatched', 
                      'consumingQueried', 'consumingProcessed', 'consumingMatched',
                      'docsScanned', 'totalDocs', 'duration']
    for i in range(len(fields)):
        result[renamed_fields[i]] = response.get(fields[i])
    return result

def format_result(result):
    text = result.get('queryId') + ' count=' + str(result.get('count'))
    text += ' segments(queried/processed/matched)=' + str(result.get('segQueried')) + '/' + str(result.get('segProcessed')) + '/' + str(result.get('segMatched'))
    text += ' consuming(queried/processed/matched)=' + str(result.get('consumingQueried')) + '/' + str(result.get('consumingProcessed')) + '/' + str(result.get('consumingMatched'))
    text += ' docs(scanned/total)=' + str(result.get('docsScanned')) + '/' + str(result.get('totalDocs'))
    text += ' duration=' + str(result.get('duration'))
    return text

include_headers=True
def format_csv(result: dict):
    global include_headers
    if include_headers:
        header = ','.join(result.keys()) + '\n'
        include_headers=False
    else:
        header = ''
    values = ','.join([str(item) for item in result.values()]) + '\n'
    return header + values

def query_count():
    try:
        with requests.get("http://localhost:8099/query/sql", params={
            # "sql": 'set "skipUpsert"=true; select count(*) as count from issuerrisk'
            "sql": 'select count(*) as count from issuerrisk'
        }) as response:
            return process_response(response.json())
    except requests.RequestException as e:
        print(e)

date = '20231107'
i = 3
test_number = f'{date}-{i}'
while os.path.isfile(f'data/{test_number}.log'):
    i += 1
    test_number = f'{date}-{i}'

try:
    log_file = open(f'data/{test_number}.log', 'w')
    csv_file = open(f'data/{test_number}.csv', 'w')
    while True:
        result = query_count()
        text = format_result(result)
        print(text)
        log_file.write(text + '\n')
        csv_file.write(format_csv(result))
        time.sleep(0.1)
except Exception as e:
    print(e)
finally:
    log_file.close()
    csv_file.close()
        
