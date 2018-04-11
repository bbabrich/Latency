files=kyoto-train.en
#sep=$2
PARSERDIR=/home/chase/stanford-parser-full-2018-02-27
for file in $files; do
  java -Xmx32g -cp "$PARSERDIR/*:" edu.stanford.nlp.parser.lexparser.LexicalizedParser \
   -nthreads 1 \
   -sentences newline \
   -tokenized \
   -escaper edu.stanford.nlp.process.PTBEscapingProcessor \
   -outputFormatOptions "basicDependencies" \
   -outputFormat "words,oneline" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz $file > $file.parsed
done

