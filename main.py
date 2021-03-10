import json
import re
import pandas as pd

"""
containsField
    Inputs: 
        df: DataFrame
        field_name: Name of text field to evaluate
        value: Word to check existence of in the field provided
    Determines which records in the dataframe contain the specified word
"""
def containsField(df, field_name, value):
    return df[field_name].str.contains(rf'\b{value}\b', regex=True, flags=re.IGNORECASE)

"""
extractFields
    Inputs:
        line: Parsed line of JSON
    Returns a record with only the necessary fields extracted
"""
def extractFields(line):
    return {
        'post_id': line['post_id'],
        'author_id': line['author_id'],
        'blog_id': line['blog_id'],
        'title': line['title'],
        'like_count': line['like_count'],
    }

"""
fetchData
    Inputs:
        None
    Reads posts from the jsonl file and constructs a DataFrame with the fields we need
    and a liker_index ({ 'liker_id': [<array of posts liked>] }). Returns a tuple of these two objects
"""
def fetchData():
    # we only need columns like_count, post_id, author_id, blog_id, title
    with open('./posts.jsonl', 'r') as input_file:
        data = []
        liker_index = {}
        for line in input_file:
            parsed = json.loads(line)
            # To avoid copying a dataframe over and over we'll keep an array for now
            data.append(extractFields(parsed))

            # Parse the liker_ids so we can build the index
            likers = parsed.get('liker_ids', [])
            for liker in likers:
                if liker_index.get(liker, None) is None:
                    liker_index[liker] = []
                liker_index[liker].append(parsed['post_id'])

        df = pd.DataFrame(data)
        return (df, liker_index)

if __name__ == '__main__':
    df, liker_index = fetchData()

    # Question 1
    agged = df['like_count'].agg(['mean', 'median'])
    print('===== Question 1 =====\nMean: {}\nMedian: {}\n'.format(agged['mean'], agged['median']))

    # Question 2
    # Mean number of posts per author in sample set
    # We first need to group by author id
    avg_per_author = df.groupby('author_id').count()['post_id'].mean()
    print('===== Question 2 =====\nMean Number of Posts Per Author: {}\n'.format(avg_per_author))

    # Question 3
    # All posts referencing the word 'red' in the title
    """
    The limitations to my method of finding this is that each record has to be evaluated at search time. If we needed to 
    search for a long list of words in the sample set, this would not be a good method. In that case, I would want to either build 
    an inverted index of words (maybe like { 'word': [<array of post ids] }) so that a word search would be a constant time operation. 
    The trade off is this would use more memory to hold. Another thing I considered, but would also use more memory, would 
    be a one-hot encoding of words in the main dataframe so the df could simply be filtered based on the presence of a word.
    """
    word = 'red'
    cntns_red = df[containsField(df, 'title', word)].count()['title']
    print('===== Question 3 =====\nNumber of Posts Containing \'{}\': {}\n'.format(word, cntns_red))

    # Question 4
    # First filter records who's author *has* liked something, then find the unique values of the remaining 'author_id' field and count them
    havent_liked = df[~df['author_id'].isin(list(liker_index.keys()))]['author_id'].unique().shape[0]
    print('===== Question 4 =====\nNumber of Authors Who Haven\'t Liked Any Posts: {}\n'.format(havent_liked))

    # Question 5
    """
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
    """
