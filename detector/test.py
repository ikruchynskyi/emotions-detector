import requests
import json
import emotionAnalyzer
import re
import sys
import os
from datetime import datetime


headers = {
    'authority': 'magento.zendesk.com',
    'Accept': 'application/json',
    'cookie': '' # Copy personal cookie to emulate access   //TODO rewrite using requests.get('auth'=())
}
params = {
    'sort_by': 'created_at',
    'sort_order': 'asc',
    'page': 1
}
negative_emotions = ['anger', 'annoyance', 'disgust']

def paginate_request(url, headers, params, agregator, field=None):
    data = []
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            pages = (response.json()['count'] // 100) + 1
            data.append(response.json()[agregator])
            if (pages > 1):
                for page in range(2, pages + 1):
                    try:
                        params['page'] = page
                        response = requests.get(url, headers=headers, params=params)
                        if response.status_code == 200:
                            data.append(response.json()[agregator])
                    except:
                        print(f"Failed to make page {page} pagination request, URL: {url}", file=sys.stderr)
    except:
        print(f"Failed to make initial pagination request, URL: {url}", file=sys.stderr)
    if field is not None:
        result = []
        for page in data:
            for item in page:
                result.append(item[field])
        return result
    else:
        return data

date_filter = os.getenv('FILTER_DATE', datetime.today().strftime('%Y-%m-%d'))
updated_tickets_url = 'https://magento.zendesk.com/api/v2/search.json?query=updated%3E{date_filter}%20type:ticket'.format(date_filter=date_filter)

print("Getting tickets data...")
tickets = paginate_request(updated_tickets_url, headers, params, 'results', 'id')
print("Getting users data...")
agent_ids = paginate_request("https://magento.zendesk.com/api/v2//users.json?role[]=agent&role[]=admin", headers, params, 'users', 'id')

for ticket_id in tickets:
    print(f"Getting list of comments for ticket ID {ticket_id}...")
    # response = requests.get(url.format(ticket_id=ticket_id), headers=headers, auth=(user, pwd), params=params)
    response = requests.get('https://magento.zendesk.com/api/v2/tickets/{ticket_id}/comments.json'.format(ticket_id=ticket_id), headers=headers, params={})
    if response.status_code == 200:
        comments = response.json()['comments']
        for comment in comments:
            if (comment['public'] != False and comment['author_id'] not in agent_ids):
                text = comment['body']
                text = re.sub(r"^Hi|Hello|Good|Greet.*$", '', text, re.MULTILINE|re.IGNORECASE) # Remove greetings
                text = re.sub(r"http.*?[\s\)\]]", '', text) # Remove links
                text = re.sub(r'\r\n|\r|\n', ' ', text).strip() # inline
                text = re.sub(r'(Thank.*|Regards.*)', '', text, re.IGNORECASE) # Remove signatureD
                if len(text) < 300: # Result for more symbols will not be accurate and might contains redundant data such as tables or code
                    emotions_data = emotionAnalyzer.analyze(text)
                    if (emotions_data[0]['label'] in negative_emotions):
                        print(text)
                        print(emotions_data)
                        print('==========================================================')
    else:
        print(f'Get ticket {ticket_id} comments failed with status code {response.status_code}', file=sys.stderr)
