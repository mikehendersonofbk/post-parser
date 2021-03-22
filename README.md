
# Post Parser

## To Run
> docker-compose build post-parser  
> docker-compose up post-parser

In a separate terminal:
> docker exec -it post-parser python main.py

## About
All of the logic is located in the `main.py` file. It will read in the post data and construct a Pandas DataFrame as well as a 'liker' index, and perform some analysis on the data.

## Output

```
===== Question 1 =====
Mean: 4.238734931867639
Median: 0.0

===== Question 2 =====
Mean Number of Posts Per Author: 122.71579732754527

===== Question 3 =====
Number of Posts Containing 'red': 5093

===== Question 4 =====
Number of Authors Who Haven't Liked Any Posts: 6402

===== Question 5 =====

    To answer questions 1-4 I've used Pandas Dataframes and Series, and Numpy Arrays. I used these tools because this was a
    relatively small dataset, and the majority of each record was not needed to answer these questions (content, etc). I picked these tools
    because they are powerful libraries for performing aggregations and scalar operations across a dataset like this one, and this particular
    sample was small enough to work with in-memory on a single machine. If the sample data was just a little bit larger than this, I would have
    chunked my operations so that each chunk could be aggregated and/or reduced in size before moving on to the next chunk. If it was one hundred times
    the size of this one, I think a distributed process would have been appropriate. Some tools I could've chosen from are Spark, Dask, Hadoop, etc. Using
    one of these could have leveraged a number of machines to perform a MapReduce flavor of algorithm, where the data could be mapped/filtered across machines
    in parallel, and then finally combined to find the final results. At my current job, I have an ETL process which needs to aggregate data from millions of 
    user interactions each day, so I decided to use Dask to handle the processing. It's very similar to Spark and has an almost identical interface as a standard
    Pandas DataFrame, but it is capable of parallelizing a task across many workers, and a scheduler to perform the final merging once the workers have finished.
   ```
   
## Questions or Comments
For any questions or comments, feel free to contact me at `mike.w.henderson.88@gmail.com`.
