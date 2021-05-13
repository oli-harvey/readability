import os
import subprocess
import zipfile

def get_kaggle_data(
        competition: str,
        # competition_name: str, 
        dir: str = "competition_data"
        ) -> [str]:
    """
        Uses Kaggle API to download zip file of all kaggle competition data.
        Saves it in data directory, default competition_data
        Extracts files
        Deletes the zip file
        Returns list of files downloaded
    """

    dl_zip = [
        f"mkdir {dir}",
        f"kaggle competitions download -c {competition} -p {dir}",
    ]

    [
       subprocess.Popen(step, shell=True).wait()
       for step in dl_zip
    ]
    zip_path = f"{dir}/{competition}.zip"

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(f"{dir}/")
    
    rm_zip = f"rm {zip_path}"
    subprocess.Popen(rm_zip, shell=True).wait()

    print(f'files downloaded for {competition} competition')
    # print('   ' + os.listdir(dir))
    files = os.listdir(dir)
    [
        print('   ' + file)
        for file in files   
    ]
    print(f'located in /{dir}/')
    return files