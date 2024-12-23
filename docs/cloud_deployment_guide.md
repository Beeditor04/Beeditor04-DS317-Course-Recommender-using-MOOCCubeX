--- 
### setup guide:
- Create Bucket on Google Storage and upload your dataset (`fine-grained` included, disabled `soft-delete`)
- setup local by installing [Gcloud CLI](https://cloud.google.com/sdk/docs/install)
- Create new projects
```
gcloud projects create PROJECT_ID
```
- Select the Google Cloud project that you created:
```
gcloud config set project PROJECT_ID
```
- Enable the Dataflow, Compute Engine, Cloud Logging, Cloud Storage, Google Cloud Storage JSON, BigQuery, Cloud Pub/Sub, Cloud Datastore, and Cloud Resource Manager APIs: 
```
gcloud services enable dataflow compute_component logging storage_component storage_api bigquery pubsub datastore.googleapis.com cloudresourcemanager.googleapis.com
```
-  Create local authentication credentials for your user account: 
```
gcloud auth application-default login
```
- Grant roles to your user account. Run the following command once for each of the following IAM roles: roles/iam.serviceAccountUser
```
gcloud projects add-iam-policy-binding PROJECT_ID --member="user:USER_IDENTIFIER" --role=ROLE
```
-  Replace `PROJECT_ID` with your project ID.
- Replace `USER_IDENTIFIER` with the identifier for your user account. For example, user:myemail@example.com.
- Replace `ROLE` with each individual role.
- Grant roles to your Compute Engine default service account. Run the following command once for each of the following IAM roles
```
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" --role=SERVICE_ACCOUNT_ROLE
```
- setup Python environment, refer to this [doc](https://docs.python.org/3/tutorial/venv.html)
- install Apache Beam SDK
```
pip install wheel
pip install 'apache-beam[gcp]'
```
### after finishing setup locally, run
```
cd src
python -m app
```