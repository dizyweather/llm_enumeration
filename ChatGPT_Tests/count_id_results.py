import os

resultdir = os.path.dirname(os.path.realpath(__file__)) + '/image_id_results'

for subdir, dirs, files in os.walk(resultdir):
    for file in files:
        f = open(resultdir + '/' + file, 'r')
        text = f.read()
        target = 'Identified'
        current_index = text.find(target)

        # Dictionaries to store words of each section
        identified_dict = {}
        missed_dict = {}
        unsure_dict = {}

        while current_index != -1:
            word_start_index = text.find('\t', current_index)
            missed_index = text.find('Missed', current_index)
            unsure_index = text.find('Unsure', current_index)

            # Find words in Identified Section
            while word_start_index < missed_index and word_start_index != -1:
                word_end_index = text.find('\n', word_start_index)
                word = text[word_start_index + 1:word_end_index]
                if identified_dict.get(word) == None:
                    identified_dict[word] = 1
                else:
                    identified_dict[word] = 1 + identified_dict[word]
                 
                word_start_index = text.find('\t', word_end_index)
            
            # Find words in Missed Section
            while word_start_index < unsure_index and word_start_index != -1:
                word_end_index = text.find('\n', word_start_index)
                word = text[word_start_index + 1:word_end_index]
                if missed_dict.get(word) == None:
                    missed_dict[word] = 1
                else:
                    missed_dict[word] = 1 + missed_dict[word]
                 
                word_start_index = text.find('\t', word_end_index)
            
            # Checks if this is end of file, if so we need special conditions for Unsure section
            current_index = text.find(target, current_index + len(target))
            end = False
            if current_index == -1:
                current_index = text.find('-', current_index)
                end = True

            # Find words in Unsure Section
            while word_start_index < current_index and word_start_index != -1:
                word_end_index = text.find('\n', word_start_index)
                word = text[word_start_index + 1:word_end_index]
                if unsure_dict.get(word) == None:
                    unsure_dict[word] = 1
                else:
                    unsure_dict[word] = 1 + unsure_dict[word]
                 
                word_start_index = text.find('\t', word_end_index)
            
            if end:
                current_index = -1

        output = open(os.path.dirname(os.path.realpath(__file__)) + '/image_id_summary/' + os.path.splitext(file)[0] + '.sum', 'w')
        sum = 0

        output.write('Identified\n')
        for key in identified_dict.keys():
            output.write('\t' + key + " [" + str(identified_dict[key]) + ']\n')
            sum = sum + identified_dict[key]
        output.write('\t--Sum [' + str(sum) + ']--\n')
        sum = 0

        output.write('\nMissed\n')
        for key in missed_dict.keys():
            output.write('\t' + key + " [" + str(missed_dict[key]) + ']\n')
            sum = sum + missed_dict[key]
        output.write('\t--Sum [' + str(sum) + ']--\n')
        sum = 0

        output.write('\nUnsure\n')
        for key in unsure_dict.keys():
            output.write('\t' + key + " [" + str(unsure_dict[key]) + ']\n')
            sum = sum + unsure_dict[key]
        output.write('\t--Sum [' + str(sum) + ']--\n')
        
        output.close()
            
    
        
        
       