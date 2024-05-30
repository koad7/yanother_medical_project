import pytest
from unittest.mock import patch, mock_open
import producers.heart_rate_producer as heart_rate_producer

@pytest.fixture
def mock_kafka_producer():
    with patch('producer.heart_rate_producer.KafkaProducer') as mock:
        yield mock

def test_read_csv_and_send_to_kafka(mock_kafka_producer):
    mock_open_file = mock_open(read_data="heart_rate\n80\n85\n90")
    with patch('builtins.open', mock_open_file):
        heart_rate_producer.read_csv_and_send_to_kafka('fake_path.csv')
    
    assert mock_kafka_producer.return_value.send.call_count == 3
    mock_kafka_producer.return_value.send.assert_any_call('heart_rate', value={'heart_rate': '80'})
    mock_kafka_producer.return_value.send.assert_any_call('heart_rate', value={'heart_rate': '85'})
    mock_kafka_producer.return_value.send.assert_any_call('heart_rate', value={'heart_rate': '90'})
