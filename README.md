Membuat pelayan cafe berbasis LLM menggunakan teknik RAG


Part I: Prepare Serverless Columnar Database

Tutorial Video

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

1. Pastikan query menggunakan athena sudah berhasil
2. Buat lambda:
  a. Masukkan kode lambda_function.py -> test dengan lambda_invoke_test.json
  b. Jika ada error permission untuk mengeksekusi Athena query, modifikasi IAM role dari lambda, attach policy: AmazonAthenaFullAccess, AmazonS3FullAccess, AWSGlueConsoleFullAccess
  c. Pastikan function invocation berjalan normal sampai lambda dapat menampilkan hasil query athena.
3. Masuk ke bedrock -> agent
  a. Buat bedrock agent. Isikan nama, model: aws APAC novalite, masukkan instruction bedrock_agent_instruction
  b. Pastikan agent memiliki permission: "bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream", "bedrock:GetInferenceProfile" "bedrock:GetFoundationModel".
4. Prepare dan test agent, jika sudah oke tinggal di publish.



Part III: Using Bedrock Agent as an API Services
...
