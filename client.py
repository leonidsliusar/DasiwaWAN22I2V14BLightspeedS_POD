import base64
import copy
import os
import json
from pathlib import Path
from time import sleep

import boto3
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

WORKFLOW_PATH = Path(__file__).parent/ "workflows" / "workflow.json"


class Client:

    def __init__(self):
        self.bucket = os.getenv("S3_BUCKET")
        self.s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("S3_ENDPOINT"),
            region_name=os.getenv("S3_REGION_NAME"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        self.run_pod_api_key = os.getenv("RUN_POD_API_KEY")
        self.run_pod_id = os.getenv("RUN_POD_ID")

        with open(WORKFLOW_PATH, "r") as f:
            self.workflow = json.load(f)

    def save_video(self, task_id: str) -> str:
        response = requests.get(
            url=f"https://api.runpod.ai/v2/{self.run_pod_id}/status/{task_id}",
            headers={
                "Authorization": f"Bearer {self.run_pod_api_key}",
                "Content-Type": "application/json"
            }
        )
        print(response)
        data = response.json()
        print(data)
        video_info = data["output"]["images"][0]

        if video_info["type"] == "s3_url":
            video_url = video_info["data"]
            video_response = requests.get(video_url)
            with open(f"./output/{task_id}.webm", "wb") as f:
                f.write(video_response.content)
        else:
            video_bytes = base64.b64decode(video_info["data"])
            with open(f"./output/{task_id}.webm", "wb") as f:
                f.write(video_bytes)

        return f"./output/{task_id}.webm"

    def send_job(self, image_path: str, prompt: str, seconds: int, seed: int) -> str:
        workflow = copy.deepcopy(self.workflow)

        workflow["959"]["inputs"]["image"] = "input.png"
        workflow["911:1044"]["inputs"]["text"] = prompt
        workflow["911:1075"]["inputs"]["value"] = seconds
        workflow["911:915"]["inputs"]["seed"] = seed

        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")

        response = requests.post(
            url=f"https://api.runpod.ai/v2/{self.run_pod_id}/run",
            json={
                "input": {
                    "workflow": workflow,
                    "images": [
                        {
                            "name": "input.png",
                            "image": image_base64
                        }
                    ]
                }
            },
            headers={
                "Authorization": f"Bearer {self.run_pod_api_key}",
                "Content-Type": "application/json"
            }
        )
        return response.json()["id"]

    def check_status(self, task_id: str) -> str:
        status = "IN_PROGRESS"
        while status not in ("FAILED", "COMPLETED"):
            sleep(5)
            response = requests.get(
                url=f"https://api.runpod.ai/v2/{self.run_pod_id}/status/{task_id}",
                headers={
                    "Authorization": f"Bearer {self.run_pod_api_key}",
                    "Content-Type": "application/json"
                }
            )
            data = response.json()
            status = data["status"]

            if status in ("FAILED", "COMPLETED"):
                if status == "FAILED":
                    logger.error(f"Job failed: {data.get('error')}")
                return status
            logger.info(f"Status: {status}, waiting for completion ...")
        return status

    def generate_video(self, image_path: str, prompt: str, seconds: int = 5, seed: int = -1) -> str:
        task_id = self.send_job(image_path=image_path, prompt=prompt, seconds=seconds, seed=seed)
        status = self.check_status(task_id=task_id)
        match status:
            case "COMPLETED":
                print("Job completed successfully!")
                self.save_video(task_id=task_id)
                print(f"Video {task_id}.webm saved successfully!")
        return status