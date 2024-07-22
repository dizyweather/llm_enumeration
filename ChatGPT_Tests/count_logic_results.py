import os

resultdir = os.path.dirname(os.path.realpath(__file__)) + '/image_logic_results'

for subdir, dirs, files in os.walk(resultdir):
    for file in files:
        f = open(resultdir + '/' + file, 'r')
        text = f.read()
        target = 'True Positive'
        current_index = text.find(target)

        # Dictionaries to store words of each section
        true_pos_dict = {}
        false_pos_dict = {}
        true_neg_dict = {}
        false_neg_dict = {}

        while current_index != -1:
            word_start_index = text.find('\t', current_index)
            
            false_pos_index = text.find('False Positive', current_index)
            true_neg_index = text.find('True Negative', current_index)
            false_neg_index = text.find('False Negative', current_index)
            end_line_index = text.find('---', current_index)

            # Find words in True Positive Section
            while word_start_index < false_pos_index and word_start_index != -1:
                word_end_index = text.find('\n', word_start_index)
                word = text[word_start_index + 1:word_end_index]
                if true_pos_dict.get(word) == None:
                    true_pos_dict[word] = 1
                else:
                    true_pos_dict[word] = 1 + true_pos_dict[word]
                 
                word_start_index = text.find('\t', word_end_index)
            
            # Find words in False Positive Section
            while word_start_index < true_neg_index and word_start_index != -1:
                word_end_index = text.find('\n', word_start_index)
                word = text[word_start_index + 1:word_end_index]
                if false_pos_dict.get(word) == None:
                    false_pos_dict[word] = 1
                else:
                    false_pos_dict[word] = 1 + false_pos_dict[word]
                 
                word_start_index = text.find('\t', word_end_index)
            
            # Find words in True Negative Section
            while word_start_index < false_neg_index and word_start_index != -1:
                word_end_index = text.find('\n', word_start_index)
                word = text[word_start_index + 1:word_end_index]
                if true_neg_dict.get(word) == None:
                    true_neg_dict[word] = 1
                else:
                    true_neg_dict[word] = 1 + true_neg_dict[word]
                 
                word_start_index = text.find('\t', word_end_index)

            # Find words in False Negative Section
            while word_start_index < end_line_index and word_start_index != -1:
                word_end_index = text.find('\n', word_start_index)
                word = text[word_start_index + 1:word_end_index]
                if false_neg_dict.get(word) == None:
                    false_neg_dict[word] = 1
                else:
                    false_neg_dict[word] = 1 + false_neg_dict[word]
                 
                word_start_index = text.find('\t', word_end_index)
            
            current_index = text.find(target, current_index + len(target))

        output = open(os.path.dirname(os.path.realpath(__file__)) + '/image_logic_summary/' + os.path.splitext(file)[0] + '.sum', 'w')
        sum = 0

        output.write('True Positive\n')
        for key in true_pos_dict.keys():
            output.write('\t' + key + " [" + str(true_pos_dict[key]) + ']\n')
            sum = sum + true_pos_dict[key]
        output.write('\t--Sum [' + str(sum) + ']--\n')
        sum = 0

        output.write('\nFalse Positive\n')
        for key in false_pos_dict.keys():
            output.write('\t' + key + " [" + str(false_pos_dict[key]) + ']\n')
            sum = sum + false_pos_dict[key]
        output.write('\t--Sum [' + str(sum) + ']--\n')
        sum = 0

        output.write('\nTrue Negative\n')
        for key in true_neg_dict.keys():
            output.write('\t' + key + " [" + str(true_neg_dict[key]) + ']\n')
            sum = sum + true_neg_dict[key]
        output.write('\t--Sum [' + str(sum) + ']--\n')
        sum = 0

        output.write('\nFalse Negative\n')
        for key in false_neg_dict.keys():
            output.write('\t' + key + " [" + str(false_neg_dict[key]) + ']\n')
            sum = sum + false_neg_dict[key]
        output.write('\t--Sum [' + str(sum) + ']--\n')
        
        output.close()
            
    
        
        
       