import os
import uuid
import cloudinary
import cloudinary.uploader


class Files:
    def __init__(self):
        cloudinary.config(
            cloud_name=os.getenv('CLOUDINARY_NAME'),
            api_key=os.getenv('CLOUDINARY_KEY'),
            api_secret=os.getenv('CLOUDINARY_SECRET')
        )


    def upload_file(self, storage_folder, file, file_type):

        file_hash = uuid.uuid4()

        public_file_name = f"{storage_folder}/{file_hash}"

        result = cloudinary.uploader.upload(
            file,
            public_id=public_file_name,
            resource_type=file_type)

        file_url = result['secure_url']

        return file_url