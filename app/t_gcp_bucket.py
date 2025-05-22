from google.cloud import storage
import os


bucket_json = "app/bucket_key.json"
def test_gcp_storage(bucket_name: str):
    try:
        print("Setting GOOGLE_APPLICATION_CREDENTIALS environment variable")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = bucket_json
        print(f"GCP credential file created.")

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blobs = list(bucket.list_blobs())

        print(f"✅ Successfully connected to bucket: {bucket_name}")
        print(f"Found {len(blobs)} objects:")
        if len(blobs) == 0:
            print("No objects found in the bucket.")
        else:
            print("Objects in the bucket:")
            for blob in blobs[:5]:  # 最多列出前5筆
                print(f"- {blob.name}")
        return True

    except Exception as e:
        print("❌ Failed to connect to GCP:", e)
        return False

def test_upload(bucket_name: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    # 讀取本地測試檔案
    file_path = "app/src/pdf-example-a4-portrait.pdf"
    file_name = f"pdf-example-a4-portrait.pdf"

    blob = bucket.blob(file_name)
    with open(file_path, "rb") as f:
        blob.upload_from_file(f, content_type="application/pdf")
    
    # 設定公開讀取
    blob.make_public()
    print("Uploaded file URL:", blob.public_url)
    blobs = list(bucket.list_blobs())
    print(f"Found {len(blobs)} objects.")

    
if __name__ == "__main__":
    # 設定你的 GCP bucket 名稱
    BUCKET_NAME = "leave_system_attachments_test"
    
    # 測試 GCP 存儲
    test_gcp_storage(BUCKET_NAME)
    # 測試上傳檔案
    test_upload(BUCKET_NAME)