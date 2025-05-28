from datetime import datetime, timezone, timedelta
from time import sleep
from http import HTTPStatus

def create_detection_in_api(client,
                            text: str = "Reconocer",
                            language: str = "Español"):
    detection_data = {
        "text": text,
        "language": language
    }
    return client.post("/detections/", json=detection_data)

def test_create_detection_not_palindrome(client, db_session):
    response = create_detection_in_api(client=client)
    assert response.status_code == HTTPStatus.OK.value
    detection_result = response.json()
    assert detection_result["id"] == 1
    assert detection_result["text"] == "Reconocer"
    assert detection_result["language"] == "Español"
    assert detection_result["is_palindrome"] == True

def test_create_detection_missing_parameter(client, db_session):
    detection_data = {
        "text": "Reconocer"
    }

    response = client.post("/detections/", json=detection_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value


def test_delete_detection_found(client, db_session):
    response = create_detection_in_api(client=client)

    assert response.status_code == HTTPStatus.OK.value

    detection_id = response.json()["id"]

    response = client.delete(f"/detections/{detection_id}")
    assert response.status_code == HTTPStatus.OK.value
    detection_result = response.json()
    assert detection_result["id"] == 1
    assert detection_result["text"] == "Reconocer"
    assert detection_result["language"] == "Español"
    assert detection_result["is_palindrome"] == True

def test_delete_detection_not_found(client, db_session):
    response = client.delete(f"/detections/{1}")
    assert response.status_code == HTTPStatus.NOT_FOUND.value

def test_find_specific_detection_found(client, db_session):
    response = create_detection_in_api(client=client)

    assert response.status_code == HTTPStatus.OK.value

    detection_id = response.json()["id"]

    response = client.get(f"/detections/{detection_id}")

    assert response.status_code == HTTPStatus.OK.value

    detection_result = response.json()

    assert detection_result["id"] == 1
    assert detection_result["text"] == "Reconocer"
    assert detection_result["language"] == "Español"
    assert detection_result["is_palindrome"] == True

def test_find_specific_detection_not_found(client, db_session):
    response = client.get(f"/detections/1")
    assert response.status_code == HTTPStatus.NOT_FOUND.value

def test_find_list_detections_filter_by_language(client, db_session):
    response = create_detection_in_api(client=client,
                                       text="Esto es una prueba",
                                       language="Spanish")

    assert response.status_code == HTTPStatus.OK.value

    response = create_detection_in_api(client=client,
                                       text="This is a test",
                                       language="English")

    assert response.status_code == HTTPStatus.OK.value

    response = client.get("/detections/?language=Spanish")

    assert response.status_code == HTTPStatus.OK.value
    assert len(response.json()) == 1

    detection_result = response.json()[0]

    assert detection_result["id"] == 1
    assert detection_result["text"] == "Esto es una prueba"
    assert detection_result["language"] == "Spanish"
    assert detection_result["is_palindrome"] == False

    response = client.get("/detections")
    assert response.status_code == HTTPStatus.OK.value
    assert len(response.json()) == 2

def test_find_list_detections_filter_by_date(client, db_session):

    response = create_detection_in_api(client=client,
                                       text="Tete",
                                       language="English")

    created_at_first_detection = datetime.fromisoformat(response.json()["created_at"])

    sleep(3)

    assert response.status_code == 200

    response = create_detection_in_api(client=client,
                            text="Reconocer",
                            language="Spanish")

    assert response.status_code == 200

    created_at_second_detection = datetime.fromisoformat(response.json()["created_at"])

    start_date = (created_at_first_detection - timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S").replace(":", "%3A")
    end_date = (created_at_first_detection + timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S").replace(":", "%3A")


    response = client.get(f"/detections/?start_date={start_date}&end_date={end_date}")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["text"] == "Tete"

    end_date = (created_at_second_detection + timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S").replace(":", "%3A")

    response = client.get(f"/detections/?start_date={start_date}&end_date={end_date}")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["text"] == "Reconocer"
    assert response.json()[1]["text"] == "Tete"

