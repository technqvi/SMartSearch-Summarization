

def ingest_incident_json_to_gs(list_json:list[str],config)  :
    """
    Ingest json data to google cloud storage.
    Args:
        list_json (list[str]): List json files.
        config : .env Config file
    """


    # In[22]:


    from pathlib import Path
    import os
    from google.cloud.storage import Client, transfer_manager
    from dotenv import dotenv_values


    # # Reference

    # * https://cloud.google.com/storage/docs/samples/storage-transfer-manager-upload-directory#storage_transfer_manager_upload_directory-python
    # * https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python

    # In[23]:


    source_path=config['INPUT_SEARCH_DATA_PATH']
    target_gs_bucket=config['TARGET_SEARCH_GS_PATH']

    #comment
    list_json = [ x for x in os.listdir(source_path)  if x.endswith(".ndjson")]
    print(list_json)


    # In[24]:


    def upload_many_files_blobs_with_transfer_manager(
        bucket_name, filenames, source_directory="", workers=8
    ):
        """Upload every file in a list to a bucket, concurrently in a process pool.

        Each blob name is derived from the filename, not including the
        `source_directory` parameter. For complete control of the blob name for each
        file (and other aspects of individual blob metadata), use
        transfer_manager.upload_many() instead.
        """

        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # A list (or other iterable) of filenames to upload.
        # filenames = ["file_1.txt", "file_2.txt"]

        # The directory on your computer that is the root of all of the files in the
        # list of filenames. This string is prepended (with os.path.join()) to each
        # filename to get the full path to the file. Relative paths and absolute
        # paths are both accepted. This string is not included in the name of the
        # uploaded blob; it is only used to find the source files. An empty string
        # means "the current working directory". Note that this parameter allows
        # directory traversal (e.g. "/", "../") and is not intended for unsanitized
        # end user input.
        # source_directory=""

        # The maximum number of processes to use for the operation. The performance
        # impact of this value depends on the use case, but smaller files usually
        # benefit from a higher number of processes. Each additional process occupies
        # some CPU and memory resources until finished. Threads can be used instead
        # of processes by passing `worker_type=transfer_manager.THREAD`.
        # workers=8


        storage_client = Client()
        bucket = storage_client.bucket(bucket_name)

      # To advoid error from uploading, worker_type=transfer_manager.THREAD 
        results = transfer_manager.upload_many_from_filenames(
            bucket, filenames, source_directory=source_directory, max_workers=workers
            ,worker_type=transfer_manager.THREAD
        )

        for name, result in zip(filenames, results):
            # The results list is either `None` or an exception for each filename in
            # the input list, in order.

            if isinstance(result, Exception):
                print("Failed to upload {} due to exception: {}".format(name, result))
            else:
                print("Uploaded {} to {}.".format(name, bucket.name))




    upload_many_files_blobs_with_transfer_manager(target_gs_bucket,list_json,source_path,workers=1)


    return True

