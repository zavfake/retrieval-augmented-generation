Membuat pelayan cafe berbasis LLM menggunakan teknik RAG

Part I: Prepare Serverless Columnar Database
Video: https://ptorbitventurainodnesia-my.sharepoint.com/:v:/g/personal/cloud6_orbitfutureacademy_sch_id/EXAWlA0Rm7NDkn3CcDwuFdsBVPa1hqWAB0NgzScJa1xxxw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=NW4Uov

Steps:

1. Buat file CSV menggunakan spreadsheet. Sample data ada disini: https://docs.google.com/spreadsheets/d/1ukozLJjD__D1_oRJ81m9klYLqVMxuCu-KR8dlqRuFPc/edit?usp=sharing
2. Convert format CSV ke Parquet. Format parquet akan membuat data yang besar terkompresi menjadi 10x lipat lebih kecil dibanding format CSV.

   Online csv to parquet converter: https://www.agentsfordata.com/csv/to/parquet (seperti video)
   Online parquet reader: https://dataconverter.io/view/parquet (seperti video)
   Python converter & reader: pyarrow & pandas (jika ingin explorasi mandiri)
3. Buat S3, buat folder "menu" dan masukkan file parquet ke dalam folder tersebut
4. Buat glue crawler dengan step sebagai berikut:
   a. Buka glue, di menu kiri pilih data catalog -> crawler -> buat crawler baru
   b. Isi nama crawler dengan format: nama-bucket-crawler. Next
   c. Data source configuration pilih add data source. Pilih S3, S3 path pilih bucket yang dibuat di poin 3, add an s3 data source
   d. Creat IAM role. Next
   e. Target database: add database, nama-bucket-db
   f. Balik ke settingan database di glue, refresh lalu piluh database yang barusan dibuat
   g. Pada crawler schedule, buat schedule menggunakan format cron. Anda dapat menggunakan tool ini untuk membuat format cron: https://crontab.guru/
   h. Create crawler. Tunggu sampai state crawling done dan last run succeded.
   i. Setealah sukses, buka data catalog -> database -> pilih database yang baru dibuat tadi (nama-bucket-db) dan cek apakah didalamnya sudah terbuat table baru berisi menu di parquet kita. Jika belum silahkan tunggu sampai crawler selesai, jika sudah lanjut ke next step.
5. Buat athena connection ke glue data catalog:
   a. Buka athena, di menu kiri pilih query editor, di tab, pilih setting lalu klik manage. pada Location of query result pilih s3 bucket yang dibuat tadi, lalu klik save.
   b. Kembali ke editor via tab, lalu pilih database yang baru dibuat tadi, dan coba query sederhana seperti "SELECT * FROM nama_table" di tabel yang tersedia.
   c. Pastika query berhasil memanggil data parquet dengan lancar.

Part II: Integrate Bedrock with Athena using Lambda Function to Perform RAG
Video: https://ptorbitventurainodnesia-my.sharepoint.com/:v:/g/personal/instructor3_orbitfutureacademy_sch_id/EYqHqukHaxBHi3LO0aX0qMABRi4jqx4-q8QHf-rwbFvHHw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=ILxKk3

Steps:

1. Pastikan query menggunakan athena sudah berhasil
2. Buat lambda:
   a. Masukkan kode lambda_function.py -> test dengan lambda_invoke_test.json
   b. Jika ada error permission untuk mengeksekusi Athena query, modifikasi IAM role dari lambda, attach policy: AmazonAthenaFullAccess, AmazonS3FullAccess, AWSGlueConsoleFullAccess
   c. Pastikan function invocation berjalan normal sampai lambda dapat menampilkan hasil query athena.
3. Masuk ke bedrock -> agent
   a. Buat bedrock agent. Isikan nama, model: aws APAC novalite, masukkan instruction bedrock_agent_instruction.
   b. Klik save, prepare dan lakukan interaksi dengan model. Pastikan model dapat melakukan perkenalan diri dan basic natural converstation.
   c. Buat action group
   d. Isi nama, define with API schemas
   e. Select existing lambda function, pilih lambda function yg dibuat di step 2, Define via in-line schema editor isikan bedrock_inline_openapi_schema.json ke text editor.
   f. save, prepare dan coba tanya menu. pasti error permission.
4. Finalisasi permission
   a. Buka IAM -> role. Cari role yang namanya sama dengan iam di Agent resource role di bedrock Agent builder.
   Pastikan role tersebut memiliki: "bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream", "bedrock:GetInferenceProfile" "bedrock:GetFoundationModel". Jangan lupa pilih any resource in this account untuk menyimpan.
   b. Buka lambda -> pilih lambda yang dibuat di step 2 -> configuration -> permission -> Resource-based policy statements. Add permission.
   Isi Name: mirip dengan agent, Principal: bedrock.amazonaws.com, effect: Allow, Action: lambda:InvokeFunction
5. Balik ke agent, prepare, test lagi. Jika sudah bisa buat alis dan agent siap digunakan!

Part III: Using Bedrock Agent as an API Services

```
Mau lanjut ga? jika iya request di group ya guys! Jika banyak yg butuh saya lanjut 😁
```
