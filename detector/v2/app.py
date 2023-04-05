from emotionAnalyzer import Analyzer
from datetime import datetime, timedelta
from tensorflow.python.framework.errors_impl import InvalidArgumentError
import csv
from config import Config
from ZDClient import ZDClient

def run(config) -> int:
    try:
        writeCommentsToFile()
        report_data = analyzeComments()
        generateReport(report_data)
    except Exception as e:
        print("Exception occured", e)
        return 1
    return 0;

def writeCommentsToFile():
    zd_client = ZDClient(config)
    date_filter = config.get('date_filter')
    if (date_filter is None):
        date_filter = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    print("Collecting tickets")
    tickets = zd_client.getTickets(f"%20updated%3E{date_filter}")

    if (len(tickets) > 0):
        with open(config.get('comments_file'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ticket_id", "comment_id", "comment", "created_at"])
            for ticket_id in tickets:
                print(f"Collecting comments for ticket_id {ticket_id}")
                comments = zd_client.getComments(ticket_id, date_filter)
                for comment in comments:
                    writer.writerow([ticket_id, comment['id'], comment['sanitized_text'], comment['created_at']])

def analyzeComments():
    negative_emotions = config.get('negative_emotions')
    report_data = []
    with open(config.get('comments_file'), mode='r') as file:
        csvFile = csv.DictReader(file)
        analyzer = Analyzer();
        for line in csvFile:
            try:
                emotions_data = analyzer.analyze(line['comment'])
                if (emotions_data[0]['label'] in negative_emotions):
                    row = {
                        'ticket_id': line['ticket_id'],
                        'comment': line['comment'],
                        'label': emotions_data[0]['label'],
                        'score': emotions_data[0]['score']
                    }
                    report_data.append(row)
                    print(line['comment'])
                    print(emotions_data)
            except InvalidArgumentError:
                print(f"Error during parsing comment {line['comment_id']}")
    return report_data
def generateReport(report_data):
    print("Generating report..")
    if (len(report_data)):
        with open(config.get('report_file'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ticket_id", "comment", "sentiment_label", "sentiment_score"])
            for row in report_data:
                writer.writerow([
                    "https://magento.zendesk.com/agent/tickets/" + str(row['ticket_id']),
                    row['comment'],
                    row['label'],
                    row['score']
                ])

if __name__ == '__main__':
    config = Config()
    run(config)