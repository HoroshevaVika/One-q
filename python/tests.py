import json
import pytest
import time


class TestExample:

    def test_check_all_resourse(self, client):
        version_status = client.check_version()
        data = {"command": "sleep 20 && echo 200"}
        response = client.create_task(data)
        jsonData = response.json()
        assert response.status_code == 201, "Код запроса не равен ожидаемому 201. Код запроса = {}".format(response.status_code)
        assert ('task_id' in jsonData), "В теле ответа отсутствует информация о task_id"


    def test_more_gpu_than_allowed(self, client):
        version_status = client.check_version()
        data = {
            "command":"echo 1",
            "gpu":"10",
            "cpu":"8",
            "gpu_model":"Tesla K40c"
        }
        response = client.create_task(data)
        jsonData = response.json()
        assert jsonData['error'] == "No available GPUs in cluster: 1 < 10", "Отсутствует ожидаемая ошбика, что количество gpu превышает дозволенное значение."


    def test_more_cpu_than_allowed(self, client):
        version_status = client.check_version()
        data = {
            "command":"echo 1",
            "gpu":"1",
            "cpu":"80",
            "gpu_model":"Tesla K40c"
        }
        response = client.create_task(data)
        jsonData = response.json()
        assert jsonData['error'] == "No available CPUs in cluster: 8 < 80", "Отсутствует ожидаемая ошбика, что количество cpu превышает дозволенное значение."


    def test_more_gpu_model_than_allowed(self, client):
        version_status = client.check_version()
        data = {
            "command":"echo 1",
            "gpu":"1",
            "cpu":"8",
            "gpu_model":"Tesla K80"
        }
        response = client.create_task(data)
        jsonData = response.json()
        assert jsonData['error'] == "No 'Tesla K80' GPU in cluster", "Отсутствует ожидаемая ошбика, что количество gpu превышает дозволенное значение."


    # @pytest.mark.in_progress
    def test_create_simple_task(self, client):
        version_status = client.check_version()
        data = {
            "command":"echo 1"
        }
        response = client.create_task(data)
        jsonData = response.json()
        assert response.status_code == 201, "Код запроса не равен 201. Код запроса = {}".format(response.status_code)
        assert ("task_id" in jsonData), "В теле ответа отсутствует информация о task_id"


    def test_create_task_without_command(self, client):
        version_status = client.check_version()
        data = {}
        response = client.create_task(data)
        jsonData = response.json()
        assert response.status_code == 400, "Код запроса не равен ожидаемому 400. Код запроса = {}".format(response.status_code)
        assert jsonData['error'] == "Command found not, Luke!", "Отсутствует ожидаемая ошбика 'Команда не найдена'"


    def test_get_nonexistent_task(self, client):
        version_status = client.check_version()
        bad_id = "/00000000-1111-2222-3333-444444444444"
        response = client.get_task_by_id(bad_id)
        jsonData = response.json()
        assert response.status_code == 404, "Код запроса не равен ожидаемому 404. Код запроса = {}".format(response.status_code)
        assert jsonData['error'] == "Task not found", "Отсутствует ожидаемая ошбика 'Задача с id = '{}'' не найдена'".format(bad_id)

    @pytest.mark.in_progress
    def test_check_task_statuses(self, client):
        # version_status = client.check_version()
        data = {
            "command": "sleep 20 && echo 200"
        }
        # создаем задачу /task
        response1 = client.create_task(data)
        print("Task is create!")
        jsonData1 = response1.json()
        assert response1.status_code == 201, "Код запроса не равен ожидаемому 201. Код запроса = {}".format(response1.status_code)
        # print("/n jsonData1 = ", jsonData1)
        assert 'task_id' in jsonData1, "В теле ответа отсутствует информация о task_id"
        task_id = jsonData1['task_id']

        # проверка статуса таски = 0
        response2 = client.get_task_by_id(task_id)
        jsonData2 = response2.json()
        # print("/n jsonData2 = ", jsonData2)
        assert jsonData2['status'] == 0, "Код задачи не равен 0. Код задачи = {}".format(jsonData2['status'])

        # проверка статуса таски = 100
        response3 = client.get_task_by_id(task_id)
        jsonData3 = response3.json()
        print("\njsonData3 = " + str(jsonData3))
        client.check_status(20, 100, jsonData3['status'], 0, 0.5, task_id)
        time.sleep(3)
        # проверка статуса таски = 200
        response4 = client.get_task_by_id(task_id)
        jsonData4 = response4.json()
        print("\njsonData4 = " + str(jsonData4))
        client.check_status(20, 200, jsonData4['status'], 100, 3, task_id)







