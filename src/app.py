import apache_beam as beam
import json
import re
from apache_beam.options.pipeline_options import PipelineOptions

def parse_csv(line):
    # ...parse logic...
    return line.split(',')

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text).strip().lower()
    return text

def process_record(record, file_label):
    if isinstance(record, list):
        record = {str(i): v for i, v in enumerate(record)}
    
    if file_label == "course":
        record = {k: v for k, v in record.items() if k != 'name'}
        record = {k: v for k, v in record.items() if k != 'field_trans'}
        record = {k: v for k, v in record.items() if k != 'name_trans'}
    elif file_label == "concept":
        record = {k: v for k, v in record.items() if k != 'name'}
    elif file_label == "course_field":
        record["cleaned_course_name"] = re.sub(r'[^\w\s]', '', record.get("course_name", "")).strip().lower()
        record["field"] = ', '.join(record.get("field", []))
    elif file_label == "school":
        record["sign"] = record.get("sign", "").upper()
        record = {k: v for k, v in record.items() if k != 'name'}
    elif file_label == "teacher":
        record = {k: v for k, v in record.items() if k != 'name'}
    elif file_label == "user":
        record = {k: v for k, v in record.items() if k != 'name'}
    return record

def run():
    pipeline_options = PipelineOptions([
        "--runner=DataflowRunner",
        "--project=ds317-445515",
        "--temp_location=gs://ds317/temp",
    ])
    with beam.Pipeline(options=pipeline_options) as p:

        for file_label, file_path in [
            ("course", "gs://ds317/course.csv"),
            ("concept", "gs://ds317/concept.csv"),
            ("course_field", "gs://ds317/course_field.csv"),
            ("school", "gs://ds317/school.csv"),
            ("teacher", "gs://ds317/teacher.csv"),
            ("user", "gs://ds317/user.csv"),
        ]:
            (
                p
                | f"Read_{file_label}" >> beam.io.ReadFromText(file_path)
                | f"Parse_{file_label}" >> beam.Map(parse_csv)
                | f"Process_{file_label}" >> beam.Map(process_record, file_label=file_label)
                | f"Write_{file_label}" >> beam.io.WriteToText(f"gs://ds317/output/{file_label}_processed.csv")
            )

if __name__ == "__main__":
    run()