import os,sys,requests
from zipfile import ZipFile

def download_zip_file(url, output_dir):
    response = requests.get(url, stream=True)
    os.makedirs(output_dir, exist_ok=True)

    if response.status_code == 200:
        filename = os.path.join(output_dir, "downloaded.zip")
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded zip file: {filename}")
        return filename
    else:
        raise Exception(f"Failed to download file: Status code {response.status_code}")

def extract_zip_file(zip_filename, output_dir):

    with ZipFile(zip_filename, "r") as zip_file:
        zip_file.extractall(output_dir)

    print(f"Extract files written to: {output_dir}")
    print("Removing the zip file")
    os.remove(zip_filename)

def fix_json_dict(output_dir):
    import json
    file_path = os.path.join(output_dir, "dict_artists.json")

    with open(file_path, "r") as f:
        data = json.load(f)

    with open(os.path.join(output_dir, "fixed_da.json"), "w", encoding="utf-8") as f_out:
        for key, value in data.items():
            record = {"id": key, "related_ids": value}
            json.dump(record, f_out, ensure_ascii = False)
            f_out.write("\n")
        print(f"File {file_path} has been fixed and written to {output_dir} as fixed_da.json")

    print("Removing the original file")
    os.remove(file_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Extraction path is required")
        print("Exame Usage:")
        print("python3 execute.py /home/Data/Extraction")
    else:
        try:
            print("Starting Extration Engine...")
            EXTRACT_PATH = sys.argv[1]
            KAGGLE_URL = "https://storage.googleapis.com/kaggle-data-sets/1993933/3294812/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20250722%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250722T014520Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=3182dc40eb52c481bf7254bb0c10a2a5a2a5b2d814bad0b563bcd2b3ba9e5f94598b0304a73a2c121c94499be8acd3e86fefe596d9d24b0116629de9b3cba8b6c6269c6d01fd7b4697162a6564b3a7791cef040f4abe7d3c34a1997b663ae27e5fa60e4105f39854b481bfa8743e7b82a9b59183d02f034674c308a32b5327b0c62c0e531e0a8ec25cd0ff603ba77939313e4b4f9aaf47caf4de3737ea632c6761cf4733de755f69f592ea114dfbab21b1dd79602cc7e406a4a70426d1fd67a1467caeae2f064bdb515fc820ee5ad3d1c5db883e4bd49721de7fe21f603ce84186c932987f3ad1ddb2213cb40d0914aaaadca19915105d716a855bbade4fcf3e"
            zip_filename = download_zip_file(KAGGLE_URL, EXTRACT_PATH)
            extract_zip_file(zip_filename, EXTRACT_PATH)
            fix_json_dict(EXTRACT_PATH)
            print("Extraction Successfully Completed!! :))")
        except Exception as e:
            print(f"Error: {e}")

