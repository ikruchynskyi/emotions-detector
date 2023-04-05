import requests
import sys
import re

class ZDClient:
    def __init__(self, config):
        self._config = config
        self._domain = config.get('domain')
        self._url = f"https://{self._domain}.zendesk.com/"
        self._params = {
            'sort_by': 'created_at',
            'sort_order': 'asc',
            'page': 1
        }
        self._headers = {
            'authority': f'{self._domain}.zendesk.com',
            'Accept': 'application/json',
            'Authorization': "Bearer " + config,get('bearer')
        }

    def getTickets(self, filter) -> list:
        return self.paginate_request("api/v2/search.json?query=type:ticket" + filter, 'results', 'id')

    def getComments(self, ticket_id, date_filter) -> list:
        response = requests.get(self._url + f"api/v2/tickets/{ticket_id}/comments.json", headers=self._headers)
        data = []
        if response.status_code == 200:
            comments = response.json()['comments']
            for comment in comments:
                if (comment['public'] != False and comment['created_at'] > date_filter):
                    text = comment['body']
                    text = re.sub(r'\r\n|\r|\n', ' ', text).strip()  # Strip NBSP chars and new lines
                    text = "".join(ch for ch in text if ch.isalnum() or ch == " ")
                    comment['sanitized_text'] = text
                    data.append(comment)
        else:
            print(f'Get ticket {ticket_id} comments failed with status code {response.status_code}', file=sys.stderr)
        return data

    def paginate_request(self, endpoint, agregator, field=None) -> list:
        data = []
        try:
            url = self._url + endpoint
            response = requests.get(url, headers=self._headers, params=self._params)
            if response.status_code == 200:
                pages = (response.json()['count'] // 100) + 1
                data.append(response.json()[agregator])
                if (pages > 1):
                    for page in range(2, pages + 1):
                        try:
                            self._params['page'] = page
                            response = requests.get(url, headers=self._headers, params=self._params)
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