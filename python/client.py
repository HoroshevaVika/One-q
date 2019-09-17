import requests
import time
import pytest

retry_timeout = 3
limit = 4
good_version_couter = 0
good_version = "v0.4.21"
retry_number = 12

class RestfulOneQ:

    
    host = None

    def __init__(self, host):
        self.host = host
        self._s = requests.session()


    def create_task(self, data: dict):
        return self._s.post(self.host + "/task", json=data)

    def get_task_by_id(self, id):
        return self._s.get(self.host + "/task/" + id)


    def send_version(self, retry_count):
        global good_version_couter
        response = self._s.get(self.host + "/version")
        # self.retry_count = retry_count

        print("Version from response - " + response.json())

        if response.json() == good_version:
            print("good_version_couter before increment = ", good_version_couter)
            good_version_couter = good_version_couter + 1
            print("good_version_couter after increment = ", good_version_couter)

            if good_version_couter >= limit:
                print("Version is giving up.")
            else:
                print("Need to check version one more time. Retrying in ", retry_timeout, "sec")
                self.retry_it(retry_count)
        else:
            good_version_couter = 0
            print("good_version_couter after zerroing = ", good_version_couter)
            print("Version is still DEPLOY. Retrying in ", retry_timeout, "ms")
            self.retry_it(retry_count)



    def retry_it(self, retry_count):
        if retry_count <= 1: 
            print("Sorry, version is wrong and retry count = ", retry_count)
            assert False
            # postman.setNextRequest(null);
        else:
            time.sleep(retry_timeout)
            retry_count = retry_count - 1
            print("During retry count = ", retry_count)
            self.send_version(retry_count)
            

    def check_version(self):
        if good_version_couter >= limit:
            print("Version is already giving up.")
            return
        else:
            self.send_version(retry_number)


    def check_status(self, retry_count, waiting_status, status, previous_status, timeout, task_id):
        if retry_count == 0:
            print("During retry count = ", retry_count)
            pytest.fail("Not enough retries. Retry count = ", retry_count)
        elif status == waiting_status:
            print("The status is correct. During status = {}, waiting status = {}".format(status, waiting_status))
            assert (True), "The status is correct. Task status =  " + str(status)
            return
        elif status == previous_status:
            retry_count = retry_count - 1
            print("The status is incorrect. During status = {}, waiting status = {}. \nLet's try again. During retry count = {}".format(status, waiting_status, retry_count))
            time.sleep(timeout)
            json_response = self.get_task_by_id(task_id).json()
            status = json_response['status']
            # print("\nnew json_response" + str(json_response))
            self.check_status(retry_count, waiting_status, status, previous_status, timeout, task_id)
        else:
            pytest.fail("Unknown task status = " + str(status))
        # retry_status_100 = retry_count


