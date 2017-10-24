# wikipedia-category-csv
Output csv file for wikipedia category data which includes sub category info

# Dockerfile

categories.csv will be found in /opt/categories.csv in docker container.
So, please follow the following step.

## Run a following command (It takes an hour)
```bash
docker run -d -v /opt/:/opt/ --rm niwatolli3/wikipedia-category-csv
```

You will see categories.csv in /opt/categories.csv


