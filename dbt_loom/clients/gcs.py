import json
from pathlib import Path
from typing import Dict, Optional

from google.cloud import storage


class GCSClient:
    """Client for GCS. Fetches manifest for a given bucket."""

    def __init__(
        self,
        project_id: str,
        bucket_name: str,
        object_name: str,
        credentials: Optional[Path] = None,
    ) -> None:
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.credentials = credentials

    def load_manifest(self) -> Dict:
        """Load a manifest json from a GCS bucket."""
        client = (
            storage.Client.from_service_account_json(
                self.credentials, project=self.project_id
            )
            if self.credentials
            else storage.Client(project=self.project_id)
        )
        bucket = client.get_bucket(self.bucket_name)
        blob = bucket.get_blob(self.object_name)
        if not blob:
            raise Exception(
                f"The object `{self.object_name}` does not exist in bucket `{self.bucket_name}`."
            )

        manifest_json = blob.download_as_text()

        try:
            return json.loads(manifest_json)
        except:
            raise Exception(f"The object `{self.object_name}` is not a valid JSON.")
