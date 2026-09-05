import sys
sys.path.append('c:/Users/user/prod/py/videolang/backend')
from services.search_service import semantic_search

try:
    results = semantic_search('wind')
    print(f'Count after filter: {len(results)}')
    if len(results) > 0:
        print('Sample score:', results[0].get('timestamp_score'))
except Exception as e:
    print(f'Error: {e}')
