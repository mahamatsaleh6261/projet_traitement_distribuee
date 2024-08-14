-- test.pig
data = LOAD 'hdfs:///hadoop-data/input/example.txt' AS (line:chararray);
words = FOREACH data GENERATE FLATTEN(TOKENIZE(line)) AS word;
grouped = GROUP words BY word;
counts = FOREACH grouped GENERATE group AS word, COUNT(words) AS count;
STORE counts INTO 'hdfs:///hadoop-data/output';
