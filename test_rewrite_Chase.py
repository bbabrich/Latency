import sys, argparse
from rules import *
from rewriter import *

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('--filename', dest='filename', action='store', type=str, help='Path to parsed file', required=True)
   args = parser.parse_args()

   tgt_parse_file = args.filename

   rewriter = Rewriter()
   rules = [LooksLike(), Seem(), Clause(), Verb(), Conjunction(), Possessive(), Voice()]

   j = 0
   with open(tgt_parse_file, 'r') as fparse :
      tgt_sents = rewriter.read_sent_parse(fparse)
      for i, tgt_sent in enumerate(tgt_sents):
         #print i
         
         try:
            try:
                TreeUtil.label_idx(tgt_sent.parse_tree)
            except AssertionError:
                continue
         except ValueError:
            continue

         # apply rules in fixed order greedily
         tmp_tree = TreeUtil.deepcopy_parentedtree(tgt_sent.parse_tree)
         for rule in rules:
             #print 'RULE:', rule.name
             # rule is applicable
             try:
                 if rule.apply(tmp_tree):
                     if not rule.fail:
                         tgt_sent.parse_tree = TreeUtil.deepcopy_parentedtree(tmp_tree)
                         print j
                         print 'ORIGINAL:', tgt_sent.text() + '\n'
                         print 'REWRITTEN:', str(tgt_sent) + '\n'
                         j += 1
                         #print 'JAPANESE:',jaFile.line()
                     else:
                         tmp_tree = TreeUtil.deepcopy_parentedtree(tgt_sent.parse_tree)
                         #print 'failed and reverted'
                 else:
                     continue
                     #print 'not applicable'
             except:
                 continue
         # post-processing
         new_sent = str(tgt_sent)
         # may have inserted redundant comma
         new_sent = re.sub(r'[\.,] [\.,]', r',', new_sent)
         new_sent = re.sub(r'^ , ', r'', new_sent)
         new_sent = re.sub(r'\'\'|``', r'"', new_sent)
         #print 'NEW:', new_sent
