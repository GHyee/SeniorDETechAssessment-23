# Data Pipelines

The data pipeline consist of several python jobs to validate and transform the data.

The following validation is performed:
1. Check if the field `mobile_no` has 8 digit
2. Check if the field `email` ends with `@emailprovider.com` or `@emailprovider.net`