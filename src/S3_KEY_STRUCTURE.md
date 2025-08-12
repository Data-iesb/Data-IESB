# S3 Key Structure - DataIESB Reports

## ✅ **New Simplified Structure**

The Lambda function now uses a clean, simple S3 key structure:

```
s3://dataiesb-reports/{report_id}/main.py
```

### Examples:
```
s3://dataiesb-reports/1/main.py
s3://dataiesb-reports/2/main.py
s3://dataiesb-reports/5/main.py
s3://dataiesb-reports/abc123/main.py
s3://dataiesb-reports/e86f197c-f476-440e-8bf1-700ef864a0b6/main.py
```

## 📁 **Bucket Organization**

### Reports Bucket (`s3://dataiesb-reports/`)
```
dataiesb-reports/
├── 1/
│   └── main.py
├── 2/
│   └── main.py
├── 5/
│   └── main.py
├── abc123/
│   └── main.py
└── e86f197c-f476-440e-8bf1-700ef864a0b6/
    └── main.py
```

### Datasets Bucket (`s3://dataiesb-datasets/`)
```
dataiesb-datasets/
├── dataset1.csv
├── dataset2.json
├── processed/
│   ├── data1.parquet
│   └── data2.csv
└── raw/
    ├── source1.xlsx
    └── source2.txt
```

## 🔄 **Before vs After**

### ❌ Old Structure (Complex)
```
s3://dataiesb-datasets/reports/user@email.com/uuid/main.py
```

### ✅ New Structure (Simple)
```
s3://dataiesb-reports/{report_id}/main.py
```

## 🎯 **Benefits**

1. **Simpler Paths**: Easy to understand and manage
2. **Direct Access**: Report ID directly maps to S3 path
3. **Better Organization**: Clear separation between reports and datasets
4. **Easier Debugging**: Simple structure for troubleshooting
5. **Scalable**: Works with any report ID format (numeric, UUID, etc.)

## 🔧 **Implementation Details**

The Lambda function automatically:
- Generates unique report IDs (UUID format)
- Creates the S3 key as `{report_id}/main.py`
- Stores metadata in DynamoDB with the S3 key reference
- Maintains user ownership through DynamoDB records

## 📋 **Test Results**

✅ **Verified Structure**: `s3://dataiesb-reports/e86f197c-f476-440e-8bf1-700ef864a0b6/main.py`

The test confirms the new structure works correctly with:
- Report creation
- File upload to correct location
- Soft delete (preserves S3 files)
- Restore functionality
- Download functionality
