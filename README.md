# wikipedia-category-csv
Output csv file for wikipedia category data which includes sub category info

# Dockerfile

categories.csv will be found in /tmp/categories.csv in docker container.
So, please follow the following step.

## Run a following command (It takes an hour)
```bash
docker run -d -v /tmp/:/tmp/ --rm niwatolli3/wikipedia-category-csv
```

You will see categories.csv in /tmp/categories.csv


